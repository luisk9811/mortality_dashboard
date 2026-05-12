from dash import html, dcc

# Estilos del menú lateral
SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0,
    "width": "18rem", "padding": "2rem 1rem",
    "backgroundColor": "#1d2b36", "color": "white", "fontFamily": "Arial"
}

# Estilos de los enlaces del menú
LINK_STYLE = {
    "color": "#a5b1c2", "textDecoration": "none", "display": "block",
    "padding": "12px 10px", "fontSize": "16px", "borderBottom": "1px solid #2d3e4f"
}

# Genera el menú lateral de navegación
def get_sidebar():
    return html.Div([
        html.H2("Mortalidad 2019", style={'textAlign': 'center', 'marginBottom': '20px'}),

        html.Hr(style={'borderColor': '#455a64'}),

        # Enlaces de navegación
        html.Div([
            dcc.Link("Mapa de Mortalidad", href="/", style=LINK_STYLE),
            dcc.Link("Serie de Tiempo", href="/meses", style=LINK_STYLE),
            dcc.Link("Ciudades Violentas", href="/violencia", style=LINK_STYLE),
            dcc.Link("Menor Mortalidad", href="/menor-mortalidad", style=LINK_STYLE),
            dcc.Link("Top Causas", href="/causas", style=LINK_STYLE),
            dcc.Link("Sexo y Departamento", href="/sexo", style=LINK_STYLE),
            dcc.Link("Categoría de Edad", href="/edades", style=LINK_STYLE),
        ])
    ], style=SIDEBAR_STYLE)