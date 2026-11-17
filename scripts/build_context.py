import sys,json,math,shutil
from pathlib import Path

import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1]
a=np.full((1024,768),np.nan,dtype=np.float32)
for r in range(24,28):
 for c in range(116,119):
  d=np.load(root/'source'/f'ais2024_{r}_{c}.npz');v=d['values'].copy();v[~d['valid']]=np.nan
  a[(r-24)*256:(r-23)*256,(c-116)*256:(c-115)*256]=v
# Reproject the raster rows to Web Mercator for Leaflet imageOverlay.
north=28.56;south=18.32;west=116.96;east=124.64
merc=lambda lat:np.log(np.tan(np.pi/4+np.deg2rad(lat)/2))
ys=np.linspace(merc(north),merc(south),1024,endpoint=False)
lats=np.rad2deg(2*np.arctan(np.exp(ys))-np.pi/2)
rows=np.clip(((north-lats)/.01).astype(int),0,1023)
x=a[rows,:];positive=np.isfinite(x)&(x>0)
strength=np.clip(np.log1p(np.nan_to_num(x,nan=0))/np.log1p(1000),0,1)
rgba=np.zeros((1024,768,4),dtype=np.uint8)
rgba[:,:,0]=45+190*strength;rgba[:,:,1]=151+90*strength;rgba[:,:,2]=222-35*strength
rgba[:,:,3]=np.where(positive,55+195*strength,0)
Image.fromarray(rgba).save(root/'data/ais2024.png')
np.savez_compressed(root/'data/ais2024-grid.npz',values=a)
qa={'year':2024,'slice_id':4,'tiles':12,'shape':list(a.shape),'bounds':[west,south,east,north], 'valid_cells':int(np.isfinite(a).sum()),'positive_cells':int((a>0).sum()),'valid_zero_cells':int((a==0).sum()),'nodata_cells':int(np.isnan(a).sum()),'max_value':float(np.nanmax(a)), 'source_grid_degrees':.01,'display':'log1p saturation at 1000; valid-zero and NoData both visually transparent, never interpreted as no ships or no mobile signal'}
(root/'evidence/ais-qa.json').write_text(json.dumps(qa,indent=2))
# Lightweight sampling rows for click inspection. Keep original values and mask in NPZ.
points=[]
for r,c in np.argwhere(a>0):
 if r%3==0 and c%3==0:points.append([round(west+(int(c)+.5)*.01,3),round(north-(int(r)+.5)*.01,3),round(float(a[r,c]),2)])
print(json.dumps(qa,indent=2))
