import openfhe

# ============================================
# SETUP
# ============================================
parameters = openfhe.CCParamsCKKSRNS()
parameters.SetMultiplicativeDepth(2)   # Need depth 2 for mult
parameters.SetScalingModSize(50)
parameters.SetBatchSize(4)

cc = openfhe.GenCryptoContext(parameters)
cc.Enable(openfhe.PKESchemeFeature.PKE)
cc.Enable(openfhe.PKESchemeFeature.LEVELEDSHE)

keypair = cc.KeyGen()
cc.EvalMultKeyGen(keypair.secretKey)   # Required for multiplication

# ============================================
# ENCRYPT TWO VECTORS
# ============================================
a = [1.0, 2.0, 3.0, 4.0]
b = [0.5, 1.5, 2.5, 3.5]

ptxt_a = cc.MakeCKKSPackedPlaintext(a)
ptxt_b = cc.MakeCKKSPackedPlaintext(b)

ctxt_a = cc.Encrypt(keypair.publicKey, ptxt_a)
ctxt_b = cc.Encrypt(keypair.publicKey, ptxt_b)

print(f"Vector a: {a}")
print(f"Vector b: {b}")
print(f"Level after encrypt: {ctxt_a.GetLevel()}")

# ============================================
# HOMOMORPHIC ADDITION
# ============================================
ctxt_add = cc.EvalAdd(ctxt_a, ctxt_b)

result_add = cc.Decrypt(ctxt_add, keypair.secretKey)
result_add.SetLength(4)

expected_add = [a[i] + b[i] for i in range(4)]
print(f"\n--- ADDITION ---")
print(f"Expected:  {expected_add}")
print(f"Got:       {result_add}")
print(f"Level after add: {ctxt_add.GetLevel()}  (unchanged)")

# ============================================
# HOMOMORPHIC MULTIPLICATION
# ============================================
ctxt_mult = cc.EvalMult(ctxt_a, ctxt_b)

result_mult = cc.Decrypt(ctxt_mult, keypair.secretKey)
result_mult.SetLength(4)

expected_mult = [a[i] * b[i] for i in range(4)]
print(f"\n--- MULTIPLICATION ---")
print(f"Expected:  {expected_mult}")
print(f"Got:       {result_mult}")
print(f"Level after mult: {ctxt_mult.GetLevel()}  (decreased by 1)")

# ============================================
# LEVEL COMPARISON
# ============================================
print(f"\n--- LEVEL SUMMARY ---")
print(f"After encrypt:  level = {ctxt_a.GetLevel()}")
print(f"After add:      level = {ctxt_add.GetLevel()}  (free operation)")
print(f"After mult:     level = {ctxt_mult.GetLevel()}  (costs 1 level)")