"""
Stage 0 probe (Step 2) -- stage0_encoded_probe.py
Add the CKKS canonical-embedding encoding on top of the Step-1 RLWE layer and
show that an adversary who observes ONLY the decoded approximate message (the
complex slot vector that decryption returns) reconstructs the ring decryption
d = pt + e exactly, and hence recovers the secret key.  Real-only mode, matching
OpenFHE's secure CKKS: intended messages are real, and the imaginary part of the
decoded slots serves as the noise gauge (the signal OpenFHE reads to estimate
noise, which the Stage 2-3 audit will target).

Encoding (canonical embedding):
  roots  w_k = exp(i*pi*(2k+1)/N),  k = 0..N-1   (the N roots of X^N + 1)
  V[k,i] = w_k^i.  V/sqrt(N) is UNITARY, so V^{-1} = (1/N) V^*  and V^{-1}u is
  exactly real when u is conjugate-symmetric.
  encode(z) : u = expand_conj(z);  pt = round(Delta * V^{-1} u)   (real integer poly)
  decode(d) : zt = (V d / Delta)[0:N/2]                            (complex slots)

Parts (each self-verifies before the next is trusted):
  A : ring R_q sanity (reused from Step 1)
  B : encoding self-tests (V unitary; V^{-1} = V^*/N; encode/decode round-trip)
  C : real-only pipeline; imaginary slot part tracks the ring-error magnitude
  D : the attack -- observe zt only, reconstruct d exactly, recover s exactly
"""

import numpy as np

# ----------------------------------------------------------------------
# Parameters (toy; Delta and Q chosen so that pt+e never wraps mod Q)
# ----------------------------------------------------------------------
N      = 16            # ring degree (slots = N/2 = 8)
Q      = 65537         # prime modulus (Fermat inverse for the GF(Q) solve)
DELTA  = 2 ** 12       # scaling factor (message precision ~ 12 bits here)
SIGMA  = 3.2
ZMAX   = 2.0           # message range; DELTA*ZMAX + ||e|| must stay < Q/2
SEED   = 2025
rng = np.random.default_rng(SEED)

assert DELTA * ZMAX + 10 * SIGMA < Q / 2, "parameters would wrap mod Q"


