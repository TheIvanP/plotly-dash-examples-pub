import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# https://plotly.com/python/plotly-express/#highlevel-features

# dash html components wraps common html:
# https://dash.plotly.com/dash-html-components

# dash core componenets, widgets and controls
# https://dash.plotly.com/dash-core-components

# data specific to our application
df = px.data.iris()
all_dims = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

# WSGI application object
app = dash.Dash(__name__)

# How the application looks and it's hierachy on screen
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in all_dims],
            value=all_dims[:2],
            multi=True,
        ),
        dcc.Graph(id="splom"),
    ]
)

# callback function is triggered whenever and input component with id="dropdown" is changed
# "value" will be passed to the function via it's augments 'dims'
# a figure will be output and passed to the component in the layout with id="splom"
@app.callback(Output("splom", "figure"), [Input("dropdown", "value")])
def update_bar_chart(dims):
    fig = px.scatter_matrix(df, dimensions=dims, color="species")
    return fig


# Boilerplate for running this file with Flask development server
# for production, use e.g. gunicorn https://docs.gunicorn.org/en/stable/run.html
# example: gunicorn --workers=2 dash_minimal:app
app.run_server(debug=True)
