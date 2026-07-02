"""
HUONG 3 PROBE (plaintext, chay local tren ECG cua ban).
Cau hoi: dac trung OBLIVIOUS / FHE-friendly (tinh thang tu ECG tho, KHONG
phat hien dinh-R) co giu duoc kha nang phan biet apnea ngang baseline R-peak/HRV?

So sanh 3 nhom dac trung tren CUNG mot classifier:
  [A] BASELINE (data-dependent, tran tren): R-peak -> RR -> HRV features
  [B] OBLIVIOUS-AUTOCORR: tu tuong quan cua ECG bandpass (multiply+SubSum -> FHE de)
  [C] OBLIVIOUS-SPECTRAL+ENVELOPE: band-power (Parseval) + envelope modulation

Moi dac trung oblivious deu chi gom add/multiply/rotation -> annotate chi phi FHE.
"""
import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

FS = 100            # Apnea-ECG sampling rate
WIN = 60*FS         # 1-min segment = 6000 samples

# ----------------------------------------------------------------------
# [A] BASELINE: lightweight R-peak detector (Pan-Tompkins-style) + HRV
#     DATA-DEPENDENT (thresholding/peak-finding) -> the FHE-hard part.
# ----------------------------------------------------------------------
def bandpass(x, lo, hi, fs=FS, order=3):
    b,a = butter(order, [lo/(fs/2), hi/(fs/2)], btype='band')
    return filtfilt(b,a,x)

def detect_rpeaks(x):
    f = bandpass(x, 5, 15)                 # QRS band
    d = np.diff(f, prepend=f[0])
    sq = d*d
    win = int(0.15*FS)
    integ = np.convolve(sq, np.ones(win)/win, mode='same')
    thr = 0.3*np.mean(integ) + 0.2*np.max(integ)
    peaks=[]; i=1; refractory=int(0.25*FS)
    while i < len(integ)-1:
        if integ[i]>thr and integ[i]>=integ[i-1] and integ[i]>integ[i+1]:
            peaks.append(i); i+=refractory
        else: i+=1
    return np.array(peaks)

def hrv_features(x):
    pk = detect_rpeaks(x)
    if len(pk) < 4: return np.zeros(8)
    rr = np.diff(pk)/FS*1000.0             # RR in ms
    meanNN=np.mean(rr); sdnn=np.std(rr)
    rmssd=np.sqrt(np.mean(np.diff(rr)**2))
    pnn50=np.mean(np.abs(np.diff(rr))>50)*100
    # crude freq-domain on interpolated RR
    t=np.cumsum(rr)/1000.0; tu=np.arange(t[0],t[-1],0.25)
    if len(tu)<8: return np.array([meanNN,sdnn,rmssd,pnn50,0,0,0,len(pk)])
    rri=np.interp(tu,t,rr); rri-=rri.mean()
    P=np.abs(np.fft.rfft(rri))**2; fr=np.fft.rfftfreq(len(rri),0.25)
    lf=P[(fr>=0.04)&(fr<0.15)].sum(); hf=P[(fr>=0.15)&(fr<0.4)].sum()
    lfhf=lf/(hf+1e-9)
    return np.array([meanNN,sdnn,rmssd,pnn50,lf,hf,lfhf,len(pk)])

# ----------------------------------------------------------------------
# [B] OBLIVIOUS-AUTOCORR: autocorrelation of bandpassed ECG.
#     FHE COST: bandpass=FIR (k rot, depth 1); autocorr lag-l = sum(x*rot(x,l))
#     = 1 pmult (depth1) + SubSum (log n rot). NO peak detection, NO branching.
# ----------------------------------------------------------------------
def autocorr_features(x):
    f = bandpass(x, 0.5, 8)                 # keep QRS rhythm + low modulation
    f = f - f.mean()
    n=len(f); ac=np.correlate(f,f,'full')[n-1:]/ (np.sum(f*f)+1e-9)
    # heart period typ 0.5-1.2s -> lags 50..120 samples; sample the AC curve there
    lags = np.arange(40, 160, 8)            # 15 features along the AC curve
    feats = ac[lags]
    # dominant-lag peak height + its lag (smooth surrogate of heart rate/regularity)
    region = ac[50:130]
    feats = np.concatenate([feats, [region.max(), region.argmax()+50, region.std()]])
    return feats

