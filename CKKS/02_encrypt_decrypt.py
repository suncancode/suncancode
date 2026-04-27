import openfhe

# ============================================
# SETUP
# ============================================
parameters = openfhe.CCParamsCKKSRNS()
parameters.SetMultiplicativeDepth(1)
parameters.SetScalingModSize(50)
parameters.SetBatchSize(4)

cc = openfhe.GenCryptoContext(parameters)
cc.Enable(openfhe.PKESchemeFeature.PKE)

# ============================================
# KEY GENERATION
# ============================================
keypair = cc.KeyGen()
print("Keys generated:")
print("  - Secret key: known only to data owner")
print("  - Public key: shared with compute server")

# ============================================
# ENCRYPT
# ============================================
z = [1.5, 2.7, 3.3, 4.1]
ptxt = cc.MakeCKKSPackedPlaintext(z)
ctxt = cc.Encrypt(keypair.publicKey, ptxt)

print(f"\nOriginal vector:  {z}")
print(f"Ciphertext level: {ctxt.GetLevel()}")
print(f"(Server sees only ciphertext - cannot recover values)")

# ============================================
# DECRYPT
# ============================================
result = cc.Decrypt(ctxt, keypair.secretKey)
result.SetLength(4)

print(f"\nDecrypted result: {result}")
print("\nObserve: small noise introduced by encryption/decryption")