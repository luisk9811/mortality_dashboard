from dash import html, dcc
from figure_cache import FIGURES_CACHE

# Genera el layout reutilizable para cada página
def create_page_layout(title: str, figure_key: str, is_table: bool = False):

    # Valida si el contenido es tabla o gráfica
    content = (
        FIGURES_CACHE[figure_key]
        if is_table
        else dcc.Graph(
            figure=FIGURES_CACHE[figure_key],
            style={'height': '75vh'}
        )
    )
    
    return html.Div([
        html.H2(
            title,
            style={
                'borderBottom': '2px solid #eee',
                'paddingBottom': '10px',
                'marginBottom': '30px' if is_table else '10px'
            }
        ),

        content
    ])

# Genera la página de error 404
def get_404_layout(pathname: str):
    return html.Div([
        html.H1(
            "404: Página no encontrada",
            style={'color': 'red'}
        ),

        html.P(f"La ruta {pathname} no está definida.")
    ])