# ----------------------------------------------------------------------
# [C] OBLIVIOUS-SPECTRAL+ENVELOPE: band power (Parseval) + envelope modulation.
#     FHE COST: bandpass+square+SubSum per band (no DFT); envelope = square+LP.
# ----------------------------------------------------------------------
def spectral_envelope_features(x):
    feats=[]
    for lo,hi in [(0.5,4),(4,15),(15,40)]:  # rhythm / QRS / high
        bp=bandpass(x,lo,hi); feats.append(np.mean(bp*bp))      # band power
    env = bandpass(x,5,15); env = env*env                       # QRS energy envelope
    env = bandpass(env, 0.01, 0.5)          # modulation of QRS energy (resp/HRV proxy)
    for lo,hi in [(0.01,0.05),(0.05,0.15),(0.15,0.4)]:          # VLF/LF/HF of envelope
        m=bandpass(env,lo,hi); feats.append(np.mean(m*m))
    feats += [np.std(env), np.mean(np.abs(env))]
    return np.array(feats)

# ======================================================================
# SYNTHETIC ECG (chi de TEST script o may toi; ban thay bang data that)
# ======================================================================
def make_synth(apnea, fs=FS, dur=60, seed=0):
    rng=np.random.default_rng(seed); n=dur*fs; t=np.arange(n)/fs
    hr=70/60.0
    if apnea:   mod=0.18*np.sin(2*np.pi*0.03*t)+0.04*rng.standard_normal(n)  # strong VLF, low HF
    else:       mod=0.06*np.sin(2*np.pi*0.25*t)+0.02*rng.standard_normal(n)  # normal resp HF
    phase=2*np.pi*np.cumsum(hr*(1+mod))/fs
    beats=(np.mod(phase,2*np.pi)<0.25).astype(float)
    qrs=np.exp(-0.5*((np.arange(-15,16))/2.5)**2); qrs[15]+=2
    ecg=np.convolve(beats,qrs,'same')+0.05*rng.standard_normal(n)
    return ecg

def load_dataset_synth(n_per=120):
    X=[];y=[]
    for i in range(n_per):
        X.append(make_synth(False,seed=i)); y.append(0)
        X.append(make_synth(True ,seed=1000+i)); y.append(1)
    return X,np.array(y)

# ======================================================================
# REAL DATA loader for PhysioNet Apnea-ECG  ->  SWAP THIS IN.
# Needs: pip install wfdb. Records released set: a01..a20,b01..b05,c01..c10.
# Each record: .dat (ECG @100Hz) + .apn (per-minute 'A'=apnea / 'N'=normal).
# ======================================================================
def load_dataset_apnea(data_dir, records=None):
    import wfdb
    if records is None:
        records = [f"a{i:02d}" for i in range(1,21)] + \
                  [f"b{i:02d}" for i in range(1,6)]  + \
                  [f"c{i:02d}" for i in range(1,11)]
    X=[]; y=[]
    for rec in records:
        try:
            sig = wfdb.rdrecord(f"{data_dir}/{rec}").p_signal[:,0]
            ann = wfdb.rdann(f"{data_dir}/{rec}", 'apn')
        except Exception as e:
            print(f"  skip {rec}: {e}"); continue
        for i, sym in enumerate(ann.symbol):
            s = i*WIN
            if s+WIN <= len(sig):
                seg = sig[s:s+WIN]
                if np.std(seg) > 1e-6:                 # drop flat/lost segments
                    X.append(seg); y.append(1 if sym=='A' else 0)
    return X, np.array(y)

# ======================================================================
# RUN
# ======================================================================
def evaluate(segments, labels, featfn, name):
    F=np.array([featfn(s) for s in segments])
    F=np.nan_to_num(F)
    for clf,cn in [(RandomForestClassifier(n_estimators=200,random_state=0),'RF'),
                   (make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000)),'LogReg')]:
        acc=cross_val_score(clf,F,labels,cv=5,scoring='accuracy').mean()
        auc=cross_val_score(clf,F,labels,cv=5,scoring='roc_auc').mean()
        print(f"  {name:<26}{cn:<8} acc={acc:.3f}  auc={auc:.3f}  ({F.shape[1]} feats)")

print("Loading data...")
# ---- TO USE YOUR REAL DATA: comment the synthetic line, uncomment the apnea line ----
# segs, labs = load_dataset_synth()
segs, labs = load_dataset_apnea(r"D:\sun\WOLLONGONG\RA\Code\data\apnea-ecg")
print(f"{len(segs)} one-minute segments, {labs.mean()*100:.0f}% apnea\n")
print("Classification accuracy (5-fold CV):")
evaluate(segs, labs, hrv_features,            "[A] baseline R-peak/HRV")
evaluate(segs, labs, autocorr_features,       "[B] oblivious autocorr")
evaluate(segs, labs, spectral_envelope_features,"[C] oblivious spectral+env")
print("\nDECISION RULE:")
print("  if [B] or [C] ~ [A]  -> oblivious kernel viable; build the winner in CKKS (NO R-peak needed)")
print("  if [B],[C] << [A]    -> must approximate R-peak detection itself (harder kernel)")