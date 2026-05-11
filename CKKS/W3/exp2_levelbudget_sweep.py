"""
W3 Experiment 2: Level budget sweep (memory-isolated, ONE budget per call).

Runs ONE budget per Python process invocation. To sweep, call this script
3 times with different --budget values; each call gets fresh memory.

Usage:
    python exp2_levelbudget_sweep.py --budget 3 --fast
    python exp2_levelbudget_sweep.py --budget 4 --fast
    python exp2_levelbudget_sweep.py --budget 5 --fast

Output one JSON per call to stdout, progress to stderr.
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
    if len(actual) != len(expected):
        raise ValueError("Length mismatch")
    max_err = max(abs(a.real - e.real) for a, e in zip(actual, expected))
    if max_err <= 0:
        return float("inf")
    return -math.log2(max_err)


def run_one_budget(budget_k: int, fast: bool):
    log = lambda m: print(m, file=sys.stderr, flush=True)
    log(f"\n=== Running level_budget = [{budget_k}, {budget_k}] ===")

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
        # Reduced-memory mode: N=2^14 (~1.5GB peak).
        params.SetSecurityLevel(SecurityLevel.HEStd_NotSet)
        params.SetRingDim(1 << 14)
    else:
        params.SetSecurityLevel(SecurityLevel.HEStd_128_classic)

    level_budget = [budget_k, budget_k]
    levels_after = 3
    boot_depth = FHECKKSRNS.GetBootstrapDepth(level_budget, secret_key_dist)
    depth = levels_after + boot_depth
    params.SetMultiplicativeDepth(depth)

    log(f"  Bootstrap consumes {boot_depth} levels; total depth = {depth}.")

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
    log(f"  Ring dim: {ring_dim}, slots: {num_slots}")

    t0 = time.time()
    cc.EvalBootstrapSetup(level_budget)
    t_setup = time.time() - t0

    keypair = cc.KeyGen()
    cc.EvalMultKeyGen(keypair.secretKey)

    t0 = time.time()
    cc.EvalBootstrapKeyGen(keypair.secretKey, num_slots)
    t_keygen = time.time() - t0

    x = [0.5 - 0.001 * (i % 100) for i in range(num_slots)]
    ptxt = cc.MakeCKKSPackedPlaintext(x, 1, depth - 1)
    ptxt.SetLength(num_slots)
    ct = cc.Encrypt(keypair.publicKey, ptxt)

    expected = x

    res_pre = cc.Decrypt(ct, keypair.secretKey)
    res_pre.SetLength(num_slots)
    prec_pre = precision_bits(res_pre.GetCKKSPackedValue(), expected)

    log(f"  Pre-bootstrap level: {ct.GetLevel()}, precision: {prec_pre:.2f} bits.")

    t0 = time.time()
    ct_boot = cc.EvalBootstrap(ct)
    t_bootstrap = time.time() - t0

    res_post = cc.Decrypt(ct_boot, keypair.secretKey)
    res_post.SetLength(num_slots)
    prec_post = precision_bits(res_post.GetCKKSPackedValue(), expected)
    levels_remaining = (depth - ct_boot.GetLevel()
                        - (ct_boot.GetNoiseScaleDeg() - 1))

    log(f"  Bootstrap time: {t_bootstrap:.2f}s")
    log(f"  Post-bootstrap precision: {prec_post:.2f} bits, "
        f"levels remaining: {levels_remaining}.")

    return {
        "level_budget": level_budget,
        "ring_dim": ring_dim,
        "num_slots": num_slots,
        "bootstrap_depth_consumed": boot_depth,
        "total_multiplicative_depth": depth,
        "level_pre_bootstrap": ct.GetLevel(),
        "level_post_bootstrap": ct_boot.GetLevel(),
        "levels_remaining_after_bootstrap": levels_remaining,
        "precision_pre_bootstrap_bits": round(prec_pre, 2),
        "precision_post_bootstrap_bits": round(prec_post, 2),
        "timings_seconds": {
            "context_gen": round(t_context, 3),
            "bootstrap_setup": round(t_setup, 3),
            "keygen_bootstrap": round(t_keygen, 3),
            "bootstrap_eval": round(t_bootstrap, 3),
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--budget", type=int, required=True,
                        help="Single budget k for level_budget=[k,k]")
    args = parser.parse_args()

    log = lambda m: print(m, file=sys.stderr, flush=True)
    log(f"Running single budget k={args.budget} "
        f"({'fast' if args.fast else 'production'} mode)...")

    result = run_one_budget(args.budget, args.fast)
    summary = {
        "experiment": "exp2_levelbudget_single",
        "mode": "fast" if args.fast else "production",
        "budget_k": args.budget,
        "result": result,
    }
    print(json.dumps(summary, indent=2))