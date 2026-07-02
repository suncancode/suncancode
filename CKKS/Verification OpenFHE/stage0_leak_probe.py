"""
Stage 0 probe -- stage0_leak_probe.py
Reproduce the Li--Micciancio key-recovery leak of CKKS at the Ring-LWE level,
in a self-contained plaintext simulation (numpy only, no OpenFHE).

Structure (each part self-verifies before the next is trusted):
  Part A : build and self-test the ring R_q = Z_q[X]/(X^N + 1)
  Part B : minimal symmetric RLWE encrypt/decrypt; verify Dec(ct) = pt + e
  Part C : the attack -- recover the secret key s from a SINGLE decryption

Convention (matching the OpenFHE / Guo et al. description):
  ciphertext  ct = (c0, c1),  c0 = -a*s + pt + e (mod q),  c1 = a
  decryption  Dec(ct) = c0 + c1*s (mod q) = pt + e   (centered into (-q/2, q/2])

The leak: an adversary holding the ciphertext ct = (c0, c1) and the observed
decryption d = pt + e forms  t = d - c0 = c1*s (mod q).  Multiplication by c1
is a linear map over Z_q, so this is one N x N linear system in s; if c1 is
invertible, a single decryption recovers s exactly.  Note that the KEY recovery
needs only (c0, c1, d) -- not pt or e, which cancel in t.
"""

import numpy as np

# ----------------------------------------------------------------------
# Parameters (toy, for exact verification; N, Q may be increased freely)
# ----------------------------------------------------------------------
N     = 16          # ring degree, power of two   (slots = N/2 in Step 2)
Q     = 65537       # prime modulus (Fermat inverse for the GF(Q) solve)
SIGMA = 3.2         # RLWE error standard deviation (standard CKKS value)
SEED  = 2025
rng = np.random.default_rng(SEED)


