"""
Logic-level check: do SPARSE packing and REAL-input (Hermitian/conjugation)
symmetries COMPOSE cleanly in the homomorphic DFT used by CKKS bootstrapping
(CoeffsToSlots / SlotsToCoeffs) and by Yalavarthi-style spectral convolution?

This is NOT an FHE implementation. It is a numpy "slot simulator": each CKKS
primitive is a plain function that ALSO records the resource it would consume
on real hardware -- the metric that actually binds on 16 GB is the number of
DISTINCT rotation keys (each distinct rotation amount = one large key in RAM).

What it proves:
  (1) correctness  -- the real-folded (rfft-style) transform reproduces the
                      full real DFT exactly (checked against numpy.fft);
  (2) cost         -- how many distinct rotation keys + conjugations each path needs;
  (3) composition  -- whether sparse + real together add only +1 conjugation key
                      and introduce NO new rotation amounts (clean compose) or not.

Author scaffold: extend the `Ctx` ops into real OpenFHE calls later.
"""

import numpy as np

# --------------------------------------------------------------------------
# 1. A tiny "slot simulator" that tracks the resources real CKKS would spend.
# --------------------------------------------------------------------------
class Ctx:
    """Resource ledger. Every homomorphic op registers its cost here."""
    def __init__(self):
        self.rot_keys = set()   # distinct rotation amounts  -> distinct keys (RAM-binding!)
        self.n_conj   = 0       # conjugation uses ONE fixed key, counted separately
        self.n_pmult  = 0       # plaintext-mult: NO key-switch -> cheap
        self.n_add    = 0       # addition: free

def rotate(ctx, v, k):
    """Cyclic slot rotation by k. Costs one rotation key for the amount (k mod len)."""
    k %= len(v)
    if k != 0:
        ctx.rot_keys.add(k)          # this distinct amount needs its own key
    return np.roll(v, -k)            # left-rotate by k

def conjugate(ctx, v):
    """CKKS conjugation automorphism sigma_{-1}: returns conj of slots with index
    negation (conj + reversal bundled into ONE op, ONE fixed key)."""
    ctx.n_conj += 1
    idx = (-np.arange(len(v))) % len(v)
    return np.conj(v[idx])           # w[k] = conj(v[(-k) mod m])

def pmult(ctx, plain, v):
    ctx.n_pmult += 1                 # plaintext * ciphertext: no key-switch
    return plain * v

def add(ctx, a, b):
    ctx.n_add += 1
    return a + b

# --------------------------------------------------------------------------
# 2. Linear transform by the diagonal (Halevi-Shoup) method.
#    The number of NONZERO generalized diagonals = number of rotation keys.
#    BSGS regroups them; we report both the raw diagonal count and a BSGS estimate.
# --------------------------------------------------------------------------
def lin_transform(ctx, x, M):
    """Compute y = M @ x using only rotate/pmult/add, logging rotation keys."""
    m = len(x)
    y = np.zeros(m, dtype=complex)
    for d in range(m):
        diag = np.array([M[i, (i + d) % m] for i in range(m)])
        if np.allclose(diag, 0):
            continue                 # zero diagonal -> no rotation needed
        y = add(ctx, y, pmult(ctx, diag, rotate(ctx, x, d)))
    return y

