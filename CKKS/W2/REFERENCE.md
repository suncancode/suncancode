# OpenFHE CKKS Reference Sheet

## Parameters

| Parameter         | Formula                        | Trade-off                        |
|-------------------|--------------------------------|----------------------------------|
| MultiplicativeDepth | = number of ct*ct mults       | ↑ depth → ↑ N → 2x slower       |
| ScalingModSize    | = bits of Δ = 2^ScalingModSize | ↑ scale → ↑ precision → ↑ N     |
| BatchSize         | = slots to use (≤ N/2)         | no speed effect, pack more data  |

## Parameter Selection
  target_precision ≥ 20 bits for ML
  ScalingModSize ≥ 6 + 4×depth + 20
  For depth > 10: must use bootstrapping

## Timing (N=32768, measured)
  EvalAdd(ct, ct)          ~10ms   level: 0   noise: B1+B2
  EvalAdd(ct, plaintext)   ~23ms   level: 0   noise: B1
  EvalSub(ct, ct)          ~19ms   level: 0   noise: B1+B2
  EvalNegate(ct)           ~10ms   level: 0   noise: B1
  EvalMult(ct, scalar)     ~17ms   level: +1  noise: ~B1
  EvalMult(ct, plaintext)  ~27ms   level: +1  noise: moderate
  EvalMult(ct, ct)        ~161ms   level: +1  noise: high
  EvalRotate(ct, k)        ~72ms   level:  0  noise: ~B1
  EvalInnerProduct(n=8)   ~180ms   level: +1

## Key Ratios
  EvalMult(ct,ct)  ≈ 16x EvalAdd
  EvalRotate       ≈  7x EvalAdd  ← nearly same as Mult!
  EvalMult(ct,pt)  ≈  3x EvalAdd

## Required Enables per Operation
  PKE:          KeyGen, Encrypt, Decrypt
  LEVELEDSHE:   EvalAdd, EvalMult, EvalRotate, EvalSub
  ADVANCEDSHE:  EvalInnerProduct, EvalSum

## Required Key Generation
  EvalMultKeyGen(sk)          → for EvalMult(ct,ct)
  EvalRotateKeyGen(sk, steps) → for EvalRotate, EvalInnerProduct
  EvalSumKeyGen(sk)           → for EvalSum

## Circuit Cost Estimation
  Dense layer (n=128): 1 mult + 7 rot = 161 + 7×72  = 665ms
  Poly activation d=3: 2 mult         = 2×161        = 322ms
  Poly activation d=7: 4 mult         = 4×161        = 644ms
  Full layer (w/ act): 3-5 mult + 7 rot               ≈ 1.2s

## Precision Budget
  Start (ScalingModSize=50):  50 bits
  After encrypt:              44 bits  (-6)
  Per multiplication:         -4 bits
  Formula: final = 50 - 6 - 4×depth
  depth=1:  40 bits (~12 decimal digits)  ✓
  depth=5:  24 bits (~7 decimal digits)   ✓
  depth=10:  4 bits (~1 decimal digit)    ✗ need bootstrapping
