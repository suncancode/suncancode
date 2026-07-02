"""
HUONG 3 PROBE v2 (plaintext, chay local).
Sua 3 diem so voi v1:
  (1) GroupKFold theo benh nhan  -> so trung thuc, khong ro ri.
  (2) Chuan hoa z-score theo tung ban ghi (client lam truoc khi ma hoa -> FHE-free).
  (3) Dac trung [B] CHI dung gia tri autocorr tai cac lag CO DINH (oblivious thuc su,
      bo argmax). + autocorr lag-dai cua duong bao nang luong de bat chu ky
      bradycardia-tachycardia (dau hieu apnea). Classifier: LogReg (tuyen tinh = FHE-friendly).
"""
import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GroupKFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

FS=100; WIN=60*FS

def bandpass(x,lo,hi,fs=FS,order=3):
    b,a=butter(order,[lo/(fs/2),hi/(fs/2)],btype='band'); return filtfilt(b,a,x)

# ---------------- [A] baseline R-peak/HRV (data-dependent) ----------------
def detect_rpeaks(x):
    f=bandpass(x,5,15); d=np.diff(f,prepend=f[0]); sq=d*d
    w=int(0.15*FS); integ=np.convolve(sq,np.ones(w)/w,'same')
    thr=0.3*np.mean(integ)+0.2*np.max(integ); pk=[]; i=1; refr=int(0.25*FS)
    while i<len(integ)-1:
        if integ[i]>thr and integ[i]>=integ[i-1] and integ[i]>integ[i+1]: pk.append(i); i+=refr
        else: i+=1
    return np.array(pk)
def hrv_features(x):
    pk=detect_rpeaks(x)
    if len(pk)<4: return np.zeros(7)
    rr=np.diff(pk)/FS*1000.0
    t=np.cumsum(rr)/1000.0; tu=np.arange(t[0],t[-1],0.25)
    lf=hf=0.0
    if len(tu)>=8:
        rri=np.interp(tu,t,rr)-np.mean(np.interp(tu,t,rr))
        P=np.abs(np.fft.rfft(rri))**2; fr=np.fft.rfftfreq(len(rri),0.25)
        lf=P[(fr>=0.04)&(fr<0.15)].sum(); hf=P[(fr>=0.15)&(fr<0.4)].sum()
    return np.array([np.mean(rr),np.std(rr),np.sqrt(np.mean(np.diff(rr)**2)),
                     np.mean(np.abs(np.diff(rr))>50)*100, lf, hf, lf/(hf+1e-9)])

# ---------------- [B] OBLIVIOUS autocorr (fixed lags only, no argmax) ----------------
def autocorr_features(x):
    f=bandpass(x,0.5,8); f=f-f.mean()
    n=len(f); denom=np.sum(f*f)+1e-9
    # AC at FIXED lags covering heart periods 0.4-1.5s  (oblivious: sum(f*rot(f,l)))
    lags=np.arange(40,151,5)                       # 23 fixed lags
    ac=np.array([np.sum(f[:n-l]*f[l:])/denom for l in lags])
    # long-lag AC of ENERGY ENVELOPE -> bradycardia-tachycardia cyclicity (~10-45s)
    env=bandpass(f*f,0.01,0.5); env=env-env.mean(); de=np.sum(env*env)+1e-9
    Llags=np.arange(10*FS,45*FS+1,5*FS)            # 8 fixed long lags
    eac=np.array([np.sum(env[:n-L]*env[L:])/de for L in Llags])
    # a few fixed band powers (Parseval, oblivious)
    bp=[np.mean(bandpass(x,lo,hi)**2) for lo,hi in [(0.5,4),(4,15)]]
    return np.concatenate([ac,eac,bp])

# ---------------- loader: per-record z-norm + return groups ----------------
def load_dataset_apnea(data_dir, records=None):
    import wfdb
    if records is None:
        records=[f"a{i:02d}" for i in range(1,21)]+[f"b{i:02d}" for i in range(1,6)]+[f"c{i:02d}" for i in range(1,11)]
    X=[];y=[];g=[]
    for gi,rec in enumerate(records):
        try:
            sig=wfdb.rdrecord(f"{data_dir}/{rec}").p_signal[:,0]
            ann=wfdb.rdann(f"{data_dir}/{rec}",'apn')
        except Exception as e:
            print(f"  skip {rec}: {e}"); continue
        sig=(sig-np.mean(sig))/(np.std(sig)+1e-9)        # per-record z-norm (client-side)
        for i,sym in enumerate(ann.symbol):
            s=i*WIN
            if s+WIN<=len(sig) and np.std(sig[s:s+WIN])>1e-6:
                X.append(sig[s:s+WIN]); y.append(1 if sym=='A' else 0); g.append(gi)
    return X,np.array(y),np.array(g)

# ---------------- synthetic (only to TEST this script here) ----------------
def make_synth(apnea,seed):
    rng=np.random.default_rng(seed); n=WIN; t=np.arange(n)/FS; hr=70/60
    mod=(0.18*np.sin(2*np.pi*0.03*t) if apnea else 0.06*np.sin(2*np.pi*0.25*t))+0.03*rng.standard_normal(n)
    ph=2*np.pi*np.cumsum(hr*(1+mod))/FS; beats=(np.mod(ph,2*np.pi)<0.25).astype(float)
    q=np.exp(-0.5*(np.arange(-15,16)/2.5)**2); q[15]+=2
    return np.convolve(beats,q,'same')+0.05*rng.standard_normal(n)
def load_synth():
    X=[];y=[];g=[]
    for p in range(12):                              # 12 fake patients
        for k in range(20):
            X.append(make_synth(False,p*100+k)); y.append(0); g.append(p)
            X.append(make_synth(True ,p*100+k+50)); y.append(1); g.append(p)
    return X,np.array(y),np.array(g)

def evaluate(F,y,groups,name):
    F=np.nan_to_num(np.array(F))
    clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced'))
    # honest: GroupKFold by patient ; vs leaky: StratifiedKFold random
    gk=GroupKFold(n_splits=5); sk=StratifiedKFold(5,shuffle=True,random_state=0)
    auc_g=cross_val_score(clf,F,y,cv=gk.split(F,y,groups),scoring='roc_auc').mean()
    acc_g=cross_val_score(clf,F,y,cv=gk.split(F,y,groups),scoring='accuracy').mean()
    auc_r=cross_val_score(clf,F,y,cv=sk,scoring='roc_auc').mean()
    print(f"  {name:<24} LogReg  GroupKFold: acc={acc_g:.3f} auc={auc_g:.3f}   (leaky random auc={auc_r:.3f})  [{F.shape[1]} feats]")

print("Loading data...")
# segs,labs,grp = load_synth()
segs,labs,grp = load_dataset_apnea(r"D:\sun\WOLLONGONG\RA\Code\data\apnea-ecg")   # <-- raw string
print(f"{len(segs)} segments, {labs.mean()*100:.0f}% apnea, {len(set(grp))} patients\n")
print("Honest patient-wise evaluation (FHE-relevant = linear classifier):")
evaluate([hrv_features(s)      for s in segs], labs, grp, "[A] baseline R-peak/HRV")
evaluate([autocorr_features(s) for s in segs], labs, grp, "[B] oblivious autocorr")
print("\nWHAT TO READ:")
print("  GroupKFold auc is the TRUTH. If [B] auc ~ [A] auc -> oblivious kernel viable.")
print("  Big drop from leaky->GroupKFold = patient-specific signal (expected on this dataset).")