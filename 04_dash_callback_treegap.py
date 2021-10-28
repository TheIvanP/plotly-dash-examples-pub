import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dash_bootstrap_templates import load_figure_template

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])
load_figure_template("superhero")

navbar = dbc.NavbarSimple(
    brand="navigation",
    brand_href="#",
    color="primary",
    dark=True,
)

df = px.data.gapminder()

# filter outlier
df = df.loc[df["country"] != "Kuwait"]

df.columns
#%%
range_limits = df["gdpPercap"]

values = df["year"].unique().tolist()
gap_options = [{"label": x, "value": x} for x in values]


def threshold_dataframe(
    df: pd.DataFrame, column_name: str, low: float, high: float
) -> pd.DataFrame:
    """return DataFrame where column_name is between low and high"""
    return df.loc[(df[column_name] >= low) & (df[column_name] <= high)]


#%%


def layout_content_card(title, content: list):
    content_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H3(title, className="card-title"),
                    *content,
                ]
            ),
        ],
        outline=True,
        # className="mb-4",
        #        style={"width": "18rem"},
    )

    return content_card


main_graph = layout_content_card(
    content=[
        dcc.Graph(id="graph-gap"),
    ],
    title="Population sizes, GDP highlight",
)


side_menu = layout_content_card(
    content=[
        dcc.Dropdown(
            id="gap-year",
            options=gap_options,
            value=list(gap_options[0].values())[0],
        ),
    ],
    title="year",
)

bottom_area = layout_content_card(
    content=[
        dcc.RangeSlider(
            id="gap-threshold",
            min=range_limits.min(),
            max=range_limits.max(),
            step=0.5,
            value=[
                range_limits.min(),
                range_limits.max(),
            ],
            included=True,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
    ],
    title=range_limits.name,
)


@app.callback(
    Output("graph-gap", "figure"),
    Input("gap-threshold", "value"),
    Input("gap-year", "value"),
)
def update_figure(gap_thres: float, selected_year):

    filtered_df = df[df.year == selected_year]

    df_thres = threshold_dataframe(filtered_df, "gdpPercap", gap_thres[0], gap_thres[1])

    fig = px.treemap(
        df_thres,
        path=["continent", "country"],
        values="pop",
        color="gdpPercap",
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig.update_layout()

    return fig


# app_layout = html.Div([])

app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            [
                navbar,
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col([main_graph]),
                                dbc.Col([side_menu], width=2),
                            ],
                            className="g-0",
                        ),
                        dbc.Row(
                            [
                                dbc.Col([bottom_area]),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ),
)

if __name__ == "__main__":
    app.run_server(debug=True)
