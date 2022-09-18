import os
from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
    register_page,
    callback,
    clientside_callback,
)

import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import numpy as np
from constant import STATIC, C_1, C_2, C_3, C_4
import sqlite3

# connect to database
con = sqlite3.connect("static/World_data.db")
cur = con.cursor()

load_figure_template("MINTY")


df = pd.read_sql_query(
    "SELECT Code, Entity, Year, Annual_CO2_emissions, rounded_emissions, map_emissions "
    "from World_data WHERE Year >= 1800",
    con,
)


# df functions
def prepare_map(df, year):
    df_yr = df.loc[df["Year"] == year].copy()
    df_yr = df_yr.drop(df_yr.loc[df_yr["Entity"] == "Antarctica"].index)
    # ARE --> UAE --> still not showing the country
    df_yr["map_emissions"] = df_yr["map_emissions"].fillna("Missing Data")
    df_yr["rounded_emissions"] = df_yr["rounded_emissions"].fillna(0)
    return df_yr


def prepare_scatter(df, year, selectedData):
    # record the last one to remove selection if double click
    if selectedData is None:
        mask = [
            "United States",
            "United Kingdom",
            "European Union (28)",
            "India",
            "China",
            "South Africa",
            "Russia",
            "Brazil",
        ]
        df_p = df[df["Entity"].isin(mask)]
    else:
        mask = selectedData["points"][0]["hovertext"]
        df_p = df[df["Entity"] == mask]

    df_p_yr = df_p.loc[df["Year"] <= year]
    df_p_yr = df_p_yr.fillna(0)

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
                            html.P(
                                """Carbon dioxide (CO₂) emissions from fossil fuels and industry. Land use change is not included."""
                            ),
                            html.P(
                                "Click on a country to see its CO2 emissions over time."
                            ),
                        ],
                        style={"height": "45vh"},  # "textAlign": "center",
                    ),
                    html.Div([]),
                ]
            ),
            color=C_4,
            style={"border": "rgba(0,0,0,0)"},
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
            ),
            color=C_4,
            style={"border-color": "rgba(0,0,0,0"},
        )
    ]
)

map_graph = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Slider(
                        id="my-slider-1",
                        value=df["Year"].max(),
                        min=df["Year"].min(),
                        max=df["Year"].max(),
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                        step=1,
                    ),
                    dcc.Graph(
                        id="my-graph-2",
                        style={"width": "100%", "height": "100%", "Align": "center"},
                        # config={
                        #     "displaylogo": False,
                        #     "displayModeBar": False,
                        # },
                    ),
                ]
            ),
            color="white",
            style={"border-color": "rgba(0,0,0, 0)"},
        )
    ]
)


# -------------------Build app-----------------------------

# app = Dash(__name__)
register_page(__name__, path="/co2", external_stylesheets=[dbc.themes.LUX])


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
                # color for background card
            ),
            color=C_4,
        )
    ]
)


# ----------------Build callbacks--------------------
@callback(Output("my-graph-2", "figure"), [Input("my-slider-1", "value")])
def update_map(value):
    dff = prepare_map(df, value)
    palette_p = px.colors.sequential.YlGnBu
    palette_n = px.colors.sequential.Reds
    # colorArray = px.colors.sequential.YlGnBu
    # colorArray.insert(0, 'rgb(211, 211, 211)')
    fig = px.choropleth(
        dff,
        locations="Code",
        color="map_emissions",
        hover_name="Entity",
        custom_data=["Entity", "rounded_emissions", "Year"],
        category_orders={
            "map_emissions": [
                "Missing Data",
                "0 - 20M",
                "20M - 50M",
                "50M - 100M",
                "100M - 200M",
                "200M - 500M",
                "500M - 1B",
                "1B - 2B",
                "2B - 5B",
                "5B - 10B",
                "> 10B",
            ]
        },
        color_discrete_map={
            "Missing Data": "LightGrey",
            "0 - 20M": palette_p[1],
            "20M - 50M": palette_p[2],
            "50M - 100M": palette_n[2],
            "100M - 200M": palette_n[3],
            "200M - 500M": palette_n[4],
            "500M - 1B": palette_n[5],
            "1B - 2B": palette_n[6],
            "2B - 5B": palette_n[7],
            "5B - 10B": palette_n[8],
            "> 10B": palette_n[8],
        },
    )

    fig.update_traces(
        hovertemplate="CO2 for %{customdata[0]} in %{customdata[2]}: %{customdata[1]:.2f} millions",
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        geo=dict(
            showframe=False,
            showcountries=True,
            showlakes=True,
            landcolor="White",
            projection_type="equirectangular",
            lataxis_range=(-60, 80),
        ),
        width=1500,
        height=600,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        clickmode="event+select",
        legend=dict(
            # try to create the bar
            y=-0.15,
            x=0.1,
            orientation="h",
            valign="top",
            itemclick="toggleothers",
            title="Annual CO2 Emissions",
        ),
    )

    return fig


@callback(
    Output("my-graph-1", "figure"),
    [Input("my-slider-1", "value"), Input("my-graph-2", "selectedData")],
)
def update_graph(value, selectedData):
    dff_2 = prepare_scatter(df, value, selectedData)
    fig = px.line(
        dff_2,
        x="Year",
        y="Annual_CO2_emissions",
        color="Entity",
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
    ).update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(
        showgrid=True,
        # color='LightGrey',
        gridcolor="LightGrey",
    )
    fig.update_yaxes(
        showgrid=True,
        # color='LightGrey',
        gridcolor="LightGrey",
    )
    return fig
