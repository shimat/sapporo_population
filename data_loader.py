import geopandas as gpd
import numpy as np
import pandas as pd
import streamlit as st
import requests
import io
from typing import Optional
from converter import Converter


class DataLoader:
    @staticmethod
    @st.cache
    def load_coordinates_from_csv(file_name: str):
        csv = pd.read_csv(
            file_name,
            # encoding="SHIFT-JIS",
            header=0,
            usecols=['都道府県名',
                     '市区町村名',
                     '大字町丁目名',
                     '緯度',
                     '経度'])
        return csv

    @staticmethod
    @st.cache
    def load_population_from_csv(file_name: str):
        df = pd.read_csv(
            file_name,
            header=1,)
        df['町条丁目_漢数字'] = df['町条丁目'].apply(lambda x: Converter.replace_area_number_to_kansuji(x))
        df['区別'] = df['区別'].apply(lambda x: x.replace('　', ''))
        return df

    @staticmethod
    @st.cache(allow_output_mutation=True)
    def load_geopandas_from_url(url: str):
        response = requests.get(url).content
        string_io = io.StringIO(response.decode('utf-8'))
        gdf = gpd.read_file(string_io)
        gdf.drop(columns=['KEY_CODE', 'PREF', 'CITY', 'KIGO_I', 'DUMMY1', 'KCODE1'], inplace=True)
        return gdf

    @classmethod
    @st.cache(allow_output_mutation=True)
    def load_geopandas_from_urls(cls, url_list: list[str]):
        tables = [cls.load_geopandas_from_url(url) for url in url_list]
        result = pd.concat(tables)
        return result

    @staticmethod
    @st.cache
    def load_population_by_age_from_url(url: str, limit: Optional[int] = None):
        response = requests.get(url)
        if limit:
            url += f'&limit={limit}'
        df = pd.json_normalize(response.json(), record_path=["result", "records"])
        df.rename(columns=lambda s: s.replace(' ', '').replace('歳', ''), inplace=True)

        column_names = ('年少人口', '0～4', '5～9', '10～14',
                        '生産年齢人口', '15～19', '20～24', '25～29',
                        '30～34', '35～39', '40～44', '45～49', '50～54', '55～59',
                        '60～64', '老年人口', '65～69', '70～74', '75～79', '80～84',
                        '85～89', '90～94', '95～99', '100以上')
        for col in column_names:
            df[col] = df[col].apply(lambda x: x.replace('-', '0'))
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['区分_漢数字'] = df['区分'].apply(lambda x: Converter.replace_area_number_to_kansuji(x))
        return df

    @staticmethod
    @st.cache
    def load_population_by_age_from_csv(file_name: str):
        df = pd.read_csv(file_name)
        df.rename(columns=lambda s: s.replace(' ', '').replace('歳', ''), inplace=True)

        column_names = ('年少人口', '0～4', '5～9', '10～14',
                        '生産年齢人口', '15～19', '20～24', '25～29',
                        '30～34', '35～39', '40～44', '45～49', '50～54', '55～59',
                        '60～64', '老年人口', '65～69', '70～74', '75～79', '80～84',
                        '85～89', '90～94', '95～99', '100以上')
        for col in column_names:
            df[col] = df[col].apply(lambda x: x.replace('-', '0'))
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df['区分_漢数字'] = df['区分'].apply(lambda x: Converter.replace_area_number_to_kansuji(x))
        return df
