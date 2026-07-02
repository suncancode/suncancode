"""
Stage 1 probe -- stage1_noise_gap_probe.py
Measure how the ciphertext error of a SUMMATION circuit grows with the number
of summands t, in two regimes:
    (independent)  t fresh, independent ciphertexts         -> std ~ sigma*sqrt(t)
    (identical)    the same ciphertext added to itself t x  -> std ~ sigma*t
The gap between the two is a factor sqrt(t): the average-case-vs-worst-case gap
that a noise-flooding calibrated to the average case silently misses.

FIRST PRINCIPLES (scheme level)
    Homomorphic addition is exact in the ring, so the error of the sum is the
    exact sum of the errors:                e_sum = sum_i e_i .
    - independent e_i : coeff variance adds -> Var = t*sigma^2 -> std = sigma*sqrt(t)
    - identical e_i=e : e_sum = t*e                            -> std = t*sigma
    The canonical embedding sigma() is LINEAR, so the same exponent appears in
    the ring domain ||e|| and in the imaginary-slot domain ||Im(decode(.))||
    (the signal OpenFHE reads in real mode to estimate noise).

WHAT WE VERIFY (code level)
    (1) the identity e_sum == sum_i e_i holds EXACTLY in the running pipeline;
    (2) the measured growth exponent matches 0.5 (independent) and 1.0 (identical);
    (3) the same exponent shows up in the ring domain and the imaginary-slot domain;
    (4) the ratio identical/independent tracks sqrt(t).
"""

import numpy as np

# ----------------------------------------------------------------------
# Parameters (toy; messages are 0 so only the error is measured, no wrap)
# ----------------------------------------------------------------------
N      = 16
Q      = 65537
DELTA  = 2 ** 12
SIGMA  = 3.2
T_LIST = [1, 2, 4, 8, 16, 32, 64, 128, 256]
TRIALS = 1000
SEED   = 2025
rng = np.random.default_rng(SEED)


def center(x):
    x = np.asarray(x) % Q
    return np.where(x > Q // 2, x - Q, x).astype(np.int64)


# ----------------------------------------------------------------------
# ring R_q and canonical embedding (same primitives as Stage 0)
# ----------------------------------------------------------------------
def ring_mult(a, b):
    full = np.convolve(np.asarray(a, np.int64), np.asarray(b, np.int64))
    cc = np.zeros(2 * N, dtype=np.int64); cc[:full.size] = full
    return (cc[:N] - cc[N:2 * N]) % Q


_roots = np.exp(1j * np.pi * (2 * np.arange(N) + 1) / N)
V = _roots[:, None] ** np.arange(N)[None, :]


def imag_slots(d_ring):
    """Imaginary part of the decoded slots -- the OpenFHE real-mode noise gauge."""
    return ((V @ d_ring.astype(np.float64))[:N // 2] / DELTA).imag


# ----------------------------------------------------------------------
# minimal RLWE, encrypting the ZERO message (so decryption returns e_sum)
# ----------------------------------------------------------------------
def keygen():
    return rng.integers(-1, 2, N).astype(np.int64)


def sample_error():
    return np.rint(rng.normal(0.0, SIGMA, N)).astype(np.int64)


def enc_zero(s):
    a = rng.integers(0, Q, N).astype(np.int64)
    e = sample_error()
    c0 = (-ring_mult(a, s) + e) % Q            # pt = 0
    return (c0, a), e


def decrypt(ct, s):
    c0, c1 = ct
    return center((c0 + ring_mult(c1, s)) % Q)


# ----------------------------------------------------------------------
# the two summation regimes
# ----------------------------------------------------------------------
def sum_independent(s, t):
    """t fresh, independent ciphertexts, added together."""
    cts = [enc_zero(s) for _ in range(t)]
    c0 = np.sum([c[0][0] for c in cts], axis=0) % Q
    c1 = np.sum([c[0][1] for c in cts], axis=0) % Q
    e_direct = center(np.sum([c[1] for c in cts], axis=0))     # sum of the input errors
    d = decrypt((c0, c1), s)                                   # message 0 -> d = e_sum
    return d, e_direct


def sum_identical(s, t):
    """the SAME ciphertext added to itself t times."""
    ct, e = enc_zero(s)
    c0 = (t * ct[0]) % Q
    c1 = (t * ct[1]) % Q
    e_direct = center(t * e)
    d = decrypt((c0, c1), s)
    return d, e_direct


def rms(x):
    x = np.asarray(x, dtype=np.float64)
    return np.sqrt(np.mean(x ** 2))


# ----------------------------------------------------------------------
# measurement: pool coefficients over trials, take RMS, fit the exponent
# ----------------------------------------------------------------------
def measure(regime):
    ring_rms, slot_rms, identity_ok = [], [], True
    for t in T_LIST:
        ring_pool, slot_pool = [], []
        for _ in range(TRIALS):
            s = keygen()
            d, e_direct = regime(s, t)
            if not np.array_equal(d, e_direct):                # (1) exact identity check
                identity_ok = False
            ring_pool.append(d.astype(np.float64))
            slot_pool.append(imag_slots(d))
        ring_rms.append(rms(np.concatenate(ring_pool)))
        slot_rms.append(rms(np.concatenate(slot_pool)))
    return np.array(ring_rms), np.array(slot_rms), identity_ok


def fit_slope(rms_arr):
    return np.polyfit(np.log(T_LIST), np.log(rms_arr), 1)[0]


if __name__ == "__main__":
    print("Parameters: N=%d, Q=%d, Delta=2^%d, sigma=%.1f, trials=%d\n"
          % (N, Q, int(np.log2(DELTA)), SIGMA, TRIALS))
    t = np.array(T_LIST, dtype=float)

    results = {}
    for name, regime, expect in [("INDEPENDENT", sum_independent, 0.5),
                                 ("IDENTICAL",   sum_identical,   1.0)]:
        ring_r, slot_r, ok = measure(regime)
        results[name] = ring_r
        theory = SIGMA * (t ** expect)
        print("[%s]  identity e_sum == sum(e_i): %s" % (name, ok))
        print("   %-5s %-12s %-13s %-12s" % ("t", "RMS(ring)", "RMS(Im slot)", "theory"))
        for i, tv in enumerate(T_LIST):
            print("   %-5d %-12.4f %-13.6f %-12.4f" % (tv, ring_r[i], slot_r[i], theory[i]))
        print("   fitted exponent: ring %.3f, slot %.3f   (theory %.1f)\n"
              % (fit_slope(ring_r), fit_slope(slot_r), expect))

    print("[GAP]  identical / independent   vs   sqrt(t)")
    print("   %-5s %-14s %-10s" % ("t", "ratio (ring)", "sqrt(t)"))
    for i, tv in enumerate(T_LIST):
        print("   %-5d %-14.3f %-10.3f" % (tv, results["IDENTICAL"][i] / results["INDEPENDENT"][i], np.sqrt(tv)))
