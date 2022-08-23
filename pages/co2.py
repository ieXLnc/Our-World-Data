from dash import Dash, dcc, html, Input, Output, register_page, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import numpy as np


load_figure_template("MINTY")
df = pd.read_csv(
    "C:/Users/xavier/PycharmProjects/Dashboard/climate/annual-co2-emissions-per-country.csv"
)


# df functions
def prepare_map(df, year):
    df_yr = df.loc[df["Year"] == year].copy()
    df_yr = df_yr.fillna("No data")
    return df_yr


def prepare_scatter(df, year):
    list_pays = [
        "United States",
        "United Kingdom",
        "European Union (28)",
        "India",
        "China",
        "South Africa",
        "Russia",
        "Brazil",
    ]
    df_p = df[df["Entity"].isin(list_pays)]
    df_p_yr = df_p.loc[df["Year"] <= year]
    df_p_yr = df_p_yr.fillna("No data")

    return df_p_yr


# -------------------Build Layout--------------------------
# text and slider expl
text_slider = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.H4("Annual CO2 emissions by country"),
                        ],
                        style={"textAlign": "center", "height": "45vh"},
                    ),
                    html.Div(
                        [
                            dcc.Slider(
                                id="my-slider-1",
                                value=1800,
                                min=1800,
                                max=2020,
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True},
                            )
                        ]
                    ),
                ]
            )
        )
    ]
)

scatter_graph = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="my-graph-1",
                        style={"height": "50vh"},
                        config={"displaylogo": False, "displayModeBar": False},
                    )
                ]
            )
        )
    ]
)

map_graph = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="my-graph-2",
                        style={"width": "100%", "height": "100%", "Align": "center"},
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
                    )
                ]
            )
        )
    ]
)


# -------------------Build app-----------------------------

# app = Dash(__name__)
register_page(__name__, path="/co2", external_stylesheets=[dbc.themes.MINTY])


layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    # html.Br(),
                    # next row with widgets and graphs
                    dbc.Row(
                        [
                            dbc.Col(
                                text_slider, width=3
                            ),  # text with explanations and slider
                            dbc.Col(scatter_graph, width=9),  # map
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(map_graph, width=12),
                        ],
                        align="center",
                    ),
                ]
            )
        )
    ]
)


# ----------------Build callbacks--------------------
@callback(Output("my-graph-2", "figure"), [Input("my-slider-1", "value")])
def update_map(value):
    dff = prepare_map(df, value)
    dff["Annual CO2 emissions"] = np.log10(dff["Annual CO2 emissions"])
    fig = px.choropleth(
        dff,
        locations="Code",
        color="Annual CO2 emissions",
        hover_name="Entity",
        hover_data=["Annual CO2 emissions"],
        color_continuous_scale=px.colors.sequential.YlGnBu,
        range_color=(np.log10(1e7), np.log10(20e9)),
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        geo=dict(
            showframe=False,
            showcountries=True,
            showlakes=True,
            landcolor="LightGrey",
            # projection_type='equirectangular'
            projection_type="natural earth",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        autosize=True,  # width=1300, height=500,
        clickmode="select",
    )
    fig.update_coloraxes(
        colorbar=dict(
            y=-0.15,
            orientation="h",
            len=0.7,
            thickness=15,
            title="CO2",
            tickvals=[
                np.log10(10e7),
                np.log10(20e7),
                np.log10(50e7),
                np.log10(100e7),
                np.log10(200e7),
                np.log10(500e7),
                np.log10(1e9),
                np.log10(5e9),
                np.log10(10e9),
                np.log10(20e9),
            ],
            ticktext=[
                "10M",
                "20M",
                "50M",
                "100M",
                "200M",
                "500M",
                "1B",
                "5B",
                "10B",
                "20B",
            ],
        )
    )

    return fig


@callback(Output("my-graph-1", "figure"), [Input("my-slider-1", "value")])
def update_graph(value):
    dff_2 = prepare_scatter(df, value)
    fig = px.line(
        dff_2,
        x="Year",
        y="Annual CO2 emissions",
        color="Entity",
    ).update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig
