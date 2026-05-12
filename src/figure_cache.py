import plotly.express as px
from dash import dash_table
from data_processing import (
    load_mortality_data, load_colombia_geojson,
    get_deaths_by_department, get_deaths_by_month,
    get_top_violent_cities, get_lowest_mortality_cities,
    get_top_causes, get_deaths_by_sex_and_dept, get_deaths_by_age_group
)

# Carga de datos principales
df_main = load_mortality_data()
geojson_data = load_colombia_geojson()

# Construye todas las gráficas y tablas
def build_all_figures():

    # Mapa de mortalidad por departamento
    fig_map = px.choropleth(
        get_deaths_by_department(df_main),
        geojson=geojson_data,
        locations='DEPARTAMENTO',
        featureidkey='properties.NOMBRE_DPT',
        color='TOTAL_DEATHS'
    )

    fig_map.update_geos(fitbounds="locations", visible=False)
    
    # Muertes por mes
    fig_line = px.line(get_deaths_by_month(df_main), x='MES', y='TOTAL_DEATHS')

    # Ciudades con más homicidios
    fig_bar = px.bar(get_top_violent_cities(df_main), x='MUNICIPIO', y='HOMICIDES')

    # Ciudades con menor mortalidad
    fig_pie = px.pie(get_lowest_mortality_cities(df_main), names='MUNICIPIO', values='TOTAL_DEATHS')

    # Mortalidad por sexo y departamento
    fig_stacked = px.bar(
        get_deaths_by_sex_and_dept(df_main),
        x='DEPARTAMENTO',
        y='TOTAL_DEATHS',
        color='SEX_LABEL',
        barmode='stack'
    )

    # Mortalidad por grupo de edad
    fig_hist = px.bar(get_deaths_by_age_group(df_main), x='AGE_CATEGORY', y='TOTAL_DEATHS')
    
    # Tabla de causas principales de muerte
    top_causes_df = get_top_causes(df_main)

    table_causes = dash_table.DataTable(
        data=top_causes_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in top_causes_df.columns],
        style_table={'overflowX': 'auto', 'width': '90%', 'margin': 'auto'},
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Arial'}
    )

    return {
        "mapa": fig_map,
        "linea": fig_line,
        "barras": fig_bar,
        "pie": fig_pie,
        "tabla": table_causes,
        "apiladas": fig_stacked,
        "histograma": fig_hist
    }

# Cache de gráficas reutilizable
FIGURES_CACHE = build_all_figures()