def center(x):
    x = np.asarray(x) % Q
    return np.where(x > Q // 2, x - Q, x).astype(np.int64)


# ----------------------------------------------------------------------
# Part A : ring R_q = Z_q[X]/(X^N + 1)   (same as Step 1)
# ----------------------------------------------------------------------
def ring_mult(a, b):
    full = np.convolve(np.asarray(a, np.int64), np.asarray(b, np.int64))
    cc = np.zeros(2 * N, dtype=np.int64); cc[:full.size] = full
    return (cc[:N] - cc[N:2 * N]) % Q


def neg_matrix(a):
    A = np.zeros((N, N), dtype=np.int64)
    for j in range(N):
        ej = np.zeros(N, dtype=np.int64); ej[j] = 1
        A[:, j] = ring_mult(a, ej)
    return A % Q


# ----------------------------------------------------------------------
# Part B : CKKS canonical-embedding encoding
# ----------------------------------------------------------------------
_roots = np.exp(1j * np.pi * (2 * np.arange(N) + 1) / N)      # w_k, roots of X^N+1
V      = _roots[:, None] ** np.arange(N)[None, :]             # V[k,i] = w_k^i
V_inv  = V.conj().T / N                                       # analytic inverse (V/sqrt N unitary)


def expand_conj(half):
    """Build a length-N conjugate-symmetric vector from N/2 slots."""
    full = np.zeros(N, dtype=complex)
    h = len(half)
    for k in range(h):
        full[k] = half[k]
        full[N - 1 - k] = np.conj(half[k])
    return full


def encode(z_half):
    """z_half in C^{N/2} -> real integer plaintext polynomial pt in Z^N."""
    m = (V_inv @ expand_conj(z_half)).real
    return np.rint(DELTA * m).astype(np.int64)


def decode(d_ring):
    """centered integer ring element d -> complex slots zt in C^{N/2}."""
    return (V @ d_ring.astype(np.float64))[:N // 2] / DELTA


def selftest_encoding():
    I = np.eye(N)
    assert np.allclose(V_inv @ V, I, atol=1e-9) and np.allclose(V @ V_inv, I, atol=1e-9), \
        "V^{-1} (=V^*/N) is not the inverse of V"
    assert np.allclose(np.linalg.inv(V), V_inv, atol=1e-9), "analytic inverse != numeric inverse"
    # round-trip on a general complex vector (stringent test of the embedding)
    zc = rng.uniform(-ZMAX, ZMAX, N // 2) + 1j * rng.uniform(-ZMAX, ZMAX, N // 2)
    err_c = np.max(np.abs(decode(center(encode(zc) % Q)) - zc))
    # round-trip on a real vector (real-only mode)
    zr = rng.uniform(-ZMAX, ZMAX, N // 2)
    ztr = decode(center(encode(zr) % Q))
    err_r = np.max(np.abs(ztr.real - zr))
    bound = N / (2 * DELTA)                                   # rounding-only bound ~ N/(2 Delta)
    assert err_c < 2 * bound and err_r < 2 * bound, "round-trip error exceeds rounding bound"
    print("[Part B] encoding self-tests PASS")
    print("   V/sqrt(N) unitary, V^{-1} = V^*/N verified to < 1e-9")
    print("   round-trip error: complex %.2e, real %.2e  (rounding bound %.2e)"
          % (err_c, err_r, bound))


# ----------------------------------------------------------------------
# Part C : real-only pipeline + imaginary-slot noise gauge
# ----------------------------------------------------------------------
def keygen():
    return rng.integers(-1, 2, N).astype(np.int64)


def sample_error():
    return np.rint(rng.normal(0.0, SIGMA, N)).astype(np.int64)


def encrypt(pt, s):
    a = rng.integers(0, Q, N).astype(np.int64)
    e = sample_error()
    c0 = (-ring_mult(a, s) + pt + e) % Q
    return (c0, a), e


def decrypt(ct, s):
    c0, c1 = ct
    return center((c0 + ring_mult(c1, s)) % Q)


def selftest_pipeline():
    s = keygen()
    z = rng.uniform(-ZMAX, ZMAX, N // 2)                      # real message (real-only mode)
    ct, e = encrypt(encode(z), s)
    d  = decrypt(ct, s)
    zt = decode(d)                                           # what decryption returns
    sig_err  = np.max(np.abs(zt.real - z))                    # signal error
    imag_mag = np.max(np.abs(zt.imag))                        # noise gauge (imag part)
    # reference: the decoded ring error, whose magnitude the imag part should track
    e_decoded = np.max(np.abs((V @ center(e).astype(np.float64))[:N // 2] / DELTA))
    print("[Part C] real-only pipeline PASS")
    print("   ||Re(zt) - z||_inf      = %.3e  (signal recovered)" % sig_err)
    print("   ||Im(zt)||_inf          = %.3e  (noise gauge)" % imag_mag)
    print("   ||decoded ring error||  = %.3e  (same order as the gauge)" % e_decoded)


# ----------------------------------------------------------------------
# Part D : the attack -- observe zt only, reconstruct d, recover s
# ----------------------------------------------------------------------
def gauss_solve_modp(A, b, p):
    A = (A % p).astype(object).copy(); b = (b % p).astype(object).copy()
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
                A[r] = (A[r] - f * A[col]) % p; b[r] = (b[r] - f * b[col]) % p
    return np.array([int(v) for v in b], dtype=np.int64) % p


def reconstruct_d(zt):
    """From the observed complex slots zt, rebuild the centered ring element d."""
    sigma_full = expand_conj(DELTA * zt)                     # full canonical embedding of d
    d_float = (V_inv @ sigma_full).real                      # V^{-1} sigma(d) = d (up to float)
    return center(np.rint(d_float).astype(np.int64))


def run_encoded_attack():
    s  = keygen()
    z1 = rng.uniform(-ZMAX / 2, ZMAX / 2, N // 2)
    z2 = rng.uniform(-ZMAX / 2, ZMAX / 2, N // 2)
    ct1, e1 = encrypt(encode(z1), s)
    ct2, e2 = encrypt(encode(z2), s)
    # homomorphic addition: the adversary evaluates a function, then decrypts
    ct = ((ct1[0] + ct2[0]) % Q, (ct1[1] + ct2[1]) % Q)
    d_true = decrypt(ct, s)
    zt = decode(d_true)                                      # the ONLY thing the adversary observes

    tries = 1
    d_rec = reconstruct_d(zt)
    ok_d = np.array_equal(d_rec, d_true)
    c0, c1 = ct
    s_hat = None
    if ok_d:
        t = (d_rec - c0) % Q
        s_hat = gauss_solve_modp(neg_matrix(c1), t, Q)
    while s_hat is None:                                     # c1 non-invertible (rare): fresh input
        z2 = rng.uniform(-ZMAX / 2, ZMAX / 2, N // 2)
        ct2, e2 = encrypt(encode(z2), s); tries += 1
        ct = ((ct1[0] + ct2[0]) % Q, (ct1[1] + ct2[1]) % Q)
        d_true = decrypt(ct, s); zt = decode(d_true)
        d_rec = reconstruct_d(zt); ok_d = np.array_equal(d_rec, d_true)
        c0, c1 = ct
        if ok_d:
            s_hat = gauss_solve_modp(neg_matrix(c1), (d_rec - c0) % Q, Q)
    s_hat = center(s_hat)
    ok_key = np.array_equal(s_hat, center(s))
    print("[Part D] attack from the observed message (after one homomorphic add):")
    print("   reconstructed d == true decryption d :", bool(ok_d), "(exact integer match)")
    print("   c1 invertible after %d attempt(s)" % tries)
    print("   recovered secret == true secret      :", bool(ok_key))
    print("   true s      :", center(s).tolist())
    print("   recovered s :", s_hat.tolist())
    assert ok_d and ok_key, "ATTACK FAILED"
    print("\n[Stage 0 / Step 2] SUCCESS: key recovered from the decoded approximate message.")


if __name__ == "__main__":
    print("Parameters: N=%d, Q=%d, Delta=2^%d, sigma=%.1f, seed=%d\n"
          % (N, Q, int(np.log2(DELTA)), SIGMA, SEED))
    selftest_encoding()
    selftest_pipeline()
    run_encoded_attack()