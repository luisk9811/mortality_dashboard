from dash import Dash, Input, Output, html, dcc
from layout import FIGURES_CACHE

# Registra los callbacks de navegación
def register_callbacks(app: Dash):
    
    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def render_page_content(pathname):

        # Página principal con mapa de mortalidad
        if pathname == "/" or pathname == "/mapa":
            return html.Div([
                html.H2(
                    "Distribución Geográfica de Muertes",
                    style={'borderBottom': '2px solid #eee', 'paddingBottom': '10px'}
                ),

                dcc.Graph(
                    figure=FIGURES_CACHE["mapa"],
                    style={'height': '75vh'}
                )
            ])

        # Serie temporal por meses
        elif pathname == "/meses":
            return html.Div([
                html.H2(
                    "Tendencia Temporal (Por Mes)",
                    style={'borderBottom': '2px solid #eee', 'paddingBottom': '10px'}
                ),

                dcc.Graph(
                    figure=FIGURES_CACHE["linea"],
                    style={'height': '75vh'}
                )
            ])

        # Ciudades con más homicidios
        elif pathname == "/violencia":
            return html.Div([
                html.H2(
                    "Top 5 Ciudades Más Violentas (Arma de Fuego)",
                    style={'borderBottom': '2px solid #eee', 'paddingBottom': '10px'}
                ),

                dcc.Graph(
                    figure=FIGURES_CACHE["barras"],
                    style={'height': '75vh'}
                )
            ])

        # Ciudades con menor mortalidad
        elif pathname == "/menor-mortalidad":
            return html.Div([
                html.H2(
                    "10 Ciudades con Menor Mortalidad",
                    style={'borderBottom': '2px solid #eee', 'paddingBottom': '10px'}
                ),

                dcc.Graph(
                    figure=FIGURES_CACHE["pie"],
                    style={'height': '75vh'}
                )
            ])

        # Tabla de causas principales de muerte
        elif pathname == "/causas":
            return html.Div([
                html.H2(
                    "Top 10 Principales Causas de Muerte",
                    style={
                        'borderBottom': '2px solid #eee',
                        'paddingBottom': '10px',
                        'marginBottom': '30px'
                    }
                ),

                FIGURES_CACHE["tabla"]
            ])

        # Comparación por sexo y departamento
        elif pathname == "/sexo":
            return html.Div([
                html.H2(
                    "Comparación por Sexo y Departamento",
                    style={'borderBottom': '2px solid #eee', 'paddingBottom': '10px'}
                ),

                dcc.Graph(
                    figure=FIGURES_CACHE["apiladas"],
                    style={'height': '75vh'}
                )
            ])

        # Distribución por grupo de edad
        elif pathname == "/edades":
            return html.Div([
                html.H2(
                    "Distribución de Muertes por Ciclo de Vida",
                    style={'borderBottom': '2px solid #eee', 'paddingBottom': '10px'}
                ),

                dcc.Graph(
                    figure=FIGURES_CACHE["histograma"],
                    style={'height': '75vh'}
                )
            ])

        # Página para rutas inexistentes
        return html.Div([
            html.H1("404: Página no encontrada", style={'color': 'red'}),

            html.P(f"La ruta {pathname} no está definida en la aplicación.")
        ])