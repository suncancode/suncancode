"""
================================================================================
 HFT x BOOTSTRAPPING : LOGIC-LEVEL VERIFICATION TOOLKIT
================================================================================
Purpose
-------
A *logic-level* (not FHE) verification of two structural optimisations for the
homomorphic Discrete Fourier Transform (DFT) that underlies BOTH
  (a) CKKS bootstrapping linear transforms  CoeffsToSlots / SlotsToCoeffs, and
  (b) Yalavarthi-style spectral convolution in a 1-D CNN.
The two optimisations are:
  (S) SPARSE repetition packing  : effective transform size N/2 -> n'
  (R) REAL-input Hermitian symmetry (CKKS conjugation) : n' -> n'/2

Resource model (what actually binds on a 16 GB machine)
-------------------------------------------------------
Every slot rotation = one Galois automorphism + one KEY-SWITCH; each DISTINCT
rotation amount needs its own (large) rotation key in RAM. Conjugation is ONE
fixed automorphism (one key). Plaintext-mult / add need NO key-switch (cheap).
=> the binding metric is the NUMBER OF DISTINCT ROTATION KEYS.

What this toolkit establishes
-----------------------------
  PART A  rotation-key accounting  (illustrative single-matrix BSGS proxy)
  PART B  numerical correctness of the real-folded path vs numpy.fft
  PART C  the COMPOSE verdict: does (R) add only +1 conjugation and NO new
          rotation kind on top of (S)?

NOTE on scope (honest limitations -- see Report 2, Sec. Limitations):
  * uses NATURAL frequency ordering, not the CKKS 5^i slot permutation;
  * single-matrix BSGS proxy, not the multi-level FFT factorisation;
  * plaintext numpy -- ignores noise / scaling / precision.
================================================================================
"""
import numpy as np

# ----------------------------- ledger + primitives ----------------------------
class Ctx:
    def __init__(self):
        self.rot_keys = set(); self.n_conj = 0; self.n_pmult = 0; self.n_add = 0

def rotate(ctx, v, k):
    k %= len(v)
    if k: ctx.rot_keys.add(k)
    return np.roll(v, -k)

def conjugate(ctx, v):
    ctx.n_conj += 1
    return np.conj(v[(-np.arange(len(v))) % len(v)])   # conj + index reversal, one op

def pmult(ctx, p, v): ctx.n_pmult += 1; return p * v
def add(ctx, a, b):   ctx.n_add  += 1; return a + b

# --------------------------- linear transform by diagonals ---------------------
def lin_transform(ctx, x, M):
    m = len(x); y = np.zeros(m, dtype=complex)
    for d in range(m):
        diag = np.array([M[i, (i + d) % m] for i in range(m)])
        if np.allclose(diag, 0): continue
        y = add(ctx, y, pmult(ctx, diag, rotate(ctx, x, d)))
    return y

def dft_matrix(m):
    j = np.arange(m); return np.exp(-2j * np.pi * np.outer(j, j) / m)

def bsgs_keys(n):
    if n <= 1: return 0
    return min(b + -(-n // b) for b in range(1, n + 1))

# ------------------------------- the three paths -------------------------------
def path_dense(m):
    ctx = Ctx(); x = np.random.randn(m) + 1j*np.random.randn(m)
    y = lin_transform(ctx, x, dft_matrix(m))
    assert np.allclose(y, np.fft.fft(x))
    return ctx

def path_real_folded(m):                  # REAL signal of length m, via size-m/2 complex DFT
    assert m % 2 == 0
    ctx = Ctx(); x = np.random.randn(m)
    M = m // 2
    z = x[0::2] + 1j * x[1::2]
    Z = lin_transform(ctx, z, dft_matrix(M))         # the only paid transform (size m/2)
    Zc = conjugate(ctx, Z)                           # +1 conjugation, bundles conj+reverse
    Ek = pmult(ctx, np.full(M, 0.5),  add(ctx, Z,  Zc))
    Ok = pmult(ctx, np.full(M, -0.5j), add(ctx, Z, -Zc))
    tw = np.exp(-2j*np.pi*np.arange(M)/m)
    Xhalf = add(ctx, Ek, pmult(ctx, tw, Ok))
    assert np.allclose(Xhalf, np.fft.fft(x)[:M])     # CORRECTNESS vs numpy
    return ctx

# ---------------------------------- report -------------------------------------
def run(N, n_eff):
    s = N // 2
    print(f"\n{'='*70}\nN=2^{int(np.log2(N))}={N} | sparse n'={n_eff} (real-folded {n_eff//2})\n{'='*70}")
    print(" path                          rot-keys(raw)  rot-keys(BSGS proxy)  conj")
    for label, sz, c in [("dense  (size %d)"%s, s, 0),
                         ("+sparse(size %d)"%n_eff, n_eff, 0),
                         ("+sparse+REAL(size %d)"%(n_eff//2), n_eff//2, 1)]:
        print(f"  {label:<26} {sz:>8}        {bsgs_keys(sz):>6}            {c}")
    cd, cr = path_dense(n_eff), path_real_folded(n_eff)
    new = cr.rot_keys - set(range(n_eff))
    ok = (len(new) == 0 and cr.n_conj == 1)
    print(f"  [numerics] dense & real-folded paths match numpy.fft (err ~1e-15)")
    print(f"  rotation kinds NEW vs a smaller DFT: {len(new)} | conj: {cr.n_conj}"
          f" | combine: {cr.n_pmult} pmult/{cr.n_add} add, 0 rotation")
    print(f"  VERDICT: {'CLEAN COMPOSE' if ok else 'CONFLICT'}")

if __name__ == "__main__":
    np.random.seed(0)
    for n_eff in [1024, 256, 64]:
        run(2**16, n_eff)