"""
HUONG 3 -- resolve the ESSENTIAL normalization for FHE.
Normalized AC (per-window /energy) = 0.891 but division is not FHE-native.
Test which FHE-compatible normalization preserves AUC:
  P1: homomorphic-style 1/x via Newton-Raphson (fixed init, 3 iters) -> pure FHE, +depth
  P3: per-RECORD energy normalization (plaintext constant) -> FHE-free, minimal leak
(P2 = client sends 1/energy plaintext = EXACT 0.891, no test needed.)
Also report denominator range -> how hard the division is.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold

FS=100; WIN=60*FS; CONTEXT=2
def fir_bandpass(lo,hi,L,fs=FS):
    m=np.arange(L)-(L-1)/2; h=(np.sinc(2*hi/fs*m)-np.sinc(2*lo/fs*m))*np.hamming(L); return h-h.mean()
def fir_lowpass(fc,L,fs=FS):
    m=np.arange(L)-(L-1)/2; h=np.sinc(2*fc/fs*m)*np.hamming(L); return h/np.sum(h)
def cfir(x,h): return np.convolve(x,h,'same')
H_QRS=fir_bandpass(5,15,101); H_ENV=fir_lowpass(0.5,301); LAGS=list(range(10*FS,45*FS+1,3*FS))

def raw_ac_and_energy(x):
    q=cfir(x,H_QRS); e=q*q; e=e-e.mean(); e=cfir(e,H_ENV); e=e-e.mean()
    raw=np.array([np.sum(e[:n-L]*e[L:]) for L,n in [(L,len(e)) for L in LAGS]])
    return raw, np.sum(e*e)
def add_context(F,groups,K=CONTEXT):
    F=np.asarray(F); out=[]
    for j in range(len(F)):
        blk=[F[j+d] if 0<=j+d<len(F) and groups[j+d]==groups[j] else np.zeros(F.shape[1]) for d in range(-K,K+1)]
        out.append(np.concatenate(blk))
    return np.array(out)

def load(data_dir,records):
    import wfdb; X=[];y=[];g=[]
    for gi,rec in enumerate(records):
        try:
            sig=wfdb.rdrecord(f"{data_dir}/{rec}").p_signal[:,0]; ann=wfdb.rdann(f"{data_dir}/{rec}",'apn')
        except Exception as e: print(f"  skip {rec}: {e}"); continue
        sig=(sig-np.mean(sig))/(np.std(sig)+1e-9)
        for i,sym in enumerate(ann.symbol):
            s=i*WIN
            if s+WIN<=len(sig) and np.std(sig[s:s+WIN])>1e-6:
                X.append(sig[s:s+WIN]); y.append(1 if sym in('A','a') else 0); g.append(gi)
    return X,np.array(y),np.array(g)
def make_synth(ap,seed):
    rng=np.random.default_rng(seed); n=WIN; t=np.arange(n)/FS; hr=70/60
    mod=(0.18*np.sin(2*np.pi*0.03*t) if ap else 0.06*np.sin(2*np.pi*0.25*t))+0.03*rng.standard_normal(n)
    ph=2*np.pi*np.cumsum(hr*(1+mod))/FS; b=(np.mod(ph,2*np.pi)<0.25).astype(float)
    q=np.exp(-0.5*(np.arange(-15,16)/2.5)**2); q[15]+=2
    return np.convolve(b,q,'same')+0.05*rng.standard_normal(n)
def load_synth():
    X=[];y=[];g=[]
    for p in range(12):
        for k in range(30): lab=k%2; X.append(make_synth(lab,p*200+k)); y.append(lab); g.append(p)
    return X,np.array(y),np.array(g)

DATA=r"D:\sun\WOLLONGONG\RA\Code\data\apnea-ecg"
released=[f"a{i:02d}" for i in range(1,21)]+[f"b{i:02d}" for i in range(1,6)]+[f"c{i:02d}" for i in range(1,11)]

print("Loading released...")
# segs,labs,grp=load_synth()
segs,labs,grp=load(DATA,released)
RAW=[];EN=[]
for s in segs: r,en=raw_ac_and_energy(s); RAW.append(r); EN.append(en)
RAW=np.array(RAW); EN=np.array(EN)
print(f"{len(segs)} segments, {len(set(grp))} patients")
print(f"denominator (window energy) range: min={EN.min():.3g} max={EN.max():.3g} ratio={EN.max()/EN.min():.1f} median={np.median(EN):.3g}\n")

def auc_of(F):
    F=np.nan_to_num(F); a=[]
    for tr,te in GroupKFold(5).split(F,labs,grp):
        m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=4000,class_weight='balanced')).fit(F[tr],labs[tr])
        a.append(roc_auc_score(labs[te],m.predict_proba(F[te])[:,1]))
    return np.mean(a)

# baseline: exact per-window normalization
Fexact=add_context(RAW/EN[:,None],grp)
print(f"per-window exact /energy (=P2 client-assisted) AUC = {auc_of(Fexact):.3f}")

# P1: Newton-Raphson 1/x, fixed init from training median, 3 iters (homomorphic-friendly)
d0=np.median(EN); y0=1.0/d0
def newton_inv(d,iters=3,y0=y0):
    y=np.full_like(d,y0)
    for _ in range(iters): y=y*(2-d*y)
    return y
for it in [2,3,4]:
    inv=newton_inv(EN,it); F=add_context(RAW*inv[:,None],grp)
    print(f"P1 Newton 1/x ({it} iters, fixed init)         AUC = {auc_of(F):.3f}")

# P3: per-record energy normalization (plaintext constant per patient)
inv_rec=np.zeros_like(EN)
for g in set(grp):
    m=grp==g; inv_rec[m]=1.0/np.mean(EN[m])
F3=add_context(RAW*inv_rec[:,None],grp)
print(f"P3 per-record /avg-energy (FHE-free)          AUC = {auc_of(F3):.3f}")
print("\nPICK: highest AUC that is FHE-compatible. Newton needs denom ratio not too huge;")
print("if P1>=~0.88 -> pure FHE (no leak). Else P2 (client 1/energy, benign leak) guarantees 0.891.")