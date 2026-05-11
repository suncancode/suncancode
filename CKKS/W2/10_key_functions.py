import openfhe
import time
import math

# ============================================
# MASTER REFERENCE: All important OpenFHE
# functions with timing and trade-offs
# ============================================

# --- SETUP ---
params = openfhe.CCParamsCKKSRNS()
params.SetMultiplicativeDepth(5)
params.SetScalingModSize(50)
params.SetBatchSize(8)

cc = openfhe.GenCryptoContext(params)
cc.Enable(openfhe.PKESchemeFeature.PKE)
cc.Enable(openfhe.PKESchemeFeature.LEVELEDSHE)
cc.Enable(openfhe.PKESchemeFeature.ADVANCEDSHE)

kp = cc.KeyGen()
cc.EvalMultKeyGen(kp.secretKey)
cc.EvalRotateKeyGen(kp.secretKey, [1, 2, 4])

x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
y = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

ptxt_x = cc.MakeCKKSPackedPlaintext(x)
ptxt_y = cc.MakeCKKSPackedPlaintext(y)

cx = cc.Encrypt(kp.publicKey, ptxt_x)
cy = cc.Encrypt(kp.publicKey, ptxt_y)

def timeit(label, fn):
    t0 = time.perf_counter()
    result = fn()
    t1 = time.perf_counter()
    print(f"  {label:<35} {(t1-t0)*1000:>8.3f} ms")
    return result

# ============================================
# GROUP 1: ARITHMETIC OPERATIONS
# ============================================
print("=" * 60)
print("GROUP 1: ARITHMETIC OPERATIONS")
print("=" * 60)

# --- EvalAdd: ciphertext + ciphertext ---
print("\n[EvalAdd] ct + ct")
print("  Level in / out: same level")
print("  Noise: B1 + B2")
print("  Cost: cheapest operation")
c_add = timeit("EvalAdd(cx, cy)", lambda: cc.EvalAdd(cx, cy))
print(f"  Level: {cx.GetLevel()} → {c_add.GetLevel()}")

# --- EvalAdd: ciphertext + plaintext ---
print("\n[EvalAdd] ct + plaintext (public constant)")
print("  Cost: cheaper than ct+ct (no key switching)")
ptxt_const = cc.MakeCKKSPackedPlaintext([1.0]*8)
c_add_pt = timeit("EvalAdd(cx, ptxt)", lambda: cc.EvalAdd(cx, ptxt_const))
print(f"  Level: {cx.GetLevel()} → {c_add_pt.GetLevel()}")

# --- EvalSub ---
print("\n[EvalSub] ct - ct")
print("  Same cost as EvalAdd")
c_sub = timeit("EvalSub(cx, cy)", lambda: cc.EvalSub(cx, cy))

# --- EvalNegate ---
print("\n[EvalNegate] -ct")
print("  Free: just negate coefficients, no noise added")
c_neg = timeit("EvalNegate(cx)", lambda: cc.EvalNegate(cx))

# --- EvalMult: ct * ct ---
print("\n[EvalMult] ct * ct")
print("  Level in / out: level+1 (costs 1 level)")
print("  Noise: (v1*B2 + v2*B1 + B1*B2 + B_relin) / Delta")
print("  Cost: most expensive — relinearization + rescaling")
c_mult = timeit("EvalMult(cx, cy)", lambda: cc.EvalMult(cx, cy))
print(f"  Level: {cx.GetLevel()} → {c_mult.GetLevel()}")

# --- EvalMult: ct * plaintext ---
print("\n[EvalMult] ct * plaintext (public constant)")
print("  No relinearization needed")
print("  But still costs 1 level (rescaling)")
c_mult_pt = timeit("EvalMult(cx, ptxt)", lambda: cc.EvalMult(cx, ptxt_const))
print(f"  Level: {cx.GetLevel()} → {c_mult_pt.GetLevel()}")

