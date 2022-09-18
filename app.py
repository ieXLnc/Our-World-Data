import os
from dash import Dash, dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import gunicorn
from constant import C_1, C_2, C_3, C_4

load_figure_template("LUX")


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
    color=C_1,
    dark=True,
)


###-------------------Build app-----------------------------

app = Dash(__name__,
           use_pages=True, external_stylesheets=[dbc.themes.LUX],
           meta_tags=[
               {"name": "viewport", "content": "width=device-width, initial-scale=1"}
           ],
           )
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
            ),
            color=C_1,
        ),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run_server(host="0.0.0.0", port=8050, debug=True)
