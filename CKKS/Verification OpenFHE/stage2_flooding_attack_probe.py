"""
Stage 2 probe -- stage2_flooding_attack_probe.py
Reproduce the Guo et al. (USENIX Security 2024) key-recovery attack that defeats
noise flooding when the flooding is sized by an AVERAGE-CASE noise estimate, and
show that a WORST-CASE-sized flooding blocks the same attack.

CONVENTION (matches Guo/Li-Micciancio exactly)
    ciphertext ct = (a, b),  b = a*s + e (mod Q),  Dec(a,b) = b - a*s (mod Q).
    secret s: uniform ternary in {-1,0,1}^N.  message m = 0, so Dec = e.

THE ATTACK (first principles)
    1. encrypt 0 -> c0 = (a, b),  b = a*s + e,  e ~ N(0, sigma1) per coeff.
    2. homomorphically add t copies of c0 -> (t*a, t*b); its error is t*e
       (identical inputs add COHERENTLY -- the worst case, Stage 1).
    3. flooded decryption returns  e_total = t*e + e_new,  e_new ~ N(0, sigma2).
    4. Gaussian conditioning (Guo Lemma 2): given e_total, the conditional mean
       of e is  e_total * c,  c = t*sigma1^2 / (sigma2^2 + t^2*sigma1^2).
       Subtract it from the fresh b:
            b'_i = b_i - e_total_i * c        ->   b' = a*s + e'
       with  std(e') = sigma_attack = sigma1*sigma2 / sqrt(t^2*sigma1^2 + sigma2^2).
    5. if sigma_attack is small (e' rounds to 0), recover s = a^{-1} b'.

WHY AVERAGE-CASE FLOODING BREAKS
    OpenFHE sizes sigma2 = sqrt(12*tau) * 2^(nu/2) * sigma_est with the AVERAGE-CASE
    estimate sigma_est ~ sqrt(t)*sigma1 (tau = 1 decryption query, nu >= 30).
    Then sigma_attack = Theta(t^{-1/2}) -> 0: pick t large, recovery succeeds.
    A WORST-CASE flooding sigma2 ~ t*sigma1 gives sigma_attack ~ sigma1/sqrt(2):
    bounded below, recovery fails.  This probe demonstrates both.
"""

import numpy as np

N      = 16
SIGMA1 = 3.2
SEED   = 2025
rng = np.random.default_rng(SEED)


# ----------------------------------------------------------------------
# a prime modulus (Miller-Rabin), large enough that t*e + e_new never wraps
# ----------------------------------------------------------------------
def is_prime(n):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2; r += 1
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime(n):
    while not is_prime(n):
        n += 1
    return n


Q = next_prime(2 ** 23)


