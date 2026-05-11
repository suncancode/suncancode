import openfhe
import math

# ============================================
# Fix 1: Use value with many decimal places
# to actually observe precision loss
# ============================================
print("=" * 65)
print("PRECISION LOSS — USING NON-TRIVIAL VALUES")
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

# Use pi — many decimal places, good for measuring error
import math
true_val = math.pi / 4   # 0.7853981633974483
x = [true_val, true_val, true_val, true_val]

ptxt_x   = cc.MakeCKKSPackedPlaintext(x)
ptxt_mul = cc.MakeCKKSPackedPlaintext([0.9999, 0.9999, 0.9999, 0.9999])

c_cur  = cc.Encrypt(kp.publicKey, ptxt_x)
c_mul  = cc.Encrypt(kp.publicKey, ptxt_mul)

print(f"\nTrue value: {true_val:.15f}")
print(f"\n{'Mults':>5} | {'Level':>5} | {'Decrypted[0]':>20} | "
      f"{'Abs Error':>12} | {'Precision'}")
print("-" * 75)

for i in range(7):
    result = cc.Decrypt(c_cur, kp.secretKey)
    result.SetLength(4)

    # Parse first value
    decrypted_str = str(result)
    first_val = float(decrypted_str.split("(")[1].split(",")[0].strip())

    # Note: after multiplying by 0.9999 repeatedly,
    # true value changes — track it
    expected = true_val * (0.9999 ** i)
    abs_error = abs(first_val - expected)

    if abs_error > 0:
        bits_precision = -math.log2(abs_error)
        bits_lost = 50 - int(bits_precision)
    else:
        bits_precision = 50
        bits_lost = 0

    print(f"{i:>5} | {c_cur.GetLevel():>5} | "
          f"{first_val:>20.15f} | "
          f"{abs_error:>12.2e} | "
          f"~{int(bits_precision)} bits remaining")

    if i < 6:
        c_cur = cc.EvalMult(c_cur, c_mul)

# ============================================
# Fix 2: Corrected parameter selection guide
# ScalingModSize must be in [14, 59]
# ============================================
print("\n" + "=" * 65)
print("PARAMETER SELECTION GUIDE (FIXED)")
print("=" * 65)

test_cases = [
    # name                          depth  scale  batch
    ("Dot product (n=8)",               1,    50,    8),
    ("Logistic regression",             5,    50,   64),
    ("Degree-7 poly activation",        4,    50,   64),
    ("2-layer NN (depth 10)",          10,    50,  128),
    ("Deep circuit — boost precision", 10,    59,  128),  # fix: 59 not 60
    ("Fast low-precision",              3,    40,   32),
]

print(f"\n{'Use case':<35} | {'D':>3} | {'Δ':>4} | "
      f"{'N':>6} | {'Slots':>6} | {'Final precision'}")
print("-" * 85)

for name, depth, scale, batch in test_cases:
    p = openfhe.CCParamsCKKSRNS()
    p.SetMultiplicativeDepth(depth)
    p.SetScalingModSize(scale)
    p.SetBatchSize(batch)

    cc_tmp = openfhe.GenCryptoContext(p)
    N      = cc_tmp.GetRingDimension()
    slots  = N // 2

    # Theoretical: scale - encryption_noise(6) - per_mult_loss(4)*depth
    final_bits = scale - 6 - (depth * 4)
    final_dec  = max(0, final_bits) // 3

    flag = " ← WARNING: low precision!" if final_bits < 20 else ""

    print(f"{name:<35} | {depth:>3} | {scale:>4} | "
          f"{N:>6} | {slots:>6} | "
          f"~{max(0,final_bits):>3} bits "
          f"(~{final_dec} dec){flag}")

# ============================================
# Key insight: WHY depth 10 with scale 50
# gives only 4 bits precision
# ============================================
print("\n" + "=" * 65)
print("WHY DEEP CIRCUITS LOSE PRECISION")
print("=" * 65)
print(f"""
Budget breakdown for Depth=10, ScalingModSize=50:

  Starting budget:          50 bits
  Encryption noise:         -6 bits  → 44 bits
  Per-multiplication loss:  -4 bits × 10 = -40 bits
                            ─────────────────────
  Remaining:                 4 bits  ← barely usable!

Fix options:
  Option A: Increase ScalingModSize to 59
            → 59 - 6 - 40 = 13 bits remaining (better)

  Option B: Reduce depth (optimize circuit)
            depth=5: 50 - 6 - 20 = 24 bits ✓

  Option C: Use bootstrapping
            → Refresh modulus mid-circuit
            → Maintain precision throughout
            → But adds ~20 levels overhead

Rule of thumb:
  Target final precision ≥ 20 bits for ML tasks
  → ScalingModSize ≥ 6 + 4×depth + 20
  → For depth=10: ScalingModSize ≥ 66... exceeds limit!
  → Must use bootstrapping for depth > 10
""")