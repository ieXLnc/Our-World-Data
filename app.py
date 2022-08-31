import os
from dash import Dash, dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import gunicorn

static = "static/"
load_figure_template("MINTY")

# -------------------Build Layout--------------------------
# navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",  # Label given to the dropdown menu
            children=[
                dbc.DropdownMenuItem("Home", href="/"),
                dbc.DropdownMenuItem("C02 emissions", href="/co2"),
                dbc.DropdownMenuItem("Gender Equality", href="/gender"),
                dbc.DropdownMenuItem("Democracy", href="/democracy"),
                dbc.DropdownMenuItem("Your country", href="/your-country"),
            ],
        ),
    ],
    brand="Our World Data",  # Set the text on the left side of the Navbar
    sticky="top",
    color="primary",
    dark=True,
)


###-------------------Build app-----------------------------

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.MINTY])
server = app.server

# define our HTML page
app.layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(navbar, width=12),
                        ],
                        align="center",
                    ),
                ]
            )
        ),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
