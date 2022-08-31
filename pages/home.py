import os
from dash import Dash, dcc, html, Input, Output, register_page, callback
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pickle as pkl


static = "static/"
load_figure_template("MINTY")


# ---------------Functions---------------------------------


def plot_globe():
    cache = os.path.join(static + "fig_globe.pkl")
    with open(cache, "rb") as handle:
        fig = pkl.load(handle)

    figure = go.Figure(data=fig).update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        height=580,
        width=700,
    )

    return figure


# -------------------Build Layout--------------------------
intro = html.Div(
    [
        html.H1("Welcome to our world data!"),
        html.P(
            f"This website was made as a portfolio project to learn dash and plotly and demonstrate my skills in both."
        ),
        html.P(),
        html.P(
            f"To create a relevant visualization website, I drew a lot of inspiration from the ourworldindata.org website, "
            f"where most of the datasets I used in this project came from."
        ),
        html.P(),
        html.P(
            f"The goal of this project was to create my own visualizations, "
            f"learn how to code them in backend and frontend and deploy them. "
            f"I don't think I could have picked a better example than the ourworldindata.org site, "
            f"their visualizations are relevant, well thought out and super explanatory. ",
        ),
        html.P(),
        html.P(f"I hope you enjoy this site as much!"),
    ],
    style={"color": "white"},
)

intro_2 = html.Div(
    [
        html.H1("About the webiste:"),
        html.P(
            f"This website is composed of several pages where you will find information on a specific topic in each of them."
        ),
        html.P(),
        html.P(f"The different topics of interest for the moment are :"),
        html.P(f"- CO2 emissions per country"),
        html.P(f"- Current state of gender equality "),
        html.P(f"- Current state of democracy"),
        html.P(
            "The last page allows you to select a specific country and have all the data for the selected country."
        ),
        html.P(
            "As this is a first version, I will try to add more interesting pages and visualizations as I go along."
        ),
        html.P(),
    ],
    style={"color": "white"},
)

globe = html.Div(
    [
        # dbc.Card(
        #
        #     dbc.CardBody([
        html.Center(
            dcc.Graph(
                figure=plot_globe(),
                style={"Align": "center"},
                config={
                    "displaylogo": False,
                    "displayModeBar": False,
                    "scrollZoom": False,
                },
            ),
        )
    ]
)


###-------------------Build app-----------------------------

register_page(
    __name__, use_pages=True, path="/", external_stylesheets=[dbc.themes.MINTY]
)

# define our HTML page
layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardImg(
                    src=static + "pexels-francesco-ungaro-281260.jpg",
                    top=True,
                    style={
                        "height": "90vh",
                        "width": "100%",
                    },  #  "background-color":'black' "opacity": 0.9,
                ),
                dbc.CardImgOverlay(
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(intro, width=3),
                                    dbc.Col(globe, width=6),
                                    dbc.Col(intro_2, width=3),
                                ]
                            ),
                        ]
                    )
                ),
            ]
        ),
    ]
)
