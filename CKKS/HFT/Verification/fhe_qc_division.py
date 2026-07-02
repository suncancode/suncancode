"""
HUONG 3 -- can quality-control rescue a PURE-FHE (no-leak) normalization?
The 5e13 energy range is from artifact windows (signal loss / saturation),
which the apnea literature excludes anyway. After QC the range should shrink;
then standard FHE division (poly-approx of 1/d over a bounded range) may work.
Compares, on the QC'd set:  exact 1/energy  vs  polynomial-approx 1/energy.
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
    n=len(e); raw=np.array([np.sum(e[:n-L]*e[L:]) for L in LAGS]); return raw,np.sum(e*e)
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
RAW=np.array(RAW); EN=np.array(EN); labs=np.array(labs); grp=np.array(grp)

print("Energy percentiles:", {p:f"{np.percentile(EN,p):.3g}" for p in [1,5,25,50,75,95,99]})

def auc_of(F,y,g):
    F=np.nan_to_num(F); a=[]
    for tr,te in GroupKFold(5).split(F,y,g):
        m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=4000,class_weight='balanced')).fit(F[tr],y[tr])
        a.append(roc_auc_score(y[te],m.predict_proba(F[te])[:,1]))
    return np.mean(a)

for lo,hi in [(0,100),(2,98),(5,95)]:
    a=np.percentile(EN,lo); b=np.percentile(EN,hi); keep=(EN>=a)&(EN<=b)
    R=RAW[keep]; E=EN[keep]; Y=labs[keep]; G=grp[keep]
    rng_ratio=E.max()/E.min()
    # exact
    Fex=add_context(R/E[:,None],G); auc_ex=auc_of(Fex,Y,G)
    # polynomial approx of 1/d over [a,b], degrees 3/5/7 (least-squares on log-spaced grid)
    grid=np.exp(np.linspace(np.log(a),np.log(b),400)); 
    best=None
    for deg in [3,5,7,9]:
        c=np.polyfit(grid,1.0/grid,deg); inv=np.polyval(c,E)
        Fp=add_context(R*inv[:,None],G); ap=auc_of(Fp,Y,G)
        if best is None or ap>best[1]: best=(deg,ap)
    print(f"QC [{lo:>2}-{hi}%]: kept {keep.mean()*100:4.1f}%  range_ratio={rng_ratio:.1f}  "
          f"exact AUC={auc_ex:.3f}  best-poly-approx AUC={best[1]:.3f} (deg{best[0]})")
print("\nIf a QC level gives poly-approx ~ exact ~0.88 -> PURE FHE division works (no leak, Path 1).")
print("Else -> Path 2 (client 1/energy) is the clean choice; exact 0.891, benign leak.")