def center(x):
    x = np.asarray(x) % Q
    return np.where(x > Q // 2, x - Q, x).astype(np.int64)


def center_real(x):
    x = np.asarray(x, dtype=np.float64)
    return ((x + Q / 2) % Q) - Q / 2


# ----------------------------------------------------------------------
# ring, keys, encryption (Guo convention), homomorphic sum, flooded decrypt
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


def keygen():
    return rng.integers(-1, 2, N).astype(np.int64)


def enc_zero(s):
    a = rng.integers(0, Q, N).astype(np.int64)
    e = np.rint(rng.normal(0.0, SIGMA1, N)).astype(np.int64)
    b = (ring_mult(a, s) + e) % Q                     # b = a*s + e  (m = 0)
    return (a, b), e


def sum_t(c0, t):
    a, b = c0
    return ((t * a) % Q, (t * b) % Q)                 # error becomes t*e


def flooded_decrypt(ct, s, sigma2):
    a, b = ct
    dec = center((b - ring_mult(a, s)) % Q)           # = t*e  (m = 0)
    e_new = np.rint(rng.normal(0.0, sigma2, N)).astype(np.int64)
    return center(dec + e_new)                        # e_total = t*e + e_new


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


def sigma_attack(t, sigma2):
    return SIGMA1 * sigma2 / np.sqrt((t * SIGMA1) ** 2 + sigma2 ** 2)


def flood_sigma(t, nu, worst_case=False):
    """OpenFHE-style flooding std, sized by average-case or worst-case estimate."""
    sigma_est = (t * SIGMA1) if worst_case else (np.sqrt(t) * SIGMA1)
    tau = 1                                            # one decryption query
    return np.sqrt(12 * tau) * (2.0 ** (nu / 2)) * sigma_est


# ======================================================================
# Part B (2a): theory scan -- when does sigma_attack drop below 1/2 ?
# ======================================================================
def part_b():
    print("[Part B] sigma_attack vs t  (recovery becomes trivial when < 0.5)\n")
    for nu in (0, 30):
        print("  nu = %d" % nu)
        print("     %-8s %-16s %-16s" % ("log2 t", "avg-case flood", "worst-case flood"))
        threshold = None
        for k in range(0, 62, 3):
            t = 2 ** k
            sa_avg = sigma_attack(t, flood_sigma(t, nu, worst_case=False))
            sa_wc  = sigma_attack(t, flood_sigma(t, nu, worst_case=True))
            print("     %-8d %-16.4g %-16.4g" % (k, sa_avg, sa_wc))
        # find the exact crossover for the average-case flooding
        for k in range(0, 80):
            if sigma_attack(2 ** k, flood_sigma(2 ** k, nu, worst_case=False)) < 0.5:
                threshold = k; break
        print("     -> avg-case sigma_attack < 0.5 first at log2 t = %d\n" % threshold)


# ======================================================================
# Part C (2b): run the recovery in the simulator
# ======================================================================
def run_recovery(c0, e, t, sigma2, s_true):
    a, b = c0
    ct = sum_t(c0, t)
    e_total = flooded_decrypt(ct, s_true, sigma2)
    c = t * SIGMA1 ** 2 / (sigma2 ** 2 + (t * SIGMA1) ** 2)     # Guo Lemma 2
    b_prime = b.astype(np.float64) - e_total.astype(np.float64) * c
    e_prime = center_real(b_prime - ring_mult(a, s_true))       # residual (uses s only to measure)
    rhs = center(np.rint(b_prime).astype(np.int64))             # round(b') = a*s if e' ~ 0
    s_hat = gauss_solve_modp(neg_matrix(a), rhs % Q, Q)
    s_hat = None if s_hat is None else center(s_hat)
    return {
        "sigma_attack_theory": sigma_attack(t, sigma2),
        "sigma_attack_emp":    float(np.std(e_prime)),
        "eprime_max":          float(np.max(np.abs(np.rint(e_prime)))),
        "eprime_nonzero":      int(np.count_nonzero(np.rint(e_prime))),
        "recovered":           (s_hat is not None and np.array_equal(s_hat, center(s_true))),
    }


def part_c():
    nu, t = 0, 2 ** 14
    print("[Part C] recovery on the simulator   (nu = %d, t = 2^%d, Q ~ 2^%d)\n"
          % (nu, int(np.log2(t)), int(np.log2(Q))))
    # one fresh ciphertext with invertible a, reused for both flooding regimes
    while True:
        s = keygen(); c0, e = enc_zero(s)
        if gauss_solve_modp(neg_matrix(c0[0]), center(c0[1]) % Q, Q) is not None:
            break
    for label, wc in [("average-case flooding", False), ("worst-case flooding", True)]:
        sigma2 = flood_sigma(t, nu, worst_case=wc)
        r = run_recovery(c0, e, t, sigma2, s)
        print("  %s  (sigma2 = %.3g)" % (label, sigma2))
        print("     sigma_attack: theory %.4f, empirical %.4f"
              % (r["sigma_attack_theory"], r["sigma_attack_emp"]))
        print("     residual e': max |coef| = %.0f, nonzero coeffs = %d / %d"
              % (r["eprime_max"], r["eprime_nonzero"], N))
        print("     secret key recovered: %s\n" % r["recovered"])


if __name__ == "__main__":
    print("Parameters: N=%d, Q=%d (prime, ~2^%d), sigma1=%.1f, seed=%d\n"
          % (N, Q, int(np.log2(Q)), SIGMA1, SEED))
    part_b()
    part_c()