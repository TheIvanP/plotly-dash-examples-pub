import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

# bootstrap themes and component for Dash
# https://dash-bootstrap-components.opensource.faculty.ai/

# grid system and columns explained:
# https://getbootstrap.com/docs/5.1/layout/grid/


app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])

navbar = dbc.NavbarSimple(
    brand="navigation",
    brand_href="#",
    color="primary",
    dark=True,
)


def layout_content_card(title, content: list):
    content_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(title, className="card-title"),
                    *content,
                ]
            ),
        ],
        outline=True,
        className="mb-4",
        #        style={"width": "18rem"},
    )

    return content_card


main_graph = layout_content_card(
    content=[html.H1("here we place our main content")],
    title="main",
)

side_menu = layout_content_card(
    content=[html.H1("Hello side")],
    title="side",
)

bottom_area = layout_content_card(
    content=[html.H1("Hello bottom")],
    title="bottom",
)

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
    app.run_server()
