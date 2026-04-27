import openfhe
import math

# ============================================
# SETUP
# ============================================
parameters = openfhe.CCParamsCKKSRNS()
parameters.SetMultiplicativeDepth(2)
parameters.SetScalingModSize(50)
parameters.SetBatchSize(8)

cc = openfhe.GenCryptoContext(parameters)
cc.Enable(openfhe.PKESchemeFeature.PKE)
cc.Enable(openfhe.PKESchemeFeature.LEVELEDSHE)

keypair = cc.KeyGen()
cc.EvalMultKeyGen(keypair.secretKey)

# Generate rotation keys for slot summation
# For n=8 slots: need rotations 1, 2, 4
rotation_steps = [1, 2, 4]
cc.EvalRotateKeyGen(keypair.secretKey, rotation_steps)
print(f"Rotation keys generated for steps: {rotation_steps}")

# ============================================
# INPUT VECTORS
# ============================================
n = 8
a = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
b = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

expected = sum(a[i] * b[i] for i in range(n))
print(f"\nVector a: {a}")
print(f"Vector b: {b}")
print(f"Expected dot product: {expected}")

# ============================================
# ENCRYPT
# ============================================
ptxt_a = cc.MakeCKKSPackedPlaintext(a)
ptxt_b = cc.MakeCKKSPackedPlaintext(b)

ctxt_a = cc.Encrypt(keypair.publicKey, ptxt_a)
ctxt_b = cc.Encrypt(keypair.publicKey, ptxt_b)

# ============================================
# STEP 1: Componentwise multiplication
# ============================================
ctxt_prod = cc.EvalMult(ctxt_a, ctxt_b)
print(f"\n--- STEP 1: Componentwise Multiply ---")
print(f"Level after mult: {ctxt_prod.GetLevel()}")

# Verify intermediate result
tmp = cc.Decrypt(ctxt_prod, keypair.secretKey)
tmp.SetLength(n)
print(f"Intermediate slots: {tmp}")

# ============================================
# STEP 2: Slot summation via rotate-and-add
# ============================================
print(f"\n--- STEP 2: Rotate-and-Add ({int(math.log2(n))} steps) ---")

ctxt_sum = ctxt_prod
for step in rotation_steps:
    ctxt_rot = cc.EvalRotate(ctxt_sum, step)
    ctxt_sum = cc.EvalAdd(ctxt_sum, ctxt_rot)
    print(f"  After rotate({step}) + add: level = {ctxt_sum.GetLevel()}")

# ============================================
# RESULT: Read slot 0
# ============================================
result = cc.Decrypt(ctxt_sum, keypair.secretKey)
result.SetLength(n)

print(f"\n--- RESULT ---")
print(f"All slots: {result}")
print(f"Slot 0 (dot product): {result}")
print(f"Expected:             {expected}")
print(f"\nLevel after full dot product: {ctxt_sum.GetLevel()}")
print(f"Rotations used: {len(rotation_steps)} = log2({n})")