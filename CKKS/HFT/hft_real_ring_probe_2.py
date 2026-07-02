"""
hft_real_ring_probe_v2.py   (iteration 2 -- the decisive tests)
----------------------------------------------------------------------
Question left open by v1: when the real (conjugate-invariant) HFT is
factored radix-2 into butterflies, is the 'mirror' in the combine step a
CHEAP cyclic-shift automorphism (1 key) or the EXPENSIVE reversal (l/2 keys)?

We answer it three ways, with numbers, at the plaintext level (numpy only).

  PART A. Shift- vs reflection-diagonalizability.
          A transform factors into butterflies with CHEAP cyclic shifts iff
          it is diagonalized by the shift (commutes with shift up to a
          diagonal). We test this for the complex DFT and the real DCT, and
          also test the reflection. This decides the dense regime.

  PART B. Galois reality check in the conjugate-invariant ring.
          The only cheap slot-permutations are the automorphisms X->X^{5^d}
          (cyclic shifts). Conjugation X->X^{-1} is TRIVIAL there. We confirm
          the reflection is not among the cheap shifts -> stays l/2 rotations.

  PART C. Sparse regime (the actual win).
          In Zheng's sparse C2S, complex CKKS recovers the real coefficients
          via a = b + conj(b)  (one homomorphic conjugation). In the real
          ring the slots are already real, so the conjugation is removed.
          We verify both recover the coefficients exactly, and count the
          saved conjugation.
"""

import numpy as np
np.set_printoptions(precision=4, suppress=True, linewidth=120)


def offdiag_mass(M, tol=1e-9):
    """Fraction of Frobenius mass off the main diagonal. ~0 means 'diagonal'."""
    M = np.asarray(M)
    tot = np.linalg.norm(M)
    if tot < tol:
        return 0.0
    off = np.linalg.norm(M - np.diag(np.diag(M)))
    return off / tot


def nonzero_diagonals(M, tol=1e-9):
    l = M.shape[0]
    return [d for d in range(l)
            if max(abs(M[i, (i + d) % l]) for i in range(l)) > tol]


def shift_matrix(l):
    """Cyclic shift by 1: the cheap CKKS rotation (one rotation key)."""
    S = np.zeros((l, l))
    for i in range(l):
        S[i, (i + 1) % l] = 1.0
    return S


def reflection_matrix(l):
    """Reflection i -> l-1-i: the 'reversal'/mirror."""
    R = np.zeros((l, l))
    for i in range(l):
        R[i, l - 1 - i] = 1.0
    return R


def dft_matrix(l):
    j = np.arange(l)
    return np.exp(-2j * np.pi * np.outer(j, j) / l)


def dct2_matrix(l):
    """Orthonormal DCT-II: C[k,i] = a_k cos(pi (2i+1) k / (2l))."""
    k = np.arange(l)[:, None]
    i = np.arange(l)[None, :]
    C = np.cos(np.pi * (2 * i + 1) * k / (2 * l))
    a = np.full(l, np.sqrt(2.0 / l)); a[0] = np.sqrt(1.0 / l)
    return a[:, None] * C


# ----------------------------------------------------------------------
# PART A -- does the transform factor with CHEAP shifts, or need reflection?
# ----------------------------------------------------------------------
def partA():
    print("=" * 72)
    print("PART A.  Shift- vs reflection-diagonalizability")
    print("  offdiag~0  =>  transform commutes with that op up to a diagonal")
    print("            =>  butterfly factorization with THAT op is possible")
    print("=" * 72)
    print(f"\n{'l':>4} | {'DFT.shift':>10} {'DFT.reflect':>12} | {'DCT.shift':>10} {'DCT.reflect':>12}")
    print("-" * 56)
    for l in [8, 16, 32, 64]:
        W = dft_matrix(l); Wi = np.linalg.inv(W)
        C = dct2_matrix(l); Ci = np.linalg.inv(C)
        S = shift_matrix(l); R = reflection_matrix(l)
        dft_s = offdiag_mass(W @ S @ Wi)
        dft_r = offdiag_mass(W @ R @ Wi)
        dct_s = offdiag_mass(C @ S @ Ci)
        dct_r = offdiag_mass(C @ R @ Ci)
        print(f"{l:>4} | {dft_s:>10.4f} {dft_r:>12.4f} | {dct_s:>10.4f} {dct_r:>12.4f}")
    print("\nReading (expected):")
    print("  DFT pairs with the SHIFT (DFT.shift ~ 0)   -> cheap butterflies, O(log l).")
    print("  DCT pairs with the REFLECTION (DCT.reflect ~ 0) -> its natural cheap")
    print("  operation is the reflection, NOT the shift. And the reflection is the")
    print("  expensive reversal in CKKS. So the dense real DCT-HFT does NOT inherit")
    print("  a cheap O(log l) butterfly: the W8 obstruction is INTRINSIC, not removed.")