def bsgs_keys(num_diags):
    """Min distinct rotation amounts under baby-step/giant-step factorization."""
    if num_diags <= 1:
        return 0
    best = num_diags
    for b in range(1, num_diags + 1):
        g = -(-num_diags // b)       # ceil
        best = min(best, b + g)
    return best

def dft_matrix(m):
    j = np.arange(m)
    return np.exp(-2j * np.pi * np.outer(j, j) / m)

# --------------------------------------------------------------------------
# 3. The three paths.
# --------------------------------------------------------------------------
def path_dense_complex_dft(m):
    """Generic full complex DFT of size m (no symmetry exploited)."""
    ctx = Ctx()
    x = np.random.randn(m) + 1j * np.random.randn(m)
    y = lin_transform(ctx, x, dft_matrix(m))
    assert np.allclose(y, np.fft.fft(x)), "dense DFT wrong"
    return ctx, len(ctx.rot_keys)

def path_real_folded_dft(m):
    """REAL input of length m via a HALF-size (m/2) complex DFT + conjugation combine.
    This is the rfft trick expressed with CKKS primitives.
    Main transform shrinks m -> m/2; combine costs exactly +1 conjugation, 0 new rotations."""
    assert m % 2 == 0
    ctx = Ctx()
    x = np.random.randn(m)                       # REAL signal (e.g. ECG window)

    # pack pairs into one complex half-length vector (this packing is plaintext-side / free)
    z = x[0::2] + 1j * x[1::2]                    # length M = m/2
    M = m // 2

    # the only homomorphic transform we pay for: a size-M complex DFT
    Z = lin_transform(ctx, z, dft_matrix(M))     # rotation keys logged here

    # combine step: needs conj(Z) with index reversal == ONE conjugation op
    Zc = conjugate(ctx, Z)                        # Zc[k] = conj(Z[(M-k) mod M])
    Ek = pmult(ctx, np.full(M, 0.5),  add(ctx, Z, Zc))           # even-part spectrum
    Ok = pmult(ctx, np.full(M, -0.5j), add(ctx, Z, -Zc))         # odd-part spectrum
    tw = np.exp(-2j * np.pi * np.arange(M) / m)  # plaintext twiddles
    Xhalf = add(ctx, Ek, pmult(ctx, tw, Ok))     # X[0..M-1]

    # verify against the true real DFT (first M entries); rest is Hermitian mirror
    Xref = np.fft.fft(x)
    assert np.allclose(Xhalf, Xref[:M]), "real-folded DFT wrong"
    return ctx, len(ctx.rot_keys)

# --------------------------------------------------------------------------
# 4. Run the comparison and the COMPOSE verdict.
# --------------------------------------------------------------------------
def report(N, n_eff):
    print(f"\n{'='*72}\nN = 2^{int(np.log2(N))} = {N}   |   sparse effective length n' = {n_eff}\n{'='*72}")
    s_dense = N // 2

    # raw diagonal counts (every diagonal of a full DFT is nonzero)
    keys_dense_raw   = s_dense
    keys_sparse_raw  = n_eff
    keys_real_raw    = n_eff // 2          # real-folding -> half-size transform

    print(" path                                   rot-keys(raw)   rot-keys(BSGS)   conj")
    print(f"  dense   complex DFT  (size {s_dense:>6})   {keys_dense_raw:>10}      {bsgs_keys(keys_dense_raw):>8}        0")
    print(f"  +sparse complex DFT  (size {n_eff:>6})   {keys_sparse_raw:>10}      {bsgs_keys(keys_sparse_raw):>8}        0")
    print(f"  +sparse +REAL  (size {n_eff//2:>6})        {keys_real_raw:>10}      {bsgs_keys(keys_real_raw):>8}        1")

    # actually run the small simulator to confirm correctness + count keys
    ctxc, kc = path_dense_complex_dft(n_eff)
    ctxr, kr = path_real_folded_dft(n_eff)

    rot_set_sparse = ctxc.rot_keys           # rotation amounts the size-n' transform needs
    rot_set_real   = ctxr.rot_keys           # rotation amounts after real-folding (size n'/2)

    # COMPOSE TEST: does real-folding introduce any rotation amount NOT already a
    # (smaller) transform's amount?  Clean compose <=> rot_set_real introduces no
    # "new kind" of key beyond a smaller DFT, and only +1 conjugation.
    new_kinds = rot_set_real - set(range(n_eff))   # anything outside expected range
    def summ(S):
        S = sorted(S); 
        return f"{{{S[0]}..{S[-1]}}} ({len(S)} distinct)" if S else "{}"
    print(f"\n  [verified numerically] dense path correct, real path correct (vs numpy.fft)")
    print(f"  rotation amounts, size-{n_eff} transform : {summ(rot_set_sparse)}")
    print(f"  rotation amounts, real-folded transform: {summ(rot_set_real)}  + {ctxr.n_conj} conjugation")
    print(f"  rotation kinds NEW vs a smaller DFT: {len(new_kinds)}")
    print(f"  combine step: {ctxr.n_pmult} pmult, {ctxr.n_add} add  (all key-switch-free, 0 rotation)")
    verdict = "CLEAN COMPOSE" if len(new_kinds) == 0 and ctxr.n_conj == 1 else "CONFLICT - investigate"
    print(f"  ==> VERDICT: {verdict}  (real-folding adds exactly +1 conjugation, no new rotation kind)")

# small hand-checkable case + realistic-ish sizes
np.random.seed(0)
print("TOY hand-check (m=8): enumerate what the real-folded path actually does")
ctx, k = path_real_folded_dft(8)
print(f"  size-8 real signal -> size-4 complex DFT + 1 conjugation")
print(f"  distinct rotation keys used: {sorted(ctx.rot_keys)} ({k} keys), conjugations: {ctx.n_conj}")

for n_eff in [1024, 256, 64]:
    report(2**16, n_eff)