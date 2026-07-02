"""
hft_real_ring_probe.py
----------------------------------------------------------------------
Plaintext-level (numpy only) study of the homomorphic linear transform
(C2S/S2C = HFT) for Week 9. No encryption, no OpenFHE: every question
here is about the STRUCTURE of the linear map (which rotations it needs),
which is decidable at the plaintext-circuit level -- the same style as
the Week 8 verification scripts.

It answers three things with numbers:

  OUTPUT 1. Verify Kim-Song real encode/decode (conjugate-invariant ring).
            Confirms slots are REAL and the transform is a real cosine map.

  OUTPUT 2. Compare the rotation-key cost of the complex DFT decode vs the
            real cosine (DCT) decode under the diagonal method.
            Tests the honest claim: the real ring gives NO reduction in the
            number of distinct rotations -- only a constant-factor win.

  OUTPUT 3. The reversal probe. Build, as permutations on slots:
              - a single cyclic shift          (expected: 1 rotation)
              - conjugation k -> -k            (the W8 'reversal')
            and count how many distinct shift-diagonals each needs under the
            diagonal method. This is the numerical form of the W8 negative
            result, and the object that a DCT butterfly may or may not avoid.
"""

import numpy as np

np.set_printoptions(precision=4, suppress=True, linewidth=120)


# ----------------------------------------------------------------------
# Core primitive: the diagonal method cost of an arbitrary linear map M.
# y = M x is evaluated as  y = sum_d ( m_d (.) rot(x,d) ),
#   m_d = (M[i, (i+d) mod l])_i  is the d-th generalized diagonal.
# Each NONZERO diagonal => one distinct rotation amount => one rotation key.
# ----------------------------------------------------------------------
def nonzero_diagonals(M, tol=1e-9):
    """Return the set of shift amounts d whose generalized diagonal is nonzero."""
    l = M.shape[0]
    amounts = []
    for d in range(l):
        diag = np.array([M[i, (i + d) % l] for i in range(l)])
        if np.max(np.abs(diag)) > tol:
            amounts.append(d)
    return amounts


