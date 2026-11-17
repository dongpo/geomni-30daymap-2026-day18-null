import concurrent.futures, subprocess, sys

import lerc, numpy as np
from pathlib import Path
root=Path(__file__).resolve().parents[1]
base="https://tiledimageservices7.arcgis.com/rUSNqhFNeFnLs98e/arcgis/rest/services/vessel_presence_hours_yearly_v02/ImageServer"
def get(rc):
 r,c=rc
 out=root/"source"/f"ais2024_{r}_{c}.lerc"
 subprocess.run(["curl","--silent","--show-error","--fail","--retry","2","--max-time","45",f"{base}/tile/7/{r}/{c}?sliceId=4","-o",str(out)],check=True)
 west=-180+c*2.56; north=90-r*2.56
 code,arr,valid=lerc.decode(out.read_bytes())
 if code!=0: raise RuntimeError(f"LERC decode failed {code}")
 np.savez_compressed(out.with_suffix(".npz"),values=arr,valid=valid)

 return f"{r},{c}: {out.stat().st_size} bytes"
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for msg in ex.map(get,[(r,c) for r in range(24,28) for c in range(116,119)]): print(msg,flush=True)
