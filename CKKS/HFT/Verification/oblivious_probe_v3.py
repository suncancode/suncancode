"""
HUONG 3 PROBE v3 (plaintext, chay local). Cau hoi: ngu canh nhieu phut +
chuan hoa baseline tung benh nhan co dua kernel OBLIVIOUS len ngang baseline,
o muc CANH TRANH (~0.80+) khong? Tat ca van FHE-friendly.

Them so voi v2:
  (1) NGU CANH +/-K phut (concat dac trung phut ke trong cung benh nhan).
  (2) Tru baseline tung benh nhan (client tinh ca dem -> FHE-free).
  (3) Ablation [B]: short-lag AC (nhip) vs long-lag envelope (chu ky apnea).
Danh gia: GroupKFold theo benh nhan, classifier tuyen tinh (= FHE-friendly).
"""
import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

FS=100; WIN=60*FS; CONTEXT=2          # +/- 2 minutes

def bandpass(x,lo,hi,fs=FS,order=3):
    b,a=butter(order,[lo/(fs/2),hi/(fs/2)],btype='band'); return filtfilt(b,a,x)

# ---- [A] baseline R-peak/HRV ----
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
    rr=np.diff(pk)/FS*1000.0; t=np.cumsum(rr)/1000.0; tu=np.arange(t[0],t[-1],0.25); lf=hf=0.0
    if len(tu)>=8:
        rri=np.interp(tu,t,rr)-np.mean(np.interp(tu,t,rr)); P=np.abs(np.fft.rfft(rri))**2
        fr=np.fft.rfftfreq(len(rri),0.25); lf=P[(fr>=0.04)&(fr<0.15)].sum(); hf=P[(fr>=0.15)&(fr<0.4)].sum()
    return np.array([np.mean(rr),np.std(rr),np.sqrt(np.mean(np.diff(rr)**2)),
                     np.mean(np.abs(np.diff(rr))>50)*100,lf,hf,lf/(hf+1e-9)])

# ---- [B] oblivious autocorr: split short-lag (HR) vs long-lag envelope (apnea cycle) ----
def ac_short(x):                       # heart-period autocorr, fixed lags
    f=bandpass(x,0.5,8); f=f-f.mean(); n=len(f); den=np.sum(f*f)+1e-9
    return np.array([np.sum(f[:n-l]*f[l:])/den for l in range(40,151,5)])
def ac_envlong(x):                     # bradycardia-tachycardia cyclicity, long lags
    f=bandpass(x,0.5,8); env=bandpass(f*f,0.01,0.5); env=env-env.mean(); n=len(env); de=np.sum(env*env)+1e-9
    return np.array([np.sum(env[:n-L]*env[L:])/de for L in range(10*FS,45*FS+1,5*FS)])
def autocorr_full(x): return np.concatenate([ac_short(x),ac_envlong(x)])

# ---- context + per-patient baseline ----
def add_context(F,groups,K=CONTEXT):
    F=np.asarray(F); out=[]
    for j in range(len(F)):
        block=[]
        for d in range(-K,K+1):
            k=j+d
            block.append(F[k] if 0<=k<len(F) and groups[k]==groups[j] else np.zeros(F.shape[1]))
        out.append(np.concatenate(block))
    return np.array(out)
def patient_center(F,groups):          # subtract per-patient mean (client-side, FHE-free)
    F=np.asarray(F).copy()
    for g in set(groups):
        m=groups==g; F[m]-=F[m].mean(0)
    return F

# ---- loader ----
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

# ---- synthetic (only to test this script) ----
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
    print(f"  {name:<36} GroupKFold AUC = {auc:.3f}   [{F.shape[1]} feats]")
    return auc

print("Loading data...")
# segs,labs,grp=load_synth()
segs,labs,grp=load_dataset_apnea(r"D:\sun\WOLLONGONG\RA\Code\data\apnea-ecg")
print(f"{len(segs)} segments, {labs.mean()*100:.0f}% apnea, {len(set(grp))} patients\n")

FA=[hrv_features(s) for s in segs]
SH=[ac_short(s) for s in segs]; EN=[ac_envlong(s) for s in segs]; FB=[np.concatenate([a,b]) for a,b in zip(SH,EN)]

print("Honest patient-wise AUC (linear = FHE-friendly):")
a0=ev(FA,labs,grp,"[A] baseline, no context")
b0=ev(FB,labs,grp,"[B] oblivious, no context")
print("  -- add multi-minute context --")
ac=ev(add_context(FA,grp),labs,grp,"[A] baseline + context")
bc=ev(add_context(FB,grp),labs,grp,"[B] oblivious + context")
print("  -- + per-patient baseline subtraction --")
bcp=ev(add_context(patient_center(FB,grp),grp),labs,grp,"[B] oblivious + context + pat-center")
print("  -- ablation: where is [B]'s signal? --")
ev(add_context(patient_center(SH,grp),grp),labs,grp,"   short-lag AC only (heart period)")
ev(add_context(patient_center(EN,grp),grp),labs,grp,"   long-lag envelope only (apnea cycle)")
print(f"\nDECISION: best oblivious={max(bc,bcp):.3f} vs best baseline={max(a0,ac):.3f}")
print("  if best [B] ~ best [A] AND >=~0.80 -> oblivious kernel viable & competitive -> design FHE version")
print("  if [B] tracks [A] but both <0.80   -> need richer FHE-friendly model (poly net), features ok")
print("  if [B] still trails [A] by >0.05   -> per-beat timing matters -> approx R-peak kernel")