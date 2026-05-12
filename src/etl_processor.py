import pandas as pd
import numpy as np

def map_age_category(age_code):
    if pd.isna(age_code): 
        return 'Edad desconocida'
    try:
        code = int(age_code)
        if 0 <= code <= 4: return 'Mortalidad neonatal'
        if 5 <= code <= 6: return 'Mortalidad infantil'
        if 7 <= code <= 8: return 'Primera infancia'
        if 9 <= code <= 10: return 'Niñez'
        if code == 11: return 'Adolescencia'
        if 12 <= code <= 13: return 'Juventud'
        if 14 <= code <= 16: return 'Adultez temprana'
        if 17 <= code <= 19: return 'Adultez intermedia'
        if 20 <= code <= 24: return 'Vejez'
        if 25 <= code <= 28: return 'Longevidad / Centenarios'
    except ValueError:
        pass
    return 'Edad desconocida'

def run_etl_pipeline():
    print("1. Loading raw Excel files (This will consume time and RAM)...")
    
    # Load DataFrames
    deaths_df = pd.read_excel("resources/Anexo1.NoFetal2019_CE_15-03-23.xlsx")
    causes_df = pd.read_excel("resources/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx", skiprows=8)
    divipola_df = pd.read_excel("resources/Divipola_CE_.xlsx")

    print("2. Cleaning Dimensions...")
    # Clean Causes Dimension
    causes_df = causes_df.rename(columns={
        "Capítulo": "CHAPTER",
        "Nombre capítulo": "CHAPTER_NAME",
        "Código de la CIE-10 tres caracteres": "DEATH_CODE",
        "Descripción  de códigos mortalidad a tres caracteres": "DEATH_DESCRIPTION"
    })
    
    # Keep only what we need to merge
    causes_df = causes_df.drop_duplicates(subset="DEATH_CODE")[["DEATH_CODE", "DEATH_DESCRIPTION"]]

    print("3. Transforming Mortality Facts...")
    # Standardize the merge key (first 3 characters of CIE-10)
    deaths_df["DEATH_CODE"] = deaths_df["COD_MUERTE"].astype(str).str[0:3]

    # Map Age Groups
    deaths_df['AGE_CATEGORY'] = deaths_df['GRUPO_EDAD1'].apply(map_age_category)

    # Standardize Sex (Validating if it comes as number 1/2 or String M/F)
    # Adjust this mapping if the DANE dictionary differs
    sex_mapping = {1: 'Masculino', 2: 'Femenino', 3: 'Indeterminado'}
    if pd.api.types.is_numeric_dtype(deaths_df['SEXO']):
        deaths_df['SEX_LABEL'] = deaths_df['SEXO'].map(sex_mapping).fillna('Indeterminado')
    else:
        deaths_df['SEX_LABEL'] = deaths_df['SEXO']

    # Flag Homicides explicitly (X95x)
    deaths_df['IS_HOMICIDE_X95'] = deaths_df['COD_MUERTE'].astype(str).str.startswith('X95')

    print("4. Merging Datasets (Applying LEFT JOIN to preserve all records)...")
    
    # Merge Divipola
    merged_df = pd.merge(
        left=deaths_df,
        right=divipola_df,
        on=["COD_DANE", "COD_DEPARTAMENTO", "COD_MUNICIPIO"],
        how="left" 
    )

    # Merge Causes
    merged_df = pd.merge(
        left=merged_df,
        right=causes_df,
        on="DEATH_CODE",
        how="left"
    )

    # Fill unknown descriptions
    merged_df['DEATH_DESCRIPTION'] = merged_df['DEATH_DESCRIPTION'].fillna('Causa no especificada en diccionario')

    print("5. Optimizing and Exporting Data...")
    
    # Select strictly the columns needed for the Dash application
    # Note: Validate that the 'NOM_DEPARTAMENTO' and 'NOM_MUNICIPIO' match your Divipola column names
    columns_to_keep = [
        'COD_DEPARTAMENTO', 'DEPARTAMENTO', 
        'COD_MUNICIPIO', 'MUNICIPIO',
        'MES', 'DEATH_CODE', 'DEATH_DESCRIPTION', 
        'AGE_CATEGORY', 'SEX_LABEL', 'IS_HOMICIDE_X95'
    ]
    
    # Filter existing columns to avoid KeyError if Divipola text headers differ
    final_columns = [col for col in columns_to_keep if col in merged_df.columns]
    final_df = merged_df[final_columns]

    # Export to highly compressed Parquet
    final_df.to_parquet("data/clean_mortality.parquet", engine="pyarrow")
    
    print(f"ETL Complete. Total records verified: {len(final_df)}")
    print("File saved as 'clean_mortality.parquet'. Use this in your Dash app.")

if __name__ == '__main__':
    run_etl_pipeline()