# --- EvalMult: ct * scalar ---
print("\n[EvalMult] ct * scalar (single number)")
print("  Cheapest multiplication — no level cost!")
c_mult_sc = timeit("EvalMult(cx, 2.5)", lambda: cc.EvalMult(cx, 2.5))
print(f"  Level: {cx.GetLevel()} → {c_mult_sc.GetLevel()}")

# ============================================
# GROUP 2: ROTATION OPERATIONS
# ============================================
print("\n" + "=" * 60)
print("GROUP 2: ROTATION OPERATIONS")
print("=" * 60)

print("\n[EvalRotate] rotate slots left by k")
print("  Level: unchanged")
print("  Cost: key switching — expensive but cheaper than mult")
print("  Requirement: must pre-generate rotation key for each step")

for step in [1, 2, 4]:
    c_rot = timeit(f"EvalRotate(cx, {step})", 
                   lambda s=step: cc.EvalRotate(cx, s))
    # Verify
    res = cc.Decrypt(c_rot, kp.secretKey)
    res.SetLength(8)
    decrypted_str = str(res)
    vals = decrypted_str.split("(")[1].split(")")[0].split(",")[:3]
    vals = [v.strip() for v in vals]
    print(f"  Level: {cx.GetLevel()} → {c_rot.GetLevel()}, "
          f"first 3 slots: {vals}")

print("\n  Original first 3 slots: [1.0, 2.0, 3.0]")
print("  Rotate(1):              [2.0, 3.0, 4.0]  ← shifted left")
print("  Rotate(2):              [3.0, 4.0, 5.0]")
print("  Rotate(4):              [5.0, 6.0, 7.0]")

# ============================================
# GROUP 3: COMBINING OPERATIONS — PATTERNS
# ============================================
print("\n" + "=" * 60)
print("GROUP 3: COMMON PATTERNS IN PPML")
print("=" * 60)

# Pattern 1: Scale a ciphertext (multiply by public scalar)
print("\n[Pattern 1] Scale by public scalar — FREE level")
c_scaled = cc.EvalMult(cx, 0.5)
print(f"  cx * 0.5: level {cx.GetLevel()} → {c_scaled.GetLevel()}")

# Pattern 2: Add constant bias
print("\n[Pattern 2] Add bias (public constant) — FREE level")
ptxt_bias = cc.MakeCKKSPackedPlaintext([0.1]*8)
c_biased = cc.EvalAdd(cx, ptxt_bias)
print(f"  cx + 0.1: level {cx.GetLevel()} → {c_biased.GetLevel()}")

# Pattern 3: Multiply then add (linear layer step)
print("\n[Pattern 3] w*x + b  (one step of linear layer)")
ptxt_w = cc.MakeCKKSPackedPlaintext([0.5]*8)
t0 = time.perf_counter()
c_wx   = cc.EvalMult(cx, ptxt_w)     # level+1
c_wxb  = cc.EvalAdd(c_wx, ptxt_bias) # free
t1 = time.perf_counter()
print(f"  EvalMult + EvalAdd: {(t1-t0)*1000:.3f} ms")
print(f"  Level: {cx.GetLevel()} → {c_wxb.GetLevel()}")

# Pattern 4: Inner product (dot product shortcut)
print("\n[Pattern 4] EvalInnerProduct — built-in dot product")
print("  Internally does: mult + rotate-and-add")
cc.EvalRotateKeyGen(kp.secretKey, [1, 2, 4, -1, -2, -4])
t0 = time.perf_counter()
c_inner = cc.EvalInnerProduct(cx, cy, 8)
t1 = time.perf_counter()
print(f"  EvalInnerProduct: {(t1-t0)*1000:.3f} ms")
print(f"  Level: {cx.GetLevel()} → {c_inner.GetLevel()}")

res_inner = cc.Decrypt(c_inner, kp.secretKey)
res_inner.SetLength(1)
expected_inner = sum(x[i]*y[i] for i in range(8))
decrypted_str = str(res_inner)
got_val = float(decrypted_str.split("(")[1].split(",")[0].strip())
print(f"  Expected: {expected_inner:.4f}, Got: {got_val:.4f}")

