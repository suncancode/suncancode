import openfhe

# ============================================
# Visualize modulus chain
# ============================================
print("=" * 60)
print("HOW PARAMETERS MAP TO MODULUS CHAIN")
print("=" * 60)

depth      = 3
scale_bits = 50

params = openfhe.CCParamsCKKSRNS()
params.SetMultiplicativeDepth(depth)
params.SetScalingModSize(scale_bits)
params.SetBatchSize(4)

cc = openfhe.GenCryptoContext(params)
cc.Enable(openfhe.PKESchemeFeature.PKE)
cc.Enable(openfhe.PKESchemeFeature.LEVELEDSHE)

kp = cc.KeyGen()
cc.EvalMultKeyGen(kp.secretKey)

ring_dim = cc.GetRingDimension()

print(f"\nParameters set:")
print(f"  MultiplicativeDepth = {depth}")
print(f"  ScalingModSize      = {scale_bits} bits")
print(f"  → Delta             = 2^{scale_bits}")
print(f"  → Total modulus     ≈ {scale_bits * depth + 60} bits")
print(f"  → Ring dimension N  = {ring_dim}")
print(f"  → Max slots         = {ring_dim // 2}")

# ============================================
# Track level consumption through operations
# ============================================
print("\n" + "=" * 60)
print("LEVEL CONSUMPTION THROUGH CIRCUIT")
print("=" * 60)

x = [1.0, 2.0, 3.0, 4.0]
ptxt = cc.MakeCKKSPackedPlaintext(x)

c = cc.Encrypt(kp.publicKey, ptxt)
print(f"\nAfter Encrypt:   level={c.GetLevel()}  "
      f"(modulus = q₀·Δ^{depth})")

c = cc.EvalMult(c, c)
print(f"After Mult 1:    level={c.GetLevel()}  "
      f"(modulus = q₀·Δ^{depth-1})")

c = cc.EvalMult(c, c)
print(f"After Mult 2:    level={c.GetLevel()}  "
      f"(modulus = q₀·Δ^{depth-2})")

c = cc.EvalMult(c, c)
print(f"After Mult 3:    level={c.GetLevel()}  "
      f"(modulus = q₀·Δ^{depth-3} = q₀)")

# ============================================
# What happens when you exceed depth?
# ============================================
print("\n" + "=" * 60)
print("WHAT HAPPENS IF YOU EXCEED DEPTH?")
print("=" * 60)

try:
    c = cc.EvalMult(c, c)   # depth+1 multiplication
    print("Mult 4: no error raised by OpenFHE...")
    result = cc.Decrypt(c, kp.secretKey)
    result.SetLength(4)
    print(f"But result is garbage: {result}")
except Exception as e:
    print(f"Error: {e}")

# ============================================
# Precision loss per multiplication
# ============================================
print("\n" + "=" * 60)
print("PRECISION LOSS PER MULTIPLICATION")
print("=" * 60)

params2 = openfhe.CCParamsCKKSRNS()
params2.SetMultiplicativeDepth(6)
params2.SetScalingModSize(50)
params2.SetBatchSize(1)

cc2 = openfhe.GenCryptoContext(params2)
cc2.Enable(openfhe.PKESchemeFeature.PKE)
cc2.Enable(openfhe.PKESchemeFeature.LEVELEDSHE)
kp2 = cc2.KeyGen()
cc2.EvalMultKeyGen(kp2.secretKey)

# Use x = 1.0 so x^(2^k) stays bounded
val = [1.0]
ptxt_val = cc2.MakeCKKSPackedPlaintext(val)
c_val    = cc2.Encrypt(kp2.publicKey, ptxt_val)

# Also encrypt 1.0 separately to multiply with
ptxt_one = cc2.MakeCKKSPackedPlaintext([1.0])
c_one    = cc2.Encrypt(kp2.publicKey, ptxt_one)

print(f"\n{'Mults':>6} | {'Level':>6} | {'Result':>20} | Precision")
print("-" * 60)

c_cur = c_val
for i in range(6):
    result = cc2.Decrypt(c_cur, kp2.secretKey)
    result.SetLength(1)
    print(f"{i:>6} | {c_cur.GetLevel():>6} | {str(result)[:20]:>20}")
    if i < 5:
        c_cur = cc2.EvalMult(c_cur, c_one)