from dash import Dash, Input, Output
from pages.views import create_page_layout, get_404_layout

# Registra las rutas de navegación
def register_router(app: Dash):

    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )

    def render_page(pathname):

        # Define las rutas disponibles
        routes = {
            "/": ("Distribución Geográfica de Muertes", "mapa", False),
            "/mapa": ("Distribución Geográfica de Muertes", "mapa", False),
            "/meses": ("Tendencia Temporal (Por Mes)", "linea", False),
            "/violencia": ("Top 5 Ciudades Más Violentas", "barras", False),
            "/menor-mortalidad": ("10 Ciudades con Menor Mortalidad", "pie", False),
            "/causas": ("Top 10 Principales Causas de Muerte", "tabla", True),
            "/sexo": ("Comparación por Sexo y Departamento", "apiladas", False),
            "/edades": ("Distribución de Muertes por Ciclo de Vida", "histograma", False)
        }

        # Renderiza la vista correspondiente
        if pathname in routes:
            title, fig_key, is_table = routes[pathname]
            return create_page_layout(title, fig_key, is_table)

        # Retorna página 404 si la ruta no existe
        return get_404_layout(pathname)