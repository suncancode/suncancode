"""
HUONG 3 -- FINAL FHE GATE + WEIGHT EXPORT.
(a) Does DIVISION-FREE autocorrelation (no /energy) keep the 0.927 AUC?  -> must avoid division in FHE.
(b) Fold StandardScaler into linear weights -> the exact linear form FHE will run.
(c) Export FIR coeffs, lag list, context, and folded weights -> for OpenFHE prototype.
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
H_QRS=fir_bandpass(5,15,101); H_ENV=fir_lowpass(0.5,301)
LAGS=list(range(10*FS,45*FS+1,3*FS))

def env_autocorr(x, normalize):
    q=cfir(x,H_QRS); e=q*q; e=e-e.mean(); e=cfir(e,H_ENV); e=e-e.mean()
    n=len(e); raw=np.array([np.sum(e[:n-L]*e[L:]) for L in LAGS])
    return raw/(np.sum(e*e)+1e-9) if normalize else raw    # FHE-legal version: normalize=False
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
withheld=[f"x{i:02d}" for i in range(1,36)]

print("Loading released...")
# segs,labs,grp=load_synth()
segs,labs,grp=load(DATA,released)
print(f"{len(segs)} segments, {len(set(grp))} patients\n")

def gkf_auc(F):
    F=np.nan_to_num(F); a=[]
    for tr,te in GroupKFold(5).split(F,labs,grp):
        m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=4000,class_weight='balanced')).fit(F[tr],labs[tr])
        a.append(roc_auc_score(labs[te],m.predict_proba(F[te])[:,1]))
    return np.mean(a)

Fn=add_context([env_autocorr(s,True ) for s in segs],grp)   # normalized (not FHE-legal)
Fr=add_context([env_autocorr(s,False) for s in segs],grp)   # division-free (FHE-legal)
print(f"(a) normalized (with /energy)  GroupKFold AUC = {gkf_auc(Fn):.3f}")
print(f"    division-free (FHE-LEGAL)  GroupKFold AUC = {gkf_auc(Fr):.3f}  <- must stay close")

# (b) train on FHE-legal features, fold StandardScaler -> single linear (W,B)
sc=StandardScaler().fit(np.nan_to_num(Fr))
lr=LogisticRegression(max_iter=4000,class_weight='balanced').fit(sc.transform(np.nan_to_num(Fr)),labs)
W = lr.coef_[0]/sc.scale_
B = lr.intercept_[0] - np.sum(lr.coef_[0]*sc.mean_/sc.scale_)
# sanity: folded linear == pipeline
logit_fold = np.nan_to_num(Fr)@W + B
logit_pipe = sc.transform(np.nan_to_num(Fr))@lr.coef_[0] + lr.intercept_[0]
print(f"(b) fold scaler into (W,B): max|fold-pipe| = {np.max(np.abs(logit_fold-logit_pipe)):.2e}  (should ~0)")

# (c) official withheld with FHE-legal features + folded linear
print("\n(c) Official withheld (FHE-legal, folded linear):")
try:
    Xw,yw,gw=load(DATA,withheld)
    if len(Xw)>0:
        Fw=np.nan_to_num(add_context([env_autocorr(s,False) for s in Xw],gw))
        print(f"    withheld AUC = {roc_auc_score(yw, Fw@W+B):.3f}")
except Exception as e: print(f"    skipped ({e})")

np.savez("fhe_apnea_model.npz", H_QRS=H_QRS, H_ENV=H_ENV, LAGS=np.array(LAGS),
         CONTEXT=CONTEXT, FS=FS, WIN=WIN, W=W, B=B, n_lags=len(LAGS))
print("\nExported -> fhe_apnea_model.npz  (FIR coeffs, lags, context, folded weights W,B for OpenFHE)")