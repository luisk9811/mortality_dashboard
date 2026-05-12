import pandas as pd
import json
from pathlib import Path

# BASE_DIR is mortality_dashboard/src
BASE_DIR = Path(__file__).resolve().parent
# PROJECT_ROOT is mortality_dashboard/
PROJECT_ROOT = BASE_DIR.parent

# 1. Load Data Functions
def load_mortality_data() -> pd.DataFrame:
    # Resolves to: mortality_dashboard/data/clean_mortality.parquet
    data_path = PROJECT_ROOT / "data" / "clean_mortality.parquet"
    
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontró el dataset en: {data_path}")
        
    return pd.read_parquet(data_path)

def load_colombia_geojson() -> dict:
    # If your assets folder is inside src/, change PROJECT_ROOT to BASE_DIR in the line below
    geo_path = PROJECT_ROOT / "assets" / "colombia.geojson"
    
    if not geo_path.exists():
        raise FileNotFoundError(f"No se encontró el mapa en: {geo_path}")
        
    with open(geo_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 2. Aggregation Functions for Layout
def get_deaths_by_department(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('DEPARTAMENTO').size().reset_index(name='TOTAL_DEATHS')

def get_deaths_by_month(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('MES').size().reset_index(name='TOTAL_DEATHS')

def get_top_violent_cities(df: pd.DataFrame) -> pd.DataFrame:
    violent_df = df[df['IS_HOMICIDE_X95'] == True]
    return violent_df.groupby('MUNICIPIO').size().reset_index(name='HOMICIDES').nlargest(5, 'HOMICIDES')

def get_lowest_mortality_cities(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('MUNICIPIO').size().reset_index(name='TOTAL_DEATHS').nsmallest(10, 'TOTAL_DEATHS')

def get_top_causes(df: pd.DataFrame) -> pd.DataFrame:
    causes_df = df.groupby(['DEATH_CODE', 'DEATH_DESCRIPTION']).size().reset_index(name='TOTAL_CASES')
    return causes_df.nlargest(10, 'TOTAL_CASES')

def get_deaths_by_sex_and_dept(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['DEPARTAMENTO', 'SEX_LABEL']).size().reset_index(name='TOTAL_DEATHS')

def get_deaths_by_age_group(df: pd.DataFrame) -> pd.DataFrame:
    age_order = [
        'Mortalidad neonatal', 'Mortalidad infantil', 'Primera infancia', 'Niñez',
        'Adolescencia', 'Juventud', 'Adultez temprana', 'Adultez intermedia',
        'Vejez', 'Longevidad / Centenarios', 'Edad desconocida'
    ]
    hist_data = df.groupby('AGE_CATEGORY').size().reset_index(name='TOTAL_DEATHS')
    # Set categorical type to enforce specific logical sorting
    hist_data['AGE_CATEGORY'] = pd.Categorical(hist_data['AGE_CATEGORY'], categories=age_order, ordered=True)
    return hist_data.sort_values('AGE_CATEGORY')