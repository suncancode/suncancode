import numpy as np

print("#"*70)
print("# CHECK 1: Group facts -- is conjugation a genuinely separate key?")
print("#"*70)
for logN in [4, 8, 16]:
    N = 2**logN; twoN = 2*N
    sub = set()
    x = 1
    for _ in range(twoN):
        x = (x*5) % twoN
        sub.add(x)
        if x == 1: break
    minus1 = (twoN - 1) % twoN
    print(f"  N=2^{logN}: <5> has {len(sub)} elements (expected N/2={N//2}); "
          f"-1(={minus1}) in <5>? {minus1 in sub}")
print("  => conjugation (-1) is NEVER a power of 5 -> it is exactly ONE extra key,")
print("     and (Z/2N)* is abelian so it cannot create new rotation amounts.\n")

print("#"*70)
print("# CHECK 2: What does REAL CKKS conjugation actually do to slots?")
print("#"*70)
print("  In CKKS, conjugate() returns conj(z_i) in the SAME slot i (no reversal).")
print("  The natural-order toy used conj WITH reversal -- that was optimistic.\n")

def ckks_conjugate(v):          # the REAL semantics: elementwise conjugate, NO permutation
    return np.conj(v)

# rfft split needs  conj(Z[M-k])  in slot k.  Can elementwise conj give it?
M = 8
z = np.random.randn(M) + 1j*np.random.randn(M)
Z = np.fft.fft(z)
needed   = np.conj(Z[(-np.arange(M)) % M])   # conj(Z[M-k]) : conj + REVERSAL
got_ckks = ckks_conjugate(Z)                 # conj(Z[k])   : conj only
print(f"  needed by rfft combine (conj+reverse): {np.round(needed[:4],2)}")
print(f"  real CKKS conjugate (conj only)      : {np.round(got_ckks[:4],2)}")
print(f"  equal? {np.allclose(needed, got_ckks)}")
print("  => NOT equal. The rfft-split needs a slot REVERSAL k->-k, which is NOT")
print("     a single rotation. Done naively it costs ~M rotations = as much as the")
print("     whole transform. So 'halve one transform via rfft-split' is NOT a clean")
print("     +1 conjugation in real CKKS. (This is exactly what conjugate-invariant")
print("     ring / imaginary-removing prior work restructures to handle.)\n")

print("#"*70)
print("# CHECK 3: The reversal-FREE way real data helps -- pack TWO real windows")
print("#"*70)
print("  Convolve two real signals a,b at once via z=a+ib, stay in packed form.")
n = 16
a = np.random.randn(n); b = np.random.randn(n); w = np.random.randn(n)  # real filter
z = a + 1j*b
# circular convolution via one complex DFT pair
conv_packed = np.fft.ifft(np.fft.fft(z) * np.fft.fft(w))
conv_a = np.fft.ifft(np.fft.fft(a) * np.fft.fft(w)).real
conv_b = np.fft.ifft(np.fft.fft(b) * np.fft.fft(w)).real
print(f"  real(packed) == conv(a,w)? {np.allclose(conv_packed.real, conv_a)}")
print(f"  imag(packed) == conv(b,w)? {np.allclose(conv_packed.imag, conv_b)}")
print("  => YES. ONE complex transform-pair convolves TWO real signals, NO split,")
print("     NO reversal, NO extra conjugation. This is a clean 2x THROUGHPUT win,")
print("     ideal for streaming (two ECG windows per ciphertext).\n")

print("#"*70)
print("# CHECK 4: Realistic key count -- radix-2 FACTORED transform (not proxy)")
print("#"*70)
def factored_keys(m):
    # radix-2 butterfly: distinct rotation amounts are the strides {1,2,...,m/2}
    # but per-stage only a small fixed set; HFT uses ~ 2*log2(m)-1 rotations total
    s = int(round(np.log2(m)))
    return {"rotations(keys)": 2*s-1, "depth(levels)": s}
for m,label in [(32768,"dense"),(256,"sparse n'=256"),(128,"sparse+packed(2 sig)")]:
    fk = factored_keys(m)
    print(f"  {label:<22} size {m:>6}: {fk['rotations(keys)']:>3} rotation keys, depth {fk['depth(levels)']}")
print("  => factored regime: keys grow ~2*log2(size). Sparse cuts size N/2->n'")
print("     (15 -> 8 levels here); packing two signals keeps ONE transform for TWO.")