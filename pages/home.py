from dash import Dash, dcc, html, Input, Output, register_page, callback
import dash
import json
from plotly.offline import plot
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from PIL import Image
import numpy as np


load_figure_template('SOLAR')


#---------------Functions---------------------------------
def plot_globe():
    fig = go.Figure(go.Choropleth())


    fig.update_geos(projection_type="orthographic",
                    #visible=False,
                    #showcountries=True, countrycolor='lightgrey',
                    showland=True, landcolor='#4FD190',
                    showlakes=True, lakecolor='#4F7BD1',
                    showocean=True, oceancolor="#2554C7")


    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                paper_bgcolor = "rgba(0,0,0,0)",
                                plot_bgcolor = "rgba(0,0,0,0)",
                                geo_bgcolor = "rgba(0,0,0,0)",)

    return fig

# def plot_globe():
#     cache = "C:/Users/xavier/PycharmProjects/Dashboard/climate/fig_globe.json"
#     with open(cache, 'r') as f:
#         fig = json.load(f)


    # fig.update_layout(
    #     autosize=True,
    #     margin=dict(
    #         l=0,
    #         r=0,
    #         b=0,
    #         t=0,
    #         pad=0),
    #     paper_bgcolor="LightSteelBlue",
    #
    # )
    # figure = go.Figure(data=fig).update_layout(
    #     paper_bgcolor='#002B36'
    # )
    #
    # return figure

# fig = plot_globe()


# -------------------Build Layout--------------------------

# text and slider expl
text = html.Div(
    [
        html.Div(
            [
                html.P("Home page, welcomeeee"),
            ],
            style={"textAlign": "center"},
        ),
    ]
)

globe = html.Div(
    [
        dbc.Card(

            html.Div([

            # dbc.CardImg(src="C:/Users/xavier/PycharmProjects/Dashboard/climate/space.jpg"),

            dbc.CardBody([

               #html.Center(
                          dcc.Graph(figure=plot_globe(), style={"height":"75vh"})
                #)
            ])
        ], style={'background':'black'})
        )
    ])



###-------------------Build app-----------------------------

register_page(__name__, use_pages=True, path='/', external_stylesheets=[dbc.themes.SOLAR])

# define our HTML page
layout = html.Div([
    dbc.Card(
         dbc.CardBody([
            dbc.Row([
                # dbc.Col(text, width=3),
                dbc.Col(globe, width=12)
            ]),
         ]
         )
     ),
])

#----------------app callbacks-----------------
# @callback(Output('globe-graph', 'figure'))
# def plot_globe():
#     fig = go.Figure(go.Scattergeo())
#     fig.update_geos(projection_type="orthographic")
#     fig.update_layout(height=300, margin={"r": 0, "t": 0, "l": 0, "b": 0})
#     return fig