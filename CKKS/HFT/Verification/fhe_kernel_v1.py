"""
HUONG 3 -- FHE-COMPATIBLE KERNEL v1 (plaintext verification).
Bien kernel thang (envelope long-lag autocorrelation) thanh mach CHAY DUOC trong CKKS:
  - thay IIR butter/filtfilt  ->  FIR (tich chap = rotation, plaintext coeffs)
  - moi buoc chi gom add / multiply / rotation  -> khong bootstrapping
Kiem chung: FIR co giu AUC ~0.787 khong? + dem DO SAU NHAN (level budget).

FHE circuit & depth:
  x --FIR_bp(QRS)[depth1]--> square[depth1] --demean[0]--FIR_lp[depth1]--> env
  env --autocorr lag L: env*rot(env,L)[depth1] + SubSum[0]--> features
  features --linear classifier: dot = pmul + SubSum [depth1]
  => total multiplicative depth ~ 5  -> LEVELED, no bootstrapping.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

FS=100; WIN=60*FS; CONTEXT=2

# ---------- FIR filters (FHE: y = sum_d h[d]*rot(x,d), h plaintext) ----------
def fir_bandpass(lo,hi,L,fs=FS):
    m=np.arange(L)-(L-1)/2
    h=(np.sinc(2*hi/fs*m)-np.sinc(2*lo/fs*m))*np.hamming(L)
    return h-h.mean()                       # zero DC
def fir_lowpass(fc,L,fs=FS):
    m=np.arange(L)-(L-1)/2
    h=np.sinc(2*fc/fs*m)*np.hamming(L); return h/np.sum(h)
def cfir(x,h): return np.convolve(x,h,'same')   # FHE: rotations + plaintext mults (depth 1)

H_QRS=fir_bandpass(5,15,L=101)              # QRS band, FIR length 101
H_ENV=fir_lowpass(0.5,L=301)                # envelope low-pass, FIR length 301

# ---------- FHE-compatible oblivious features ----------
def envelope(x):
    q=cfir(x,H_QRS)                         # depth 1
    e=q*q                                   # depth 2  (energy)
    e=e-e.mean()                            # depth 2  (demean = SubSum, no mult)
    e=cfir(e,H_ENV)                         # depth 3  (smooth envelope)
    return e
def env_autocorr(x):                        # the WINNING signal (apnea cycle), FHE-cheap
    e=envelope(x); e=e-e.mean(); n=len(e); de=np.sum(e*e)+1e-9
    return np.array([np.sum(e[:n-L]*e[L:])/de for L in range(10*FS,45*FS+1,3*FS)])  # 12 long lags
def short_autocorr(x):                      # heart-period AC (the patient-leak part, for ablation)
    f=cfir(x,fir_bandpass(0.5,8,L=151)); f=f-f.mean(); n=len(f); d=np.sum(f*f)+1e-9
    return np.array([np.sum(f[:n-l]*f[l:])/d for l in range(40,151,5)])

def add_context(F,groups,K=CONTEXT):
    F=np.asarray(F); out=[]
    for j in range(len(F)):
        blk=[F[j+d] if 0<=j+d<len(F) and groups[j+d]==groups[j] else np.zeros(F.shape[1]) for d in range(-K,K+1)]
        out.append(np.concatenate(blk))
    return np.array(out)

# ---------- IIR reference (v3 winner) to confirm FIR doesn't lose AUC ----------
from scipy.signal import butter, filtfilt
def iir_env_autocorr(x):
    b,a=butter(3,[0.5/(FS/2),8/(FS/2)],'band'); f=filtfilt(b,a,x)
    b2,a2=butter(3,[0.01/(FS/2),0.5/(FS/2)],'band'); e=filtfilt(b2,a2,f*f); e-=e.mean()
    n=len(e); de=np.sum(e*e)+1e-9
    return np.array([np.sum(e[:n-L]*e[L:])/de for L in range(10*FS,45*FS+1,3*FS)])

# ---------- loader ----------
def load_dataset_apnea(data_dir, records=None):
    import wfdb
    if records is None:
        records=[f"a{i:02d}" for i in range(1,21)]+[f"b{i:02d}" for i in range(1,6)]+[f"c{i:02d}" for i in range(1,11)]
    X=[];y=[];g=[]
    for gi,rec in enumerate(records):
        try:
            sig=wfdb.rdrecord(f"{data_dir}/{rec}").p_signal[:,0]; ann=wfdb.rdann(f"{data_dir}/{rec}",'apn')
        except Exception as e: print(f"  skip {rec}: {e}"); continue
        sig=(sig-np.mean(sig))/(np.std(sig)+1e-9)
        for i,sym in enumerate(ann.symbol):
            s=i*WIN
            if s+WIN<=len(sig) and np.std(sig[s:s+WIN])>1e-6:
                X.append(sig[s:s+WIN]); y.append(1 if sym=='A' else 0); g.append(gi)
    return X,np.array(y),np.array(g)
# synthetic test
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

def ev(F,y,groups,name):
    F=np.nan_to_num(np.array(F)); clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=4000,class_weight='balanced'))
    auc=cross_val_score(clf,F,y,cv=GroupKFold(5).split(F,y,groups),scoring='roc_auc').mean()
    print(f"  {name:<42} AUC={auc:.3f}  [{F.shape[1]} feats]"); return auc

print("Loading data...")
# segs,labs,grp=load_synth()
segs,labs,grp=load_dataset_apnea(r"D:\sun\WOLLONGONG\RA\Code\data\apnea-ecg")
print(f"{len(segs)} segments, {labs.mean()*100:.0f}% apnea, {len(set(grp))} patients\n")
print("Does FHE-compatible FIR preserve the winning AUC? (patient-wise, linear)")
ev(add_context([iir_env_autocorr(s) for s in segs],grp),labs,grp,"IIR envelope-AC + context (v3 reference)")
EF=[env_autocorr(s) for s in segs]
ev(add_context(EF,grp),labs,grp,"FIR envelope-AC + context  <-- FHE-COMPATIBLE")
print("  -- does adding short-lag AC help, or just add patient leakage? --")
SF=[short_autocorr(s) for s in segs]
ev(add_context([np.concatenate([e,s]) for e,s in zip(EF,SF)],grp),labs,grp,"FIR (envelope + short-lag) + context")
print("\nIf 'FIR envelope-AC' ~ IIR reference -> the depth-~5 leveled FHE kernel is locked.")
print("FHE circuit: FIR_bp -> square -> demean -> FIR_lp -> long-lag autocorr -> linear. NO bootstrapping.")