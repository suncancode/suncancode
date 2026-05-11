# W3 Bootstrapping Experiments — Run Instructions

3 scripts to gather empirical data for Section 8 of the W3 report.

## Prerequisites

- OpenFHE-Python v1.5.0+ installed (`pip show openfhe` to verify).
- Python 3.10+.
- ~8 GB free RAM (production mode), ~2 GB (fast mode).

Quick sanity check OpenFHE is working:

```bash
python -c "from openfhe import CCParamsCKKSRNS, FHECKKSRNS, SecretKeyDist; \
  print('depth =', FHECKKSRNS.GetBootstrapDepth([4,4], SecretKeyDist.UNIFORM_TERNARY))"
```

Expected output: `depth = 14` (or similar small integer).

## Recommended Workflow

### Step 1 — Verify with --fast mode first (5–10 minutes total)

Fast mode uses HEStd_NotSet with N=2^16 — no real security but bootstrap
runs much faster, useful to confirm everything works before committing
to long production runs.

```bash
# Save outputs to text files for later parsing.
python exp1_bootstrap_baseline.py --fast --mults 4 > exp1_fast.json 2> exp1_fast.log
python exp2_levelbudget_sweep.py --fast --budgets 3,4,5 > exp2_fast.json 2> exp2_fast.log
python exp3_ppml_iterated.py --fast --n 8 --blocks 6 > exp3_fast.json 2> exp3_fast.log
```

If all three complete successfully, proceed to Step 2.

### Step 2 — Production runs with HEStd_128_classic (30–60 minutes total)

```bash
python exp1_bootstrap_baseline.py --mults 4 > exp1_prod.json 2> exp1_prod.log
python exp2_levelbudget_sweep.py --budgets 3,4,5 > exp2_prod.json 2> exp2_prod.log
python exp3_ppml_iterated.py --n 8 --blocks 10 > exp3_prod.json 2> exp3_prod.log
```

Expected runtime per script (production mode, WSL2/Ubuntu, 8-core CPU):

| Script | Setup | Bootstrap × N | Total |
|--------|-------|---------------|-------|
| exp1   | ~30s  | 1 × ~60s      | ~90s  |
| exp2   | ~30s × 3 | 3 × ~60s   | ~5 min |
| exp3   | ~30s  | ~3 × ~60s + 10 PPML blocks × ~5s | ~5 min |

If exp1 takes much longer than 90s, your machine may be RAM-constrained — switch
to `--fast` mode and report so.

## What to Send Back

Once all 6 .json files are generated, paste the contents (or just send the files).
I'll parse them and update Section 8 of `W3.tex` with real numbers, replacing the
"Proposed Experiments" placeholder with measured tables and analysis.

## Common Issues

**`AttributeError: module 'openfhe' has no attribute 'CCParamsCKKSRNS'`**
→ OpenFHE-Python not installed properly. Try `pip install openfhe` again
  (Ubuntu 22.04 / 24.04 only).

**`OPENFHE_THROW: FHE feature is not enabled`**
→ Make sure `cc.Enable(PKESchemeFeature.FHE)` is called. The scripts already do
  this — if it still fails, your build of OpenFHE-Python may be missing FHE
  support (rare). Rebuild with `-DWITH_FHE=ON` cmake flag.

**`MemoryError` or system swap thrashing**
→ Use `--fast` mode. Production mode with HEStd_128_classic needs N=65536
  which uses ~6–8 GB RAM at peak.

**Bootstrap precision suspiciously low (< 10 bits)**
→ Most likely: input vector contains values too far from [-1, 1]. Sigmoid
  approximation in exp3 assumes |dot| < ~5. Reduce input magnitude in the
  script if needed.

## Tweaking Parameters

If you have time and want richer data:

```bash
# More multiplications before bootstrap (test wall-hitting precision).
python exp1_bootstrap_baseline.py --mults 8

# Wider budget sweep.
python exp2_levelbudget_sweep.py --budgets 2,3,4,5,6

# Larger dot product / more blocks.
python exp3_ppml_iterated.py --n 16 --blocks 20
```
