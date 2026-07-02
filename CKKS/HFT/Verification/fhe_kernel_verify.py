"""
HUONG 3 -- VERIFY the surprising 0.891 before locking the kernel.
Kernel = FIR envelope long-lag autocorrelation ONLY (short-lag dropped: it hurt).
Checks:
  (1) GroupKFold per-fold AUC + mean/std (variance honesty)
  (2) LABEL-SHUFFLE negative control -> MUST drop to ~0.5 (rules out leakage)
  (3) OFFICIAL split: released(a/b/c) train -> withheld(x) test  (citable vs literature)
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

FS=100; WIN=60*FS; CONTEXT=2

def fir_bandpass(lo,hi,L,fs=FS):
    m=np.arange(L)-(L-1)/2; h=(np.sinc(2*hi/fs*m)-np.sinc(2*lo/fs*m))*np.hamming(L); return h-h.mean()
def fir_lowpass(fc,L,fs=FS):
    m=np.arange(L)-(L-1)/2; h=np.sinc(2*fc/fs*m)*np.hamming(L); return h/np.sum(h)
def cfir(x,h): return np.convolve(x,h,'same')
H_QRS=fir_bandpass(5,15,101); H_ENV=fir_lowpass(0.5,301)

def env_autocorr(x):                       # THE LOCKED KERNEL (FHE-compatible, depth~5)
    q=cfir(x,H_QRS); e=q*q; e=e-e.mean(); e=cfir(e,H_ENV); e=e-e.mean()
    n=len(e); de=np.sum(e*e)+1e-9
    return np.array([np.sum(e[:n-L]*e[L:])/de for L in range(10*FS,45*FS+1,3*FS)])
def add_context(F,groups,K=CONTEXT):
    F=np.asarray(F); out=[]
    for j in range(len(F)):
        blk=[F[j+d] if 0<=j+d<len(F) and groups[j+d]==groups[j] else np.zeros(F.shape[1]) for d in range(-K,K+1)]
        out.append(np.concatenate(blk))
    return np.array(out)

def load(data_dir, records):
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

# synthetic test (shuffle control should collapse this to ~0.5)
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

def clf(): return make_pipeline(StandardScaler(),LogisticRegression(max_iter=4000,class_weight='balanced'))

DATA=r"D:\sun\WOLLONGONG\RA\Code\data\apnea-ecg"
released=[f"a{i:02d}" for i in range(1,21)]+[f"b{i:02d}" for i in range(1,6)]+[f"c{i:02d}" for i in range(1,11)]
withheld=[f"x{i:02d}" for i in range(1,36)]

print("Loading released set...")
# segs,labs,grp=load_synth()
segs,labs,grp=load(DATA,released)
print(f"{len(segs)} segments, {labs.mean()*100:.0f}% apnea, {len(set(grp))} patients\n")
F=add_context([env_autocorr(s) for s in segs],grp); F=np.nan_to_num(F)

# (1) per-fold AUC
aucs=[]
for tr,te in GroupKFold(5).split(F,labs,grp):
    m=clf().fit(F[tr],labs[tr]); aucs.append(roc_auc_score(labs[te],m.predict_proba(F[te])[:,1]))
print(f"(1) GroupKFold per-fold AUC = {[f'{a:.3f}' for a in aucs]}")
print(f"    mean={np.mean(aucs):.3f}  std={np.std(aucs):.3f}")

# (2) LABEL-SHUFFLE negative control (MUST be ~0.5)
rng=np.random.default_rng(0); ysh=rng.permutation(labs); sh=[]
for tr,te in GroupKFold(5).split(F,ysh,grp):
    m=clf().fit(F[tr],ysh[tr]); sh.append(roc_auc_score(ysh[te],m.predict_proba(F[te])[:,1]))
print(f"(2) shuffled-label control AUC = {np.mean(sh):.3f}  (MUST be ~0.50; if high -> leakage)")

# (3) OFFICIAL split (only if withheld 'x' records exist)
print("\n(3) Official released->withheld split:")
try:
    Xw,yw,gw=load(DATA,withheld)
    if len(Xw)>0:
        Fw=np.nan_to_num(add_context([env_autocorr(s) for s in Xw],gw))
        m=clf().fit(F,labs)
        print(f"    withheld AUC = {roc_auc_score(yw, m.predict_proba(Fw)[:,1]):.3f}  ({len(Xw)} test segs)  <- citable vs literature")
    else:
        print("    withheld 'x' records not found -> download withheld set for the citable benchmark number")
except Exception as e:
    print(f"    withheld split skipped ({e})")