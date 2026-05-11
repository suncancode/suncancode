"""
W3 Experiment 1: Bootstrap baseline measurement.

Encrypt a test vector, perform N multiplications to deplete the modulus chain,
bootstrap, decrypt, and measure latency + precision + levels remaining.

Usage:
    python exp1_bootstrap_baseline.py [--fast] [--mults N]

    --fast       Use HEStd_NotSet with N=2^16 (fast, ~30s bootstrap).
    --mults N    Number of consecutive squarings before bootstrap (default 4).

Outputs JSON to stdout with all measurements; human-readable info to stderr.
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


def precision_bits(actual, expected):
    """Standard CKKS precision metric: -log2(max abs error)."""
    if len(actual) != len(expected):
        raise ValueError("Length mismatch")
    max_err = max(abs(a.real - e.real) for a, e in zip(actual, expected))
    if max_err <= 0:
        return float("inf")
    return -math.log2(max_err)


def run(fast: bool, mults: int):
    log = lambda msg: print(msg, file=sys.stderr, flush=True)

    # ---------- Step 1: parameter setup ----------
    params = CCParamsCKKSRNS()
    secret_key_dist = SecretKeyDist.UNIFORM_TERNARY
    params.SetSecretKeyDist(secret_key_dist)

    # 64-bit native: FLEXIBLEAUTO, dcrt=59, first=60.
    # 128-bit native: FIXEDAUTO, dcrt=78, first=89.
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
        # Reduced-memory mode for low-RAM machines.
        # Security: ~80-100 bits, NOT production-grade 128-bit.
        params.SetSecurityLevel(SecurityLevel.HEStd_NotSet)
        params.SetRingDim(1 << 14)  # N = 16384 (matches exp2/exp3)
        log("Mode: REDUCED (HEStd_NotSet, N=2^14, ~80-100 bit security)")
    else:
        # Production mode: 128-bit security, OpenFHE picks N (typically 2^16).
        params.SetSecurityLevel(SecurityLevel.HEStd_128_classic)
        log("Mode: PRODUCTION (HEStd_128_classic, ring dim auto)")

    level_budget = [4, 4]
    levels_after = 5  # reduced from 10 to limit total depth
    boot_depth = FHECKKSRNS.GetBootstrapDepth(level_budget, secret_key_dist)
    depth = levels_after + boot_depth
    params.SetMultiplicativeDepth(depth)

    log(f"Bootstrap depth (consumed by bootstrap itself): {boot_depth}")
    log(f"Total multiplicative depth: {depth}")
    log(f"Level budget [CTS, StC]: {level_budget}")
    log(f"Levels available after bootstrap (target): {levels_after}")

    # ---------- Step 2: context generation ----------
    t0 = time.time()
    cc = GenCryptoContext(params)
    cc.Enable(PKESchemeFeature.PKE)
    cc.Enable(PKESchemeFeature.KEYSWITCH)
    cc.Enable(PKESchemeFeature.LEVELEDSHE)
    cc.Enable(PKESchemeFeature.ADVANCEDSHE)
    cc.Enable(PKESchemeFeature.FHE)
    t_context = time.time() - t0

    ring_dim = cc.GetRingDimension()
    num_slots = ring_dim // 2
    log(f"Ring dimension N: {ring_dim}")
    log(f"Number of slots: {num_slots}")
    log(f"Context generation time: {t_context:.2f}s")

    # ---------- Step 3: bootstrap setup + key gen ----------
    t0 = time.time()
    cc.EvalBootstrapSetup(level_budget)
    t_boot_setup = time.time() - t0
    log(f"EvalBootstrapSetup time: {t_boot_setup:.2f}s")

    t0 = time.time()
    keypair = cc.KeyGen()
    cc.EvalMultKeyGen(keypair.secretKey)
    t_keygen_basic = time.time() - t0
    log(f"Basic key generation time: {t_keygen_basic:.2f}s")

    t0 = time.time()
    cc.EvalBootstrapKeyGen(keypair.secretKey, num_slots)
    t_boot_keygen = time.time() - t0
    log(f"Bootstrap key generation time: {t_boot_keygen:.2f}s")

    # ---------- Step 4: encrypt a test vector ----------
    # Bound values to [0.4, 0.5] to stay within bootstrap's sin-approx domain.
    x = [0.5 - 0.001 * (i % 100) for i in range(num_slots)]
    # Encode at the boot-input level (level = depth - 1, after StC budget).
    ptxt = cc.MakeCKKSPackedPlaintext(x, 1, depth - 1)
    ptxt.SetLength(num_slots)

    ct = cc.Encrypt(keypair.publicKey, ptxt)
    log(f"Initial level: {ct.GetLevel()}, "
        f"levels remaining (approx): {depth - ct.GetLevel()}")

    # ---------- Step 5: deplete chain via consecutive squarings ----------
    # Avoid plaintext mults so we keep behavior simple.
    expected = list(x)
    actual_mults = 0
    for i in range(mults):
        # Skip if we'd run out of levels for the bootstrap input requirement.
        if ct.GetLevel() >= depth - level_budget[1] - 1:
            log(f"Stopping mults at iteration {i}: not enough levels left "
                f"for bootstrap.")
            break
        ct = cc.EvalMult(ct, ct)
        expected = [v * v for v in expected]
        actual_mults += 1
    level_pre_boot = ct.GetLevel()
    log(f"Performed {actual_mults} squarings — level: {level_pre_boot}")

    # ---------- Step 6: measure precision before bootstrap ----------
    res_pre = cc.Decrypt(ct, keypair.secretKey)
    res_pre.SetLength(num_slots)
    prec_pre = precision_bits(res_pre.GetCKKSPackedValue(), expected)
    log(f"Precision before bootstrap: {prec_pre:.2f} bits")

    # ---------- Step 7: BOOTSTRAP ----------
    t0 = time.time()
    ct_boot = cc.EvalBootstrap(ct)
    t_bootstrap = time.time() - t0
    log(f"\n>>> Bootstrap time: {t_bootstrap:.2f}s <<<\n")

    # ---------- Step 8: precision and levels after bootstrap ----------
    res_post = cc.Decrypt(ct_boot, keypair.secretKey)
    res_post.SetLength(num_slots)
    prec_post = precision_bits(res_post.GetCKKSPackedValue(), expected)

    # OpenFHE's documented formula for remaining levels.
    levels_remaining = (depth - ct_boot.GetLevel()
                        - (ct_boot.GetNoiseScaleDeg() - 1))
    log(f"Precision after bootstrap: {prec_post:.2f} bits")
    log(f"Levels remaining after bootstrap: {levels_remaining}")

    # ---------- Step 9: emit JSON to stdout ----------
    result = {
        "experiment": "exp1_bootstrap_baseline",
        "mode": "fast" if fast else "production",
        "ring_dim": ring_dim,
        "num_slots": num_slots,
        "scaling_mod_size": dcrt_bits,
        "first_mod_size": first_mod,
        "level_budget": level_budget,
        "levels_after_target": levels_after,
        "bootstrap_depth_consumed": boot_depth,
        "total_multiplicative_depth": depth,
        "mults_requested": mults,
        "mults_actually_performed": actual_mults,
        "level_pre_bootstrap": level_pre_boot,
        "level_post_bootstrap": ct_boot.GetLevel(),
        "levels_remaining_after_bootstrap": levels_remaining,
        "precision_pre_bootstrap_bits": round(prec_pre, 2),
        "precision_post_bootstrap_bits": round(prec_post, 2),
        "timings_seconds": {
            "context_gen": round(t_context, 3),
            "bootstrap_setup": round(t_boot_setup, 3),
            "keygen_basic": round(t_keygen_basic, 3),
            "keygen_bootstrap": round(t_boot_keygen, 3),
            "bootstrap_eval": round(t_bootstrap, 3),
        },
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true",
                        help="Use HEStd_NotSet with N=2^16 (no security).")
    parser.add_argument("--mults", type=int, default=2,
                        help="Number of consecutive squarings (default 2).")
    args = parser.parse_args()
    run(fast=args.fast, mults=args.mults)