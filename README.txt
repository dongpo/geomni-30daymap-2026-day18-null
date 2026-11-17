Day18 — NULL｜連線的空白，還是資料的空白？
公開專案（依使用者授權）。Facebook文案尚未批准，未啟用GitHub Pages。

開啟地圖：在專案目錄執行 python3 -m http.server 8000，瀏覽 http://localhost:8000。
HTML與本機資料俱全，FAO涵蓋背景需連網讀取官方WMTS；失敗會在介面提示，不能判為無涵蓋。

重現：在虛擬環境 pip install -r requirements.txt；另需curl與osmium。
python3 scripts/acquire_ais.py
python3 scripts/build_context.py
sh scripts/extract_roads.sh
已保留經篩選OSM PBF與GeoJSON、AIS LERC圖磚、解碼值與valid mask。
官方FAO圖磚未打包；evidence/signal-map.png為本機審稿截圖，不代表已取得公開再利用授權。

來源與限制見 DATA-NOTES.txt，QA見evidence。資料分別適用來源授權，不以單一程式授權覆蓋。
AIS衍生資料：Global Fishing Watch CC BY-NC 4.0，僅非商業用途；非GFW背書。
OSM：© OpenStreetMap contributors，ODbL。國土測繪中心：政府資料開放授權條款第1版。Natural Earth：公共領域。
FAO/GSMA：© GSMA Coverage Maps Service 2026，公開再利用範圍尚待核實。
Leaflet：保留vendor內上游授權註記。
