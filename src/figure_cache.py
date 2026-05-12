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

# Plantilla visual base para todas las gráficas
TEMPLATE = "plotly_white"

# Construye todas las gráficas y tablas
def build_all_figures():

    # Mapa de mortalidad por departamento
    fig_map = px.choropleth(
        get_deaths_by_department(df_main), 
        geojson=geojson_data, 
        locations='DEPARTAMENTO', 
        featureidkey='properties.NOMBRE_DPT', 
        color='TOTAL_DEATHS',
        color_continuous_scale='Reds',
        labels={'TOTAL_DEATHS': 'Total de Muertes', 'DEPARTAMENTO': 'Departamento'}
    )

    fig_map.update_geos(fitbounds="locations", visible=False)

    fig_map.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        template=TEMPLATE
    )
    
    # Serie temporal de muertes por mes
    fig_line = px.line(
        get_deaths_by_month(df_main), 
        x='MES', 
        y='TOTAL_DEATHS',
        markers=True,
        labels={'MES': 'Mes del Año', 'TOTAL_DEATHS': 'Total de Muertes'},
        color_discrete_sequence=['#2c3e50']
    )

    fig_line.update_xaxes(dtick=1)
    fig_line.update_layout(template=TEMPLATE)

    # Ciudades con más homicidios
    fig_bar = px.bar(
        get_top_violent_cities(df_main), 
        x='MUNICIPIO', 
        y='HOMICIDES',
        labels={'MUNICIPIO': 'Municipio', 'HOMICIDES': 'Homicidios'},
        color='HOMICIDES',
        color_continuous_scale='Reds'
    )

    fig_bar.update_layout(template=TEMPLATE, xaxis_tickangle=-45)

    # Ciudades con menor mortalidad
    fig_pie = px.pie(
        get_lowest_mortality_cities(df_main), 
        names='MUNICIPIO', 
        values='TOTAL_DEATHS',
        color_discrete_sequence=px.colors.sequential.Teal
    )

    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(template=TEMPLATE, showlegend=False)

    # Mortalidad por sexo y departamento
    fig_stacked = px.bar(
        get_deaths_by_sex_and_dept(df_main), 
        x='DEPARTAMENTO', 
        y='TOTAL_DEATHS', 
        color='SEX_LABEL', 
        barmode='stack',
        labels={
            'DEPARTAMENTO': 'Departamento',
            'TOTAL_DEATHS': 'Total de Muertes',
            'SEX_LABEL': 'Género'
        },

        # Colores personalizados para cada sexo
        color_discrete_map={
            'Masculino': '#2980b9',
            'Femenino': '#8e44ad',
            'Indeterminado': '#7f8c8d'
        } 
    )

    fig_stacked.update_layout(template=TEMPLATE, xaxis_tickangle=-45)

    # Mortalidad por grupo de edad
    fig_hist = px.bar(
        get_deaths_by_age_group(df_main), 
        x='AGE_CATEGORY', 
        y='TOTAL_DEATHS',
        labels={
            'AGE_CATEGORY': 'Categoría de Edad',
            'TOTAL_DEATHS': 'Total de Muertes'
        },

        color='AGE_CATEGORY',
        color_discrete_sequence=px.colors.qualitative.Prism
    )

    fig_hist.update_layout(
        template=TEMPLATE,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    # Tabla de principales causas de muerte
    top_causes_df = get_top_causes(df_main)

    # Renombra columnas para mostrar en la interfaz
    top_causes_df = top_causes_df.rename(columns={
        'DEATH_CODE': 'Código de Muerte', 
        'DEATH_DESCRIPTION': 'Descripción de la Causa de Muerte', 
        'TOTAL_CASES': 'Casos Registrados'
    })
    
    table_causes = dash_table.DataTable(
        data=top_causes_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in top_causes_df.columns],
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={
            'backgroundColor': '#1d2b36',
            'color': 'white',
            'fontWeight': 'bold'
        },

        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'fontFamily': 'Arial',
            'border': '1px solid #eee'
        },

        # Alterna colores entre filas
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'}
        ]
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

# Cache reutilizable de gráficas
FIGURES_CACHE = build_all_figures()