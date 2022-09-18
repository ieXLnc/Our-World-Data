from dash import Dash, dcc, html, Input, Output, register_page, callback
import os
import dash
import numpy as np
import sqlite3
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from constant import STATIC, DB, C_1, C_2, C_3, C_4

# connect to database
con = sqlite3.connect(os.path.join(STATIC, DB))
cur = con.cursor()

df_vote = pd.read_sql_query(
    "SELECT Code, Entity, Year, female_suffrage_lied "
    "from World_data "
    "WHERE Year >= 1800",
    con,
)

df_right = pd.read_sql_query(
    "SELECT Code, Entity, Year, accessjust_w_row_owid "
    "from World_data "
    "WHERE Year >= 1800",
    con,
)


def prepare_map(df, year):
    df_yr = df.loc[df["Year"] == year]
    df_yr = df_yr.drop(df_yr.loc[df_yr["Entity"] == "Antarctica"].index)
    df_yr = df_yr.fillna("Missing Data")
    return df_yr


def gender_infos(df, selectedData, var):

    mask = selectedData["points"][0]["hovertext"]
    dff_g = df[df["Entity"] == mask]

    max_year = dff_g.Year.max()
    if dff_g.loc[dff_g.Year == max_year, var].values[0] == "No":
        year = -1
        return mask, year
    else:
        year = dff_g.loc[dff_g[var] == "Yes", "Year"].min()
        return mask, year


# -------------------Build layout--------------------------
text = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.H4("Universal right to vote for women"),
                            html.P(
                                """Based on the classification and assessment by Skaaning et al. (2015).""",
                            ),
                            html.Div(id="voting-right"),
                        ],
                        style={"height": "55vh"},  # "textAlign": "center",
                    ),
                ]
            ),
            style={"height": "60vh", "border": "rgba(0,0,0,0)"},
            color=C_3,
        )
    ]
)

graph_vote = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        children=[
                            dcc.Slider(
                                id="my-slider-3",
                                value=df_vote["Year"].max(),
                                min=df_vote["Year"].min(),
                                max=df_vote["Year"].max(),
                                marks=None,
                                updatemode="drag",
                                tooltip={"placement": "bottom", "always_visible": True},
                                step=1,
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="my-graph-3",
                                config={
                                    "displaylogo": False,
                                    "displayModeBar": False,
                                },
                                style={"height": "50vh"},
                            )
                        ]
                    ),
                ],
                style={"height": "60vh"},
            ),
            color="white",
            style={"border-color": "rgba(0,0,0,0)"},
        )
    ]
)

text_2 = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.H4("Access to justice for women"),
                            html.P(
                                """Based on the classification by Lührmann et al. (2018) and the assessment by V-Dem’s experts. It captures that women
safely bring cases before courts, are able to seek redress if public authorities violate their rights, and trials are fair."""
                            ),
                            html.Div(id="access-justice"),
                        ],
                        style={"height": "55vh"},  # "textAlign": "center"
                    ),
                ]
            ),
            style={"height": "60vh", "border": "rgba(0,0,0,0)"},
            color=C_3,
        )
    ]
)

graph_right = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            dcc.Slider(
                                id="my-slider-4",
                                value=df_right["Year"].max(),
                                min=df_right["Year"].min(),
                                max=df_right["Year"].max(),
                                marks=None,
                                updatemode="drag",
                                tooltip={"placement": "bottom", "always_visible": True},
                                step=1,
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            dcc.Graph(
                                id="my-graph-4",
                                config={
                                    "displaylogo": False,
                                    "displayModeBar": False,
                                },
                                style={
                                    # "width": "100%",
                                    "height": "50vh",
                                    # "Align": "center",
                                },
                            )
                        ]
                    ),
                ],
                style={"height": "60vh"},
            ),
            color="white",
            style={"border-color": "rgba(0,0,0,0)"},
        )
    ]
)

# -------------------Build app-----------------------------

# app = Dash(__name__)
register_page(__name__, path="/gender", external_stylesheets=[dbc.themes.MINTY])

layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [dbc.Col(text, width=3), dbc.Col(graph_vote, width=9)],
                        align="center",
                    ),
                    html.Br(),
                    dbc.Row(
                        [dbc.Col(graph_right, width=9), dbc.Col(text_2, width=3)],
                        align="center",
                    ),
                ]
            ),
            color=C_4,
        )
    ]
)


# -------------- callbacks ------------------------------
@callback(Output("my-graph-3", "figure"), [Input("my-slider-3", "value")])
def update_map(value):
    dff = prepare_map(df_vote, value)
    palette_blue = px.colors.sequential.YlGnBu
    palette_red = px.colors.sequential.Reds
    fig = px.choropleth(
        dff,
        locations="Code",
        color="female_suffrage_lied",
        hover_name="Entity",
        hover_data=["female_suffrage_lied"],
        color_discrete_map={
            "No": palette_red[-4],
            "Yes": palette_blue[-4],
            "Missing Data": "LightGrey",
        },
        custom_data=["Entity", "female_suffrage_lied"],
    )
    fig.update_traces(
        hovertemplate="%{customdata[0]}"  # <br>Voting right for women: %{customdata[1]}
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(
            title="Voting right for women",
            traceorder="normal",
        ),
        geo=dict(
            showframe=False,
            showcountries=True,
            landcolor="White",
            projection_type="natural earth",
            lataxis_range=(-60, 80),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",  # autosize = True, #width=1300, height=500,
        dragmode="zoom",
        # dragmode=False,
        transition=dict(duration=50),
        clickmode="event+select",
    )

    return fig


@callback(Output("voting-right", "children"), Input("my-graph-3", "selectedData"))
def voting_rights(selectedData):

    if selectedData is None:
        return "No selected country"

    country, year = gender_infos(df_vote, selectedData, "female_suffrage_lied")
    # if still no right to vote year == -1
    if year != -1:
        if np.isnan(year):
            s = "There are no data for that country"
        else:
            s = f"In {country}, women obtained the right to vote in {year}."
    else:
        s = f"In {country}, women do not have the right to vote. "
    return s


@callback(Output("my-graph-4", "figure"), [Input("my-slider-4", "value")])
def update_map(value):
    dff = prepare_map(df_right, value)
    palette_blue = px.colors.sequential.YlGnBu
    palette_red = px.colors.sequential.Reds
    fig = px.choropleth(
        dff,
        locations="Code",
        color="accessjust_w_row_owid",
        hover_name="Entity",
        hover_data=["accessjust_w_row_owid"],
        color_discrete_map={
            "No": palette_red[-4],
            "Yes": palette_blue[-4],
            "Missing Data": "LightGrey",
        },
        custom_data=["Entity", "accessjust_w_row_owid"],
    )
    fig.update_traces(
        hovertemplate="%{customdata[0]}"  # <br>Voting right for women: %{customdata[1]}
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(
            title="Access to justice for women",
            traceorder="normal",
        ),
        geo=dict(
            lataxis_range=(-60, 80),
            showframe=False,
            showcountries=True,
            landcolor="White",
            projection_type="natural earth",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        dragmode="zoom",
        transition=dict(duration=50),
        clickmode="event+select",
    )
    return fig


@callback(Output("access-justice", "children"), Input("my-graph-4", "selectedData"))
def access_justice(selectedData):

    if selectedData is None:
        return "No selected country"

    country, year = gender_infos(df_right, selectedData, "accessjust_w_row_owid")

    if year != -1:
        if np.isnan(year):
            s = "There are no data for that country"
        else:
            s = f"In {country}, women have secure access to justice since {year}."
    else:
        s = f"In {country}, women do not have secure access to justice."
    return s
