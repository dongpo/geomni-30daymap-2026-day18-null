import json,collections
from pathlib import Path
from shapely.geometry import shape,mapping
p=Path(__file__).resolve().parents[1]
j=json.loads((p/'source/roads.geojson').read_text());out=[];excluded=collections.Counter()
allowed={'motorway','trunk','primary','secondary','motorway_link','trunk_link','primary_link','secondary_link'}
for f in j['features']:
 if f['geometry']['type'] not in ('LineString','MultiLineString') or f['properties'].get('highway') not in allowed:
  excluded[f['geometry']['type']]+=1;continue
 g=shape(f['geometry'])
 if g.is_empty or not g.is_valid:excluded['invalid']+=1;continue
 out.append({'type':'Feature','properties':{'highway':f['properties']['highway'],'name':f['properties'].get('name','')},'geometry':mapping(g.simplify(.00015,preserve_topology=True))})
(p/'data/roads.geojson').write_text(json.dumps({'type':'FeatureCollection','features':out},ensure_ascii=False,separators=(',',':')))
qa={'exported_objects':len(j['features']),'road_lines':len(out),'excluded':dict(excluded),'simplification_degrees':.00015,'scope':sorted(allowed),'source_file':'outputs/day11-spatial-v4/source/taiwan-261109.osm.pbf'}
(p/'evidence/roads-qa.json').write_text(json.dumps(qa,indent=2));print(qa)
s=(p/'DATA-NOTES.txt').read_text();s=s.replace('84,529 個道路物件通過幾何有效性檢查，未去掉任何無效物件（本批無無效物件）。',f'osmium 匯出含參照節點共84,529物件；篩除點與面後保留{len(out):,}條指定道路線形，通過幾何有效性檢查。不能把參照節點算成道路數。');(p/'DATA-NOTES.txt').write_text(s)
