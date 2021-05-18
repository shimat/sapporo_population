import math
import geopandas as gpd
import numpy as np
import pandas as pd
import pydeck
import streamlit as st
from converter import Converter
from data_loader import DataLoader


def tone_curve(x: float, a: float) -> int:
    return int(255 / (1 + math.exp(a * (127 - x * 256))))


COORDINATES_CSV_FILE_NAME = "data/位置情報_札幌.csv"
POPULATION_CSV_FILE_NAME = "data/jou202104.csv"
GEOJSON_URL_FORMAT = "https://raw.githubusercontent.com/shimat/geodata/main/geojson/{}_geo.json"
SAPPORO_WARDS = ('中央区', '東区', '西区', '南区', '北区', '白石区', '豊平区', '厚別区', '手稲区', '清田区')

st.set_page_config(layout="wide")
st.title(f'札幌の人口・世帯数集計')
ward = st.sidebar.selectbox('地域', SAPPORO_WARDS)
summary_item = st.sidebar.selectbox('集計項目', ('総数', '男', '女', '男女比', '世帯数',))

#df_coord = DataLoader.load_coordinates_csv(COORDINATES_CSV_FILE_NAME).copy()

df_pop = DataLoader.load_population_csv(POPULATION_CSV_FILE_NAME).copy()
df_pop = df_pop.dropna(how='any')
df_pop['女性比率'] = df_pop['女'] / (df_pop['男'] + df_pop['女'])
df_pop = df_pop.replace(np.inf, np.nan).fillna({'女性比率': 0})
# df_pop['男性比率'] = 1 - df_pop['女性比率']
df_pop['女性比率文字列'] = df_pop['女性比率'].apply(lambda x: "{:.2%}".format(x))


gdf = DataLoader.load_geopandas_from_url(GEOJSON_URL_FORMAT.format(f"札幌市{ward}")).copy()
gdf['S_NAME_漢数字'] = gdf['S_NAME'].apply(lambda x: Converter.replace_area_number_to_kansuji(x))
# st.write(gdf)


# GEOJsonは「三条４丁目」
# 人口CSVは「３条４丁目」
gdf_merged = gdf.merge(df_pop, left_on='S_NAME_漢数字', right_on='町条丁目_漢数字')  #, how='outer')

if summary_item == '男女比':
    a = 0.30
    gdf_merged['bg_color'] = gdf_merged['女性比率'].apply(lambda x: [tone_curve(x, a), 0, tone_curve(x, -a), 255])
if summary_item in ('総数', '男', '女', '世帯数'):
    ratio = gdf_merged[summary_item] / gdf_merged[summary_item].max()
    gdf_merged['bg_color'] = ratio.apply(lambda x: [255, (1-x) * 255, 0])
    gdf_merged['elevation'] = gdf_merged[summary_item]
# st.write(gdf_merged)

geojson_layer = pydeck.Layer(
    'GeoJsonLayer',
    gdf_merged,
    opacity=0.5,
    stroked=True,
    filled=True,
    extruded=True,
    wireframe=True,
    get_fill_color='bg_color',
    get_position="geometry",
    get_elevation='elevation',
    # get_line_color=[0, 0, 0, 192],
    get_line_width=1,
    pickable=True,
    get_color=[0, 255, 0],
    get_text='S_NAME',
)
st.pydeck_chart(pydeck.Deck(
    map_style='mapbox://styles/mapbox/streets-v11',
    initial_view_state=pydeck.ViewState(
        latitude=43.05,
        longitude=141.35,
        zoom=10.5,
        pitch=50,
    ),
    layers=[
        geojson_layer
    ],
    tooltip={"text": "{S_NAME}\n 総数: {総数} (男{男} / 女{女})\n女性比率: {女性比率文字列}\n世帯数: {世帯数}"}
))

st.write('人口', df_pop[df_pop['区別'] == ward])

st.markdown("""
<style>
div.xx-small-font dt,dd,a {
    font-size:xx-small !important;
}
</style>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
-----
<p>GitHub</p>
<p><a href="https://github.com/shimat/https://github.com/shimat/sapporo_population">https://github.com/shimat/https://github.com/shimat/sapporo_population</a></p>
<p>出典</p>
<div class="xx-small-font">
<dl>
<dt>人口データ</dt>
<dd>DATA-SMART CITY SAPPORO 町名・条丁目別世帯数及び男女別人口 令和3年（2021年）4月1日現在
(<a href="https://ckan.pf-sapporo.jp/dataset/juuki_8/resource/17075eca-d5f3-4f2c-9fd7-89c155a63fa0">https://ckan.pf-sapporo.jp/dataset/juuki_8/resource/17075eca-d5f3-4f2c-9fd7-89c155a63fa0</a>)</dd>
<dt>地区境界データ</dt>
<dd>『国勢調査町丁・字等別境界データセット』（CODH作成） 「平成27年国勢調査町丁・字等別境界データ」（NICT加工）
(<a href="https://geoshape.ex.nii.ac.jp/ka/">https://geoshape.ex.nii.ac.jp/ka/</a>)</dd>
</dl>
</div>
""", unsafe_allow_html=True)

