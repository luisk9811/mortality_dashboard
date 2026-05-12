import dash
from dash import html, dcc
from components.sidebar import get_sidebar
from callbacks.router import register_router

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

CONTENT_STYLE = {
    "marginLeft": "18rem", "padding": "2rem 2rem", "fontFamily": "Arial"
}

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    get_sidebar(),
    html.Div(id="page-content", style=CONTENT_STYLE)
])

register_router(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)