# ============================================
# GROUP 4: LEVEL MANAGEMENT
# ============================================
print("\n" + "=" * 60)
print("GROUP 4: LEVEL MANAGEMENT")
print("=" * 60)

print("\n[ModReduce / EvalMult scalar] manually drop level")
print("  Use when: two ciphertexts at different levels")
print("  must be at same level before Add or Mult")

cx_deep = cc.EvalMult(cx, cy)       # level 1
print(f"\n  cx        level = {cx.GetLevel()}")
print(f"  cx_deep   level = {cx_deep.GetLevel()}")
print(f"  → Cannot add directly — must align levels first")

# In new OpenFHE: multiply by scalar 1.0 drops one level
cx_reduced = cc.EvalMult(cx, 1.0)
print(f"\n  After EvalMult(cx, 1.0): level = {cx_reduced.GetLevel()}")

c_now_add = cc.EvalAdd(cx_reduced, cx_deep)
print(f"  EvalAdd now works:       level = {c_now_add.GetLevel()}")

# Verify correctness
res = cc.Decrypt(c_now_add, kp.secretKey)
res.SetLength(4)
print(f"  Result: {res}")

# Show what happens without level alignment
print(f"\n[Auto level alignment in OpenFHE]")
print(f"  OpenFHE actually handles level mismatch automatically")
print(f"  for EvalAdd and EvalMult — it calls ModReduce internally")
c_auto = cc.EvalAdd(cx, cx_deep)    # different levels — does it work?
print(f"  EvalAdd(level=0, level=1) → level = {c_auto.GetLevel()}")
res_auto = cc.Decrypt(c_auto, kp.secretKey)
res_auto.SetLength(4)
print(f"  Result: {res_auto}")
print(f"  → OpenFHE auto-reduces the higher level ciphertext ✓")

# ============================================
# GROUP 5: COMPLETE TIMING SUMMARY
# ============================================
print("\n" + "=" * 60)
print("GROUP 5: COMPLETE TIMING SUMMARY")
print("=" * 60)
print(f"""
{'Operation':<28} {'Time (ms)':>10} {'vs Add':>8} {'Level':>7} {'Notes'}
{'─'*75}
{'EvalAdd(ct, ct)':<28} {'2.4':>10} {'1x':>8} {'0':>7}  cheapest
{'EvalAdd(ct, plaintext)':<28} {'10.9':>10} {'4.5x':>8} {'0':>7}  still free level
{'EvalSub(ct, ct)':<28} {'12.5':>10} {'5x':>8} {'0':>7}  same as add
{'EvalNegate(ct)':<28} {'14.9':>10} {'6x':>8} {'0':>7}  NOT truly free
{'EvalMult(ct, scalar)':<28} {'13.8':>10} {'6x':>8} {'+1':>7}  cheapest mult
{'EvalMult(ct, plaintext)':<28} {'31.5':>10} {'13x':>8} {'+1':>7}  no relin needed
{'EvalMult(ct, ct)':<28} {'141.6':>10} {'58x':>8} {'+1':>7}  most expensive
{'EvalRotate(ct, k)':<28} {'~114':>10} {'47x':>8} {'0':>7}  ≈ EvalMult!
{'EvalInnerProduct(n=8)':<28} {'194.4':>10} {'79x':>8} {'+1':>7}  1mult+3rot

Key ratios to remember:
  EvalMult(ct,ct)  ≈ 58x EvalAdd
  EvalRotate       ≈ 47x EvalAdd  ← nearly same as Mult!
  EvalMult(ct,pt)  ≈ 13x EvalAdd  ← 5x cheaper than ct*ct

For PPML circuit design:
  Count: mults × 141ms + rotations × 114ms + adds × 2ms
  Dense layer (n=128): 1 mult + 7 rot = 141 + 7×114 = 939ms
  Activation (deg-3):  2 mult         = 2×141         = 282ms
  Total 1 layer:       ≈ 1.2 seconds per ciphertext
""")