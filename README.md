# sapporo_population
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/shimat/sapporo_population/main/main.py)

Streamlit study: visualizing the population of each Sapporo area

## Reference Source

- https://ckan.pf-sapporo.jp/dataset/juuki_8/resource/17075eca-d5f3-4f2c-9fd7-89c155a63fa0
  - DATA-SMART CITY SAPPORO 町名・条丁目別世帯数及び男女別人口 令和3年（2021年）4月1日現在
- https://ckan.pf-sapporo.jp/dataset/juuki_9/resource/51f660d2-1373-47ab-ad8b-834d75a4be2f
  - DATA-SMART CITY SAPPORO 町名、条丁目別年齢（5歳階級）別人口 令和２年（2020年）10月1日現在
- https://geoshape.ex.nii.ac.jp/ka/ https://www.e-stat.go.jp/terms-of-use
  - 『国勢調査町丁・字等別境界データセット』（CODH作成） 「平成27年国勢調査町丁・字等別境界データ」（NICT加工）
  - https://github.com/shimat/geodata

### TopoJSON -> GeoJSON
https://github.com/topojson/topojson-client/blob/master/README.md#topo2geo

```sh
sudo npm install -g topojson-client

topo2geo town < 清田区.topojson
mv town 清田区_geo.json
```

## Installation
### geopandas (Windows)
https://towardsdatascience.com/geopandas-installation-the-easy-way-for-windows-31a666b3610f
```sh
pip install .\GDAL-3.2.3-cp39-cp39-win_amd64.whl
pip install .\pyproj-3.0.1-cp39-cp39-win_amd64.whl
pip install .\Fiona-1.8.19-cp39-cp39-win_amd64.whl
pip install .\Shapely-1.7.1-cp39-cp39-win_amd64.whl
pip install .\geopandas-0.9.0-py3-none-any.whl
```

### geopandas (Streamlit deployment environment)
https://discuss.streamlit.io/t/shared-streamlit-with-geopandas/7277/7

requirements.txt
```
streamlit
fiona
geopandas
```

packages.txt
```
gdal-bin
python-rtree
```
