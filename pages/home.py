import os
from dash import Dash, dcc, html, Input, Output, register_page, callback
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pickle as pkl
from constant import STATIC, C_1, C_2, C_3, C_4

load_figure_template("MINTY")


# ---------------Functions---------------------------------


def plot_globe():
    cache = os.path.join(STATIC + "fig_globe.pkl")
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
title = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Br(),
                        html.H1(
                            "Our World Visualizations",
                            style={"font-size": "250%", "textAlign": "center"},
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
            Welcome to Our World Visualizations!
            
            This website was made as a portfolio project to learn dash and plotly and demonstrate my skills in both.
            To create a relevant visualization website, I drew a lot of inspiration from the [Our World In Data](https://ourworldindata.org/) 
            website, where most of the datasets I used in this project came from.
            
            The goal of this project was to create my own visualizations, learn how to code them in backend and frontend and deploy them. I don't think I could have chosen a better example, their visualizations are relevant, well thought out and highly explanatory.

            The site is composed of several pages where you will find information on a specific topic in each of them. 

            As this is a first version, I will try to add more interesting pages and visualizations as I go along.
            """,
                            style={"textAlign": "center", "font-size": "120%"},
                        ),
                    ]
                ),
            ],
            style={
                "display": "flex",
                "textAlign": "center",
                "align-items": "center",
                "justify-content": "center",
                # 'background-color':'black',
                "position": "flex",
                "height": "80vh",
            },
        ),  #
        dcc.Markdown(
            """[Xavier Lince](https://xavierlince.com)""",
            style={
                "position": "absolute",
                "bottom": "0",
                "right": "0",
            },
        ),
    ]
)

# globe = html.Div(
#     [
#         # dbc.Card(
#         #
#         #     dbc.CardBody([
#         html.Center(
#             dcc.Graph(
#                 figure=plot_globe(),
#                 style={"Align": "center"},
#                 config={
#                     "displaylogo": False,
#                     "displayModeBar": False,
#                     "scrollZoom": False,
#                 },
#             ),
#         )
#     ]
# )


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
                    src=STATIC + "map4_2.jpg",
                    top=True,
                    style={
                        "height": "90vh",
                        "width": "100%",
                        "textAlign": "center",
                        "opacity": 0.16,
                    },
                ),
                dbc.CardImgOverlay(
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(title, width=10, style={"height": "100%"}),
                                ],
                                justify="center",
                                align="center",
                            ),
                        ]
                    )
                ),
            ],
        ),
    ]
)
