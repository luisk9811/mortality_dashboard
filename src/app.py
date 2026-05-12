import dash
from layout import create_layout
from callbacks import register_callbacks

# Initialize Dash application
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Expose the underlying Flask server for PaaS deployment (Render/Gunicorn)
server = app.server

# Mount Layout
app.layout = create_layout()

# Mount Callbacks
register_callbacks(app)

if __name__ == '__main__':
    # Run locally on port 8050
    app.run(debug=True, host='0.0.0.0', port=8050)