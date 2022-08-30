import os
from dash import Dash, dcc, html, Input, Output, register_page, callback
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pickle as pkl


static = 'static/'
load_figure_template('MINTY')


#---------------Functions---------------------------------

def plot_globe():
    cache = os.path.join(static + "fig_globe.pkl")
    with open(cache, 'rb') as handle:
        fig = pkl.load(handle)

    figure = go.Figure(data=fig).update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        height=580,
        width=700
    )

    return figure

# -------------------Build Layout--------------------------
intro = html.Div([
    # dbc.Card(
    #     dbc.CardBody([
            html.H1('Welcome', style={"color":'white', "textAlign":'center'}),
            html.P('Intro text', style={"color":'white',"textAlign":'center'})
    #     ]),  style={"height":"80vh"}
    # )
])

intro_2 = html.Div([
    # dbc.Card(
    #     dbc.CardBody([
            html.H1('Welcome', style={"color":'white',"textAlign":'center'}),
            html.P('Intro text', style={"color":'white', "textAlign":'center'})
    #     ]),  style={"height":"80vh"}
    # )
])

globe = html.Div(
    [
        # dbc.Card(
        #
        #     dbc.CardBody([
                html.Center(
                    dcc.Graph(figure=plot_globe(), style={"Align":"center"
                                                          },
                              config={"displaylogo": False, "displayModeBar": False,
                                      'scrollZoom':False},),
                )
        #         )
        # ]
        #     ), style={"height":"80vh"}
        # )
    ])



###-------------------Build app-----------------------------

register_page(__name__, use_pages=True, path='/', external_stylesheets=[dbc.themes.MINTY])

# define our HTML page
layout = html.Div([
    dbc.Card([
            dbc.CardImg(
                src= static + "pexels-francesco-ungaro-281260.jpg",
                top=True,
                style={"height":"90vh", "width":"100%",} #  "background-color":'black' "opacity": 0.9,
            ),
            dbc.CardImgOverlay(
             dbc.CardBody([
                dbc.Row([
                    dbc.Col(intro, width=3),
                    dbc.Col(globe, width=6),
                    dbc.Col(intro_2, width=3)
                ]),
             ]
             )
            )]
     ),
])