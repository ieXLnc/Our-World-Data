from dash import Dash, dcc, html, Input, Output
import dash
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


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
    app.run_server(debug=True)
