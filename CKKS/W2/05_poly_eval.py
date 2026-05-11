import openfhe

# ============================================
# SETUP
# ============================================
parameters = openfhe.CCParamsCKKSRNS()
parameters.SetMultiplicativeDepth(4)   # Need more depth for poly
parameters.SetScalingModSize(50)
parameters.SetBatchSize(4)

cc = openfhe.GenCryptoContext(parameters)
cc.Enable(openfhe.PKESchemeFeature.PKE)
cc.Enable(openfhe.PKESchemeFeature.LEVELEDSHE)

keypair = cc.KeyGen()
cc.EvalMultKeyGen(keypair.secretKey)

# ============================================
# INPUT
# ============================================
x = [0.5, 1.0, 1.5, 2.0]
expected = [(xi + 1)**2 for xi in x]

print(f"Input x:               {x}")
print(f"Expected f(x)=(x+1)^2: {expected}")

ptxt_x = cc.MakeCKKSPackedPlaintext(x)
ctxt_x = cc.Encrypt(keypair.publicKey, ptxt_x)
print(f"\nLevel after encrypt: {ctxt_x.GetLevel()}")

# ============================================
# EVALUATE f(x) = x^2 + 2x + 1
# METHOD: Direct computation
#
# Circuit:
#   x^2      = Mult(x, x)          -> 1 mult, level+1
#   2x       = Add(x, x)           -> free
#   x^2 + 2x = Add(x^2, 2x)       -> free
#   + 1      = Add(..., ptxt_one)  -> free
# ============================================
print("\n--- METHOD 1: Direct Computation ---")
print("Circuit: f(x) = x*x + x + x + 1")

# x^2
ctxt_x2 = cc.EvalMult(ctxt_x, ctxt_x)
print(f"After x^2:       level = {ctxt_x2.GetLevel()}")

# 2x = x + x
ctxt_2x = cc.EvalAdd(ctxt_x, ctxt_x)
print(f"After 2x:        level = {ctxt_2x.GetLevel()}")

# x^2 + 2x
# Need same level -> ModReduce x to match x^2
ctxt_x2_plus_2x = cc.EvalAdd(ctxt_x2, ctxt_2x)
print(f"After x^2+2x:    level = {ctxt_x2_plus_2x.GetLevel()}")

# + 1 (add plaintext constant, free)
ptxt_one = cc.MakeCKKSPackedPlaintext([1.0, 1.0, 1.0, 1.0])
ctxt_result = cc.EvalAdd(ctxt_x2_plus_2x, ptxt_one)
print(f"After +1:        level = {ctxt_result.GetLevel()}")

result = cc.Decrypt(ctxt_result, keypair.secretKey)
result.SetLength(4)
print(f"\nExpected: {expected}")
print(f"Got:      {result}")

# ============================================
# EVALUATE f(x) = x^2 + 2x + 1
# METHOD 2: Horner's method
#
# f(x) = 1 + x*(2 + x*1)
# Circuit:
#   Step 1: inner = Mult(x, 1)     -> 1 mult
#   Step 2: inner = Add(inner, 2)  -> free
#   Step 3: result = Mult(x, inner)-> 1 mult
#   Step 4: result = Add(result,1) -> free
#
# Same depth (2 mults) but better for higher degree
# ============================================
print("\n--- METHOD 2: Horner's Method ---")
print("Circuit: f(x) = 1 + x*(2 + x*1)")

ctxt_x_fresh = cc.Encrypt(keypair.publicKey, ptxt_x)

# Step 1: x * 1 = x  (innermost term, coefficient of x^2)
ptxt_coef2 = cc.MakeCKKSPackedPlaintext([1.0, 1.0, 1.0, 1.0])
ctxt_h = cc.EvalMult(ctxt_x_fresh, ptxt_coef2)
print(f"After x*1:       level = {ctxt_h.GetLevel()}")

# Step 2: x + 2  (add coefficient of x^1)
ptxt_coef1 = cc.MakeCKKSPackedPlaintext([2.0, 2.0, 2.0, 2.0])
ctxt_h = cc.EvalAdd(ctxt_h, ptxt_coef1)
print(f"After +2:        level = {ctxt_h.GetLevel()}")

# Step 3: x * (x + 2)
ctxt_h = cc.EvalMult(ctxt_x_fresh, ctxt_h)
print(f"After x*(x+2):   level = {ctxt_h.GetLevel()}")

# Step 4: + 1  (add constant term)
ptxt_coef0 = cc.MakeCKKSPackedPlaintext([1.0, 1.0, 1.0, 1.0])
ctxt_h = cc.EvalAdd(ctxt_h, ptxt_coef0)
print(f"After +1:        level = {ctxt_h.GetLevel()}")

result_horner = cc.Decrypt(ctxt_h, keypair.secretKey)
result_horner.SetLength(4)
print(f"\nExpected: {expected}")
print(f"Got:      {result_horner}")

# ============================================
# DEPTH COMPARISON
# ============================================
print("\n--- DEPTH ANALYSIS ---")
print(f"Both methods use 2 multiplications for degree-2 poly")
print(f"General rule: degree-d poly needs d multiplications (naive)")
print(f"              Horner reduces to exactly d multiplications")
print(f"              Paterson-Stockmeyer reduces to ~2*sqrt(d)")
print(f"\nFor PPML activation functions:")
print(f"  sigmoid degree-7  -> 7 mults (naive) or 4 (Horner)")
print(f"  sigmoid degree-15 -> 15 mults (naive) or 8 (Horner)")
print(f"  -> This is why depth budget is a critical resource!")