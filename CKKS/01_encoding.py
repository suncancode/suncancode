import openfhe

# ============================================
# SETUP: Initialize crypto context
# ============================================
parameters = openfhe.CCParamsCKKSRNS()
parameters.SetMultiplicativeDepth(1)
parameters.SetScalingModSize(50)   # Delta = 2^50
parameters.SetBatchSize(4)         # Use 4 slots only

cc = openfhe.GenCryptoContext(parameters)
cc.Enable(openfhe.PKESchemeFeature.PKE)

# ============================================
# ENCODING: Vector -> Plaintext polynomial
# ============================================
z = [1.5, 2.7, 3.3, 4.1]
print(f"Input vector:        {z}")

ptxt = cc.MakeCKKSPackedPlaintext(z)

# ============================================
# DECODING: Plaintext polynomial -> Vector
# ============================================
ptxt.SetLength(4)
print(f"After encode/decode: {ptxt}")
print()
print("Observe: values are approximate but not exact")
print("This is the core property of CKKS approximate arithmetic")

