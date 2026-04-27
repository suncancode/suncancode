import openfhe
import math

# ============================================
# Precisely measure precision loss per mult
# ============================================
print("=" * 65)
print("PRECISION LOSS PER MULTIPLICATION — DETAILED")
print("=" * 65)

params = openfhe.CCParamsCKKSRNS()
params.SetMultiplicativeDepth(6)
params.SetScalingModSize(50)
params.SetBatchSize(4)

cc = openfhe.GenCryptoContext(params)
cc.Enable(openfhe.PKESchemeFeature.PKE)
cc.Enable(openfhe.PKESchemeFeature.LEVELEDSHE)
kp = cc.KeyGen()
cc.EvalMultKeyGen(kp.secretKey)

# Use values close to 1.0 to avoid overflow
# x^(2^k) stays near 1 if x = 1.0
x = [1.0, 1.0, 1.0, 1.0]

# Also need a "neutral" ciphertext to multiply with
# (multiplying by 1 to consume depth without changing value)
ptxt_x   = cc.MakeCKKSPackedPlaintext(x)
ptxt_one = cc.MakeCKKSPackedPlaintext([1.0, 1.0, 1.0, 1.0])

c_cur  = cc.Encrypt(kp.publicKey, ptxt_x)
c_one  = cc.Encrypt(kp.publicKey, ptxt_one)

print(f"\n{'Mults':>5} | {'Level':>5} | {'Decrypted[0]':>20} | "
      f"{'Abs Error':>12} | {'Bits lost':>9}")
print("-" * 70)

for i in range(7):
    # Decrypt and measure error
    result = cc.Decrypt(c_cur, kp.secretKey)
    result.SetLength(4)

    # Extract first value as float for error measurement
    # OpenFHE returns a Plaintext object - convert via string parsing
    decrypted_str = str(result)
    # Parse first value from "(val1, val2, ...)" format
    first_val = float(decrypted_str.split("(")[1].split(",")[0].strip())

    abs_error  = abs(first_val - 1.0)
    bits_lost  = -math.log2(abs_error) if abs_error > 0 else 50
    bits_remaining = 50 - i * 4  # theoretical

    print(f"{i:>5} | {c_cur.GetLevel():>5} | "
          f"{first_val:>20.15f} | "
          f"{abs_error:>12.2e} | "
          f"~{50 - int(bits_lost):>2} bits lost")

    if i < 6:
        c_cur = cc.EvalMult(c_cur, c_one)

# ============================================
# Practical parameter selection guide
# ============================================
print("\n" + "=" * 65)
print("PARAMETER SELECTION GUIDE")
print("=" * 65)

test_cases = [
    ("Dot product (n=8)",          1,  50, 8),
    ("Logistic regression",        5,  50, 64),
    ("Degree-7 poly activation",   4,  50, 64),
    ("2-layer NN (depth 10)",      10, 50, 128),
    ("High precision dot product", 1,  60, 8),
    ("Fast low-precision",         3,  40, 32),
]

print(f"\n{'Use case':<35} | {'D':>3} | {'Δ bits':>6} | "
      f"{'N':>6} | {'Slots':>6} | {'Est. final precision':>20}")
print("-" * 90)

for name, depth, scale, batch in test_cases:
    p = openfhe.CCParamsCKKSRNS()
    p.SetMultiplicativeDepth(depth)
    p.SetScalingModSize(scale)
    p.SetBatchSize(batch)

    cc_tmp = openfhe.GenCryptoContext(p)
    N      = cc_tmp.GetRingDimension()
    slots  = N // 2

    # Theoretical precision estimate
    final_precision = scale - 6 - (depth * 4)

    print(f"{name:<35} | {depth:>3} | {scale:>6} | "
          f"{N:>6} | {slots:>6} | "
          f"~{max(0, final_precision):>3} bits "
          f"(~{max(0,final_precision)//3} decimal digits)")

# ============================================
# The key trade-off triangle
# ============================================
print("\n" + "=" * 65)
print("THE THREE-WAY TRADE-OFF IN CKKS")
print("=" * 65)
print("""
        PRECISION
           /\\
          /  \\
         /    \\
        /      \\
       /________\\
    SPEED      DEPTH

  - More DEPTH    → larger modulus → larger N → SLOWER
  - More PRECISION → larger Δ     → larger N → SLOWER
  - More SPEED    → smaller N     → less DEPTH and PRECISION

  In practice for PPML:
    Fix target precision first (usually 20+ bits is enough)
    Then minimize depth (optimize circuit)
    Then tune ScalingModSize for speed vs precision balance
""")