def center(x):
    """Center coefficients of an integer array into (-Q/2, Q/2]."""
    x = np.asarray(x) % Q
    return np.where(x > Q // 2, x - Q, x).astype(np.int64)


# ----------------------------------------------------------------------
# Part A : ring R_q = Z_q[X] / (X^N + 1)
# ----------------------------------------------------------------------
def ring_mult(a, b):
    """Negacyclic polynomial multiplication mod (X^N + 1), coefficients mod Q."""
    a = np.asarray(a, dtype=np.int64)
    b = np.asarray(b, dtype=np.int64)
    full = np.convolve(a, b)                  # length 2N-1
    cc = np.zeros(2 * N, dtype=np.int64)
    cc[:full.size] = full
    res = cc[:N] - cc[N:2 * N]                # X^{N+r} = -X^r  (negacyclic fold)
    return res % Q


def neg_matrix(a):
    """Matrix A with (a * s mod (X^N+1)) = A @ s (mod Q), built column by column."""
    A = np.zeros((N, N), dtype=np.int64)
    for j in range(N):
        ej = np.zeros(N, dtype=np.int64)
        ej[j] = 1
        A[:, j] = ring_mult(a, ej)
    return A % Q


def selftest_ring():
    # (i) X^{N-1} * X = X^N = -1
    xNm1 = np.zeros(N, dtype=np.int64); xNm1[N - 1] = 1
    x1   = np.zeros(N, dtype=np.int64); x1[1] = 1
    prod = ring_mult(xNm1, x1)
    assert np.array_equal(center(prod), center([-1] + [0] * (N - 1))), "X^N != -1"
    # (ii) matrix form agrees with polynomial multiplication
    for _ in range(20):
        a = rng.integers(0, Q, N); s = rng.integers(0, Q, N)
        assert np.array_equal(ring_mult(a, s), (neg_matrix(a) @ s) % Q), "matrix != polymul"
    # (iii) associativity
    for _ in range(20):
        a, b, c = (rng.integers(0, Q, N) for _ in range(3))
        assert np.array_equal(ring_mult(ring_mult(a, b), c),
                              ring_mult(a, ring_mult(b, c))), "associativity fail"
    print("[Part A] ring R_q self-tests PASS  "
          "(X^N = -1, neg_matrix == polymul, associativity; exact over Z_q)")


# ----------------------------------------------------------------------
# Part B : minimal symmetric RLWE encryption / decryption
# ----------------------------------------------------------------------
def keygen(hamming=None):
    """Ternary secret in {-1,0,1}^N (uniform, or sparse with given Hamming weight)."""
    if hamming is None:
        return rng.integers(-1, 2, N).astype(np.int64)
    s = np.zeros(N, dtype=np.int64)
    idx = rng.choice(N, size=hamming, replace=False)
    s[idx] = rng.choice([-1, 1], size=hamming)
    return s


def sample_error():
    return np.rint(rng.normal(0.0, SIGMA, N)).astype(np.int64)


def encrypt(pt, s):
    """ct = (c0, c1) with c0 = -a*s + pt + e (mod Q), c1 = a (uniform)."""
    a = rng.integers(0, Q, N).astype(np.int64)
    e = sample_error()
    c0 = (-ring_mult(a, s) + pt + e) % Q
    return (c0, a), e


def decrypt(ct, s):
    c0, c1 = ct
    return center((c0 + ring_mult(c1, s)) % Q)


def selftest_encdec():
    s  = keygen()
    pt = rng.integers(-100, 101, N).astype(np.int64)      # a representative plaintext
    ct, e = encrypt(pt, s)
    d  = decrypt(ct, s)
    assert np.array_equal(d, center(pt + e)), "Dec(ct) != pt + e"
    assert np.array_equal(center(d - pt), center(e)), "recovered error != injected error"
    print("[Part B] enc/dec PASS  "
          "(Dec(ct) = pt + e exactly; ||e||_inf = %d)" % int(np.max(np.abs(center(e)))))


# ----------------------------------------------------------------------
# Part C : the attack -- recover s from a single decryption
# ----------------------------------------------------------------------
def gauss_solve_modp(A, b, p):
    """Solve A x = b over GF(p), p prime. Returns x, or None if A is singular mod p."""
    A = (A % p).astype(object).copy()        # python ints -> no overflow in elimination
    b = (b % p).astype(object).copy()
    n = A.shape[0]
    for col in range(n):
        piv = next((r for r in range(col, n) if A[r, col] % p != 0), None)
        if piv is None:
            return None
        A[[col, piv]] = A[[piv, col]]; b[[col, piv]] = b[[piv, col]]
        inv = pow(int(A[col, col]), p - 2, p)
        A[col] = (A[col] * inv) % p; b[col] = (b[col] * inv) % p
        for r in range(n):
            if r != col and A[r, col] % p != 0:
                f = A[r, col]
                A[r] = (A[r] - f * A[col]) % p
                b[r] = (b[r] - f * b[col]) % p
    return np.array([int(v) for v in b], dtype=np.int64) % p


def attack(ct, d):
    """Adversary uses ONLY the ciphertext ct=(c0,c1) and the observed decryption d.
       It does not use the secret s, nor even the plaintext pt."""
    c0, c1 = ct
    t = (d - c0) % Q                          # linear relation: c1 * s = d - c0 (mod Q)
    x = gauss_solve_modp(neg_matrix(c1), t, Q)
    return None if x is None else center(x)


def run_attack():
    s  = keygen()
    pt = rng.integers(-100, 101, N).astype(np.int64)
    ct, e = encrypt(pt, s)
    d  = decrypt(ct, s)                        # the value the honest user would release

    tries = 1
    s_hat = attack(ct, d)
    while s_hat is None:                       # c1 non-invertible mod Q (rare): fresh randomness
        ct, e = encrypt(pt, s); d = decrypt(ct, s); tries += 1
        s_hat = attack(ct, d)

    e_hat = center(d - pt)                      # error also recoverable, given known pt
    ok_key = np.array_equal(s_hat, center(s))
    ok_err = np.array_equal(e_hat, center(e))
    print("[Part C] single-decryption key-recovery attack:")
    print("   c1 invertible after %d encryption(s)" % tries)
    print("   recovered error  == injected error :", bool(ok_err))
    print("   recovered secret == true secret    :", bool(ok_key))
    print("   true s      :", center(s).tolist())
    print("   recovered s :", s_hat.tolist())
    assert ok_key and ok_err, "ATTACK FAILED"
    print("\n[Stage 0 / Step 1] SUCCESS: secret key recovered EXACTLY from one decryption.")


if __name__ == "__main__":
    print("Parameters: N=%d, Q=%d (prime), sigma=%.1f, seed=%d\n" % (N, Q, SIGMA, SEED))
    selftest_ring()
    selftest_encdec()
    run_attack()