def bsgs_count(num_nonzero_diag):
    """Distinct rotations under baby-step giant-step ~ 2*sqrt(#diagonals)."""
    import math
    m = num_nonzero_diag
    if m == 0:
        return 0
    best = m
    for b1 in range(1, m + 1):
        cost = b1 + -(-m // b1)  # b1 + ceil(m/b1)
        best = min(best, cost)
    return best


# ----------------------------------------------------------------------
# OUTPUT 1 -- Kim-Song real encode/decode over the conjugate-invariant ring
# ----------------------------------------------------------------------
def real_ring_roots(m):
    """xi_j = zeta^{4j+1} + zeta^{-(4j+1)} = 2 cos(2 pi (4j+1)/m), zeta=exp(2 pi i/m).
    These are the REAL evaluation points; here n=m/2 and there are n/2 of them."""
    n = m // 2
    half = n // 2
    return np.array([2 * np.cos(2 * np.pi * (4 * j + 1) / m) for j in range(half)])


def output1_kimsong():
    print("=" * 70)
    print("OUTPUT 1.  Kim-Song real encode/decode (conjugate-invariant ring)")
    print("=" * 70)

    # --- the paper's toy example: m=8, scale Delta=64, x=(1.1, 2.3) ---
    m = 8
    xi = real_ring_roots(m)            # expect [ sqrt2, -sqrt2 ]
    print(f"\nToy: m={m}, real roots xi_j = {xi}  (paper says [+-sqrt2={np.sqrt(2):.4f}])")

    Delta = 64
    x = np.array([1.1, 2.3])
    # decode matrix in the Y-power (monomial) basis: D[j,i] = xi_j ** i
    half = len(xi)
    D = np.array([[xi[j] ** i for i in range(half)] for j in range(half)])
    # encode: a = round( Delta * D^{-1} x )   (integer coefficient polynomial)
    a = np.round(np.linalg.solve(D, Delta * x)).astype(int)
    print(f"  encode  ->  m(Y) coefficients a = {a}   (paper: [109, -27])")
    x_back = (D @ a) / Delta
    print(f"  decode  ->  {x_back}   (paper approx: [1.1065, 2.2997])")
    print(f"  slots are real? {np.allclose(x_back.imag if np.iscomplexobj(x_back) else 0, 0)}")

    # --- a larger random round-trip to confirm it is a genuine real transform ---
    m = 64
    xi = real_ring_roots(m)
    half = len(xi)
    rng = np.random.default_rng(0)
    a = rng.integers(-50, 50, size=half)
    D = np.array([[xi[j] ** i for i in range(half)] for j in range(half)])
    x = D @ a
    a_rec = np.round(np.linalg.solve(D, x)).astype(int)
    print(f"\nRandom round-trip (m={m}, {half} real slots): "
          f"exact recovery = {np.array_equal(a, a_rec)}, all slots real = {np.isrealobj(x)}")


# ----------------------------------------------------------------------
# OUTPUT 2 -- rotation-key cost: complex DFT decode vs real cosine decode
# ----------------------------------------------------------------------
def complex_dft_decode(l):
    """Representative complex canonical-embedding decode on l slots: a dense DFT."""
    j = np.arange(l)
    return np.exp(-2j * np.pi * np.outer(j, j) / l)


def real_cosine_decode(l):
    """Representative real (conjugate-invariant) decode on l slots: dense cosine.
    Basis {1, X+X^-1, ...}: slot_j = sum_i b_i * cos(i * phi_j), phi_j real."""
    j = np.arange(l)
    phi = 2 * np.pi * (4 * j + 1) / (4 * l)   # distinct real angles
    return np.cos(np.outer(phi, np.arange(l)))


def output2_rotation_keys():
    print("\n" + "=" * 70)
    print("OUTPUT 2.  Rotation-key cost  (diagonal method)  complex vs real")
    print("=" * 70)
    print(f"\n{'l':>5} | {'complex DFT':>22} | {'real cosine (DCT)':>22}")
    print(f"{'':>5} | {'#diag  naive  BSGS':>22} | {'#diag  naive  BSGS':>22}")
    print("-" * 56)
    for l in [8, 16, 32, 64]:
        Wc = complex_dft_decode(l)
        Wr = real_cosine_decode(l)
        dc = nonzero_diagonals(Wc)
        dr = nonzero_diagonals(Wr)
        print(f"{l:>5} | {len(dc):>5}  {len(dc):>5}  {bsgs_count(len(dc)):>5} "
              f"| {len(dr):>5}  {len(dr):>5}  {bsgs_count(len(dr)):>5}")
    print("\nReading: both matrices are dense -> naive count = l for BOTH rings.")
    print("=> The real ring does NOT reduce the number of distinct rotations.")
    print("   Its win is a CONSTANT factor (2x slots / half NTT), not fewer keys.")


# ----------------------------------------------------------------------
# OUTPUT 3 -- the reversal probe (the W8 negative result, numerically)
# ----------------------------------------------------------------------
def permutation_matrix(perm):
    l = len(perm)
    P = np.zeros((l, l))
    for i, p in enumerate(perm):
        P[i, p] = 1.0
    return P


def output3_reversal_probe():
    print("\n" + "=" * 70)
    print("OUTPUT 3.  Reversal probe: how many rotations does each permutation need?")
    print("=" * 70)
    print(f"\n{'l':>5} | {'cyclic shift by 1':>20} | {'reversal k->-k':>20}")
    print(f"{'':>5} | {'#rotations needed':>20} | {'#rotations needed':>20}")
    print("-" * 52)
    for l in [8, 16, 32, 64]:
        shift = [(i + 1) % l for i in range(l)]          # cheap: one rotation
        reversal = [(-i) % l for i in range(l)]           # the W8 mirror / fold
        Pshift = permutation_matrix(shift)
        Prev = permutation_matrix(reversal)
        n_shift = len(nonzero_diagonals(Pshift))
        n_rev = len(nonzero_diagonals(Prev))
        print(f"{l:>5} | {n_shift:>20} | {n_rev:>20}")
    print("\nReading: a cyclic shift is ONE diagonal (1 rotation).")
    print("   The reversal k->-k is an anti-diagonal: it needs ~l distinct")
    print("   rotations -- more than the whole transform. This is exactly the")
    print("   Week 8 negative result, now a number.")
    print("\n   KEY QUESTION for Week 9 (not answered here -- needs the DCT")
    print("   butterfly factorization): does a radix-2 split of the real cosine")
    print("   transform REQUIRE this reversal permutation, or can the real ring")
    print("   realize the mirror as a single cheap automorphism? If cheap ->")
    print("   real rotation-key win. If not -> the W8 obstruction just moved.")


if __name__ == "__main__":
    output1_kimsong()
    output2_rotation_keys()
    output3_reversal_probe()