# ----------------------------------------------------------------------
# PART B -- Galois reality check in the conjugate-invariant ring
# ----------------------------------------------------------------------
def partB():
    print("\n" + "=" * 72)
    print("PART B.  Galois reality check (conjugate-invariant ring)")
    print("=" * 72)
    # Real slots are indexed by exponents 5^d mod 2N == {4j+1}. sigma_{5^d} is a
    # cyclic shift by d on those slots; sigma_{-1} (conjugation) is the identity
    # on the real ring (elements satisfy a(X)=a(X^-1)). We confirm the reflection
    # is not realizable as a single cheap shift.
    for l in [16, 64]:
        S = shift_matrix(l); R = reflection_matrix(l)
        # cheap automorphisms available = all cyclic shifts S^d
        shift_rotations = len(nonzero_diagonals(S))           # = 1
        reflect_rotations = len(nonzero_diagonals(R))         # = l/2
        print(f"  l={l:>3}:  cyclic shift sigma_5  -> {shift_rotations} rotation key"
              f"   |   reflection (mirror) -> {reflect_rotations} rotation keys")
    print("\n  Conjugation X->X^-1 in the real ring: acts as IDENTITY on slots")
    print("  (so the b+conj(b) step of complex C2S costs literally nothing here).")
    print("  Reflection is NOT a cyclic shift -> not a cheap automorphism -> the")
    print("  fast-DCT mirror stays at l/2 rotations. Confirms PART A from algebra.")


# ----------------------------------------------------------------------
# PART C -- the sparse regime: real ring removes the conjugation (the win)
# ----------------------------------------------------------------------
def partC():
    print("\n" + "=" * 72)
    print("PART C.  Sparse-regime C2S: real ring removes the conjugation")
    print("=" * 72)
    rng = np.random.default_rng(1)

    # --- complex CKKS sparse C2S: recover real coeffs a from slots z = U a ---
    # U is the (n/2 x n) complex Fourier-type matrix; a is real of length n.
    n = 16
    half = n // 2
    xi = np.exp(-1j * np.pi / n)                     # primitive 2n-th root
    idx = [pow(5, j, 2 * n) for j in range(half)]    # 5^j slot indexing
    U = np.array([[ (xi ** idx[j]) ** col for col in range(n)] for j in range(half)])
    a = rng.integers(-20, 20, size=n).astype(float)  # real coefficients
    z = U @ a                                         # complex slots
    # Zheng's recovery:  b = (1/n) conj(U)^T z ;  a_rec = b + conj(b)
    b = (1.0 / n) * (U.conj().T @ z)
    a_rec_complex = b + b.conj()
    ok_complex = np.allclose(a_rec_complex.imag, 0) and np.allclose(a_rec_complex.real, a)
    print(f"\n  COMPLEX ring (n={n}): a recovered exactly = {ok_complex}")
    print(f"     -> uses 1 homomorphic CONJUGATION (the b + conj(b) step)")

    # --- real (conjugate-invariant) ring: slots already real, no conjugation ---
    # z_real = C b  with C real (DCT); recover b = C^{-1} z_real, real linear map.
    C = dct2_matrix(half)
    b_real = rng.integers(-20, 20, size=half).astype(float)
    z_real = C @ b_real
    b_rec = np.linalg.solve(C, z_real)
    ok_real = np.allclose(z_real.imag if np.iscomplexobj(z_real) else 0, 0) \
              and np.allclose(b_rec, b_real)
    print(f"\n  REAL ring  (n/2={half}): b recovered exactly = {ok_real}, slots real = {np.isrealobj(z_real)}")
    print(f"     -> uses 0 homomorphic conjugations (slots already real)")
    print("\n  Net: in the SPARSE regime (Zheng depth-1, no butterfly, no reflection),")
    print("  porting to the real ring is sound and SAVES one conjugation per C2S,")
    print("  on top of Kim-Song's 2x packing. This is the regime where the")
    print("  'sparse, real-aware' contribution actually lives.")


if __name__ == "__main__":
    partA()
    partB()
    partC()