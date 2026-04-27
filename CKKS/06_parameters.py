import openfhe
import time

# ============================================
# PARAMETER 1: MultiplicativeDepth
# ============================================
# Maximum number of mulplications in the circuit. 
# Each multiplication increases the level by 1.
# If the circuit exceeds this depth, the evaluation will fail. 
# Trade-off: Higher depth allows more complex circuits but 
# increases noise and reduces performance.
# more > depth -> more noise -> more expensive to evaluate
#
# Rule of thumb:
#   Dot product:          depth = 1
#   Logistic regression:  depth = 4-5
#   Small neural net:     depth = 10-15
#   With bootstrapping:   unlimited (but expensive)
# ============================================

print("=" * 55)
print("EXPERIMENT 1: Impact of MultiplicativeDepth")
print("=" * 55)

for depth in [2, 5, 10]:
    params = openfhe.CCParamsCKKSRNS()
    params.SetMultiplicativeDepth(depth)
    params.SetScalingModSize(50)
    params.SetBatchSize(8)

    t0 = time.time()
    cc = openfhe.GenCryptoContext(params)
    cc.Enable(openfhe.PKESchemeFeature.PKE)
    cc.Enable(openfhe.PKESchemeFeature.LEVELEDSHE)
    kp = cc.KeyGen()
    t1 = time.time()

    # Encrypt a simple vector
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    ptxt = cc.MakeCKKSPackedPlaintext(x)
    ctxt = cc.Encrypt(kp.publicKey, ptxt)

    ring_dim = cc.GetRingDimension()
    print(f"\nDepth={depth:2d} | "
          f"RingDim={ring_dim:6d} | "
          f"Setup time={t1-t0:.3f}s")

# ============================================
# PARAMETER 2: ScalingModSize
# ============================================
# So bits cua scaling factor Delta = 2^ScalingModSize
# Trade-off:
#   Lon hon -> precision cao hon -> modulus lon hon -> cham hon
#   Typical values: 40-60 bits
#   < 20: too low, severe precision loss
#   > 60: diminishing returns, too slow
# ============================================

print("\n" + "=" * 55)
print("EXPERIMENT 2: Impact of ScalingModSize (precision)")
print("=" * 55)

x = [1.234567890123456]

for mod_size in [20, 30, 40, 50]:
    params = openfhe.CCParamsCKKSRNS()
    params.SetMultiplicativeDepth(1)
    params.SetScalingModSize(mod_size)
    params.SetBatchSize(1)

    cc = openfhe.GenCryptoContext(params)
    cc.Enable(openfhe.PKESchemeFeature.PKE)
    kp = cc.KeyGen()

    ptxt = cc.MakeCKKSPackedPlaintext(x)
    ctxt = cc.Encrypt(kp.publicKey, ptxt)
    result = cc.Decrypt(ctxt, kp.secretKey)
    result.SetLength(1)

    print(f"\nScalingModSize={mod_size} | Delta=2^{mod_size}")
    print(f"  Original:  {x[0]:.15f}")
    print(f"  Decrypted: {result}")

# ============================================
# PARAMETER 3: BatchSize
# ============================================
# So slots active trong mot ciphertext
# Toi da = N/2 (ring dimension / 2)
# Trade-off:
#   Lon hon -> pack duoc nhieu data hon (hieu qua hon)
#   Khong anh huong toc do (da fixed boi RingDim)
#   Nen luon set = so phan tu trong vector cua ban
# ============================================

print("\n" + "=" * 55)
print("EXPERIMENT 3: BatchSize — slots per ciphertext")
print("=" * 55)

params = openfhe.CCParamsCKKSRNS()
params.SetMultiplicativeDepth(1)
params.SetScalingModSize(50)
params.SetBatchSize(8)

cc = openfhe.GenCryptoContext(params)
cc.Enable(openfhe.PKESchemeFeature.PKE)
kp = cc.KeyGen()

ring_dim = cc.GetRingDimension()
print(f"RingDimension = {ring_dim}")
print(f"Max slots     = {ring_dim // 2}")
print(f"BatchSize set = 8")

# Pack 4 numbers into 8-slot ciphertext
x_small = [1.0, 2.0, 3.0, 4.0]
ptxt = cc.MakeCKKSPackedPlaintext(x_small)
ctxt = cc.Encrypt(kp.publicKey, ptxt)

result = cc.Decrypt(ctxt, kp.secretKey)
result.SetLength(8)
print(f"\nPacked [1,2,3,4] into 8-slot ciphertext:")
print(f"Result: {result}")
print("Observe: remaining slots are 0 (padding)")