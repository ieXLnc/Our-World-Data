from dash import Dash, dcc, html, Input, Output, register_page, callback
import os
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from constant import STATIC, DB, C_1, C_2, C_3, C_4


# connect to database
con = sqlite3.connect(os.path.join(STATIC, DB))
cur = con.cursor()

df_electoral = pd.read_sql_query(
    "SELECT Code, Entity, Year, electdem_vdem_owid, electdem_vdem_high_owid, electdem_vdem_low_owid, dem_score_rounded "
    "from World_data "
    "WHERE Year >= 1800",
    con,
)

df_civil = pd.read_sql_query(
    "SELECT Code, Entity, Year, civlib_eiu, civil_string "
    "from World_data "
    "WHERE Year >= 1800",
    con,
)

df_democracy = pd.read_sql_query(
    "SELECT Code, Entity, Year, no_regime_data, closed_autocraties, electoral_autocraties, electoral_democraties, liberal_democraties "
    "from World_data "
    "WHERE Year >= 1800",
    con,
)


def prepare_map(df, year):
    df_yr = df.loc[df["Year"] == year]
    df_yr = df_yr.drop(df_yr.loc[df_yr["Entity"] == "Antarctica"].index)
    df_yr = df_yr.fillna("Missing Data")
    return df_yr


def prepare_line(df, country):
    df = df.loc[df["Entity"] == country]
    # df = df.fillna(0)
    return df


def prepare_scatter(df, year):
    df_w = df.loc[df["Entity"] == "World"]
    df_yr = df_w.loc[df_w["Year"] <= year]
    df_yr = df_yr.fillna(0)
    return df_yr


# -------------------Build layout--------------------------
text_exp_1 = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "People living in democracies and autocracies in the world"
                    ),
                    html.P(
                        """Political regimes based on the criteria of the classification by Lührmann et al. (2018) and the assessment by V-Dem’s
                            experts.""",
                        style={"TextAlign": "center", "height": "35vh"},
                    ),
                ]
            ),
            color=C_3,
            style={"height": "40vh", "border-color": "rgba(0,0,0,0)"},
        )
    ]
)

text_exp_2 = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        ["Democracy Score", "Civil liberties Score"],
                        "Democracy Score",
                        id="dropdown-1",
                    ),
                    html.Br(),
                    html.Div(id="card-expl"),
                ]
            ),
            color=C_3,
            style={"height": "45vh", "border-color": "rgba(0,0,0,0)"},
        )
    ]
)

id_country = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(id="text-country", style={"TextAlign": "center"}),
                    #
                    dcc.Graph(
                        id="line-country-dem",
                        style={"height": "40vh"},
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
                    ),
                ]
            ),
            color=C_4,
            style={"height": "45vh", "border-color": "rgba(0,0,0,0)"},
        )
    ]
)


map_democracy = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Slider(
                        id="my-slider-5",
                        value=df_electoral["Year"].max(),
                        min=df_electoral["Year"].min(),
                        max=df_electoral["Year"].max(),
                        marks=None,
                        updatemode="drag",
                        tooltip={"placement": "bottom", "always_visible": True},
                        step=1,
                    ),
                    html.Div(
                        [
                            dcc.Graph(
                                id="graph-electoral",
                                config={
                                    "displaylogo": False,
                                    "displayModeBar": False,
                                },
                            ),
                        ]
                    ),
                ]
            )
        )
    ]
)


line_democracy = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Slider(
                        id="my-slider-7",
                        value=df_democracy["Year"].max(),
                        min=df_democracy["Year"].min(),
                        max=df_democracy["Year"].max(),
                        marks=None,
                        updatemode="drag",
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Graph(
                        id="graph-line-democracy",
                        style={"height": "35vh"},
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
                    ),
                ]
            ),
            color=C_4,
            style={"border-color": "rgba(0,0,0,0)"},
        )
    ]
)


# -------------------Build app-----------------------------
register_page(__name__, path="/democracy", external_stylesheets=[dbc.themes.LUX])

layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(text_exp_1, width=4),
                            dbc.Col(line_democracy, width=8),
                        ],
                        align="center",
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(text_exp_2, width=4),
                            dbc.Col(id_country, width=8),
                            # dbc.Col(text_exp_3, width=2),
                            # dbc.Col(id_country_civ, width=4),
                        ],
                        align="center",
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(map_democracy, width=12),
                            # dbc.Col(map_civil_lib, width=6),
                        ],
                        align="center",
                    ),
                ]
            ),
            color=C_4,
        )
    ]
)

# ----------------Callbacks--------------------------
# EXPLANATIONS
@callback(Output("card-expl", "children"), Input("dropdown-1", "value"))
def create_expl_card(value_dropdown):
    if value_dropdown == "Democracy Score":
        expl = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "Electoral democracy",
                    ),
                    html.P(
                        """Based on the expert assessments and index by V-Dem. It captures to which extent political leaders are elected under
                                comprehensive voting rights in free and fair elections, and freedoms of association and expression are guaranteed. It
                                ranges from 0 to 1 (most democratic).""",
                        style={
                            "TextAlign": "center",
                            "height": "40vh",
                            "font-size": "13px",
                        },
                    ),
                ]
            ),
            color=C_3,
            style={"height": "30vh", "border-color": "rgba(0,0,0,0)"},
        )

    else:
        expl = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "Civil liberties",
                    ),
                    html.P(
                        """Based on the expert assessments and index by the Economist Intelligence Unit (2022). It ranges from 0 to 10 (most
                        liberties).""",
                        style={
                            "TextAlign": "center",
                            "height": "40vh",
                            "font-size": "13px",
                        },
                    ),
                ]
            ),
            color=C_3,
            style={"height": "30vh", "border-color": "rgba(0,0,0,0)"},
        )
    return expl


# MAPS
@callback(
    Output("graph-electoral", "figure"),
    Input("my-slider-5", "value"),
    Input("dropdown-1", "value"),
)
def map_electoral_democracy(value, value_dropdown):

    if value_dropdown == "Democracy Score":
        dff = prepare_map(df_electoral, value)
        palette_p = px.colors.sequential.YlGnBu
        palette_n = px.colors.sequential.Reds
        fig = px.choropleth(
            dff,
            locations="Code",
            color="dem_score_rounded",
            hover_name="Entity",
            hover_data=["electdem_vdem_owid"],
            category_orders={
                "dem_score_rounded": [
                    "0 - 0.1",
                    "0.1 - 0.2",
                    "0.2 - 0.3",
                    "0.3 - 0.4",
                    "0.4 - 0.5",
                    "0.5 - 0.6",
                    "0.6 - 0.7",
                    "0.7 - 0.8",
                    "0.8 - 0.9",
                    "0.9 - 1",
                ]
            },
            color_discrete_map={
                "Missing Data": "LightGrey",
                "0 - 0.1": palette_n[7],
                "0.1 - 0.2": palette_n[6],
                "0.2 - 0.3": palette_n[5],
                "0.3 - 0.4": palette_n[3],
                "0.4 - 0.5": palette_p[1],
                "0.5 - 0.6": palette_p[2],
                "0.6 - 0.7": palette_p[4],
                "0.7 - 0.8": palette_p[5],
                "0.8 - 0.9": palette_p[6],
                "0.9 - 1": palette_p[8],
            },
            custom_data=[
                "Entity",
                "Year",
                "electdem_vdem_owid",
                "electdem_vdem_high_owid",
                "electdem_vdem_low_owid",
            ],
            title="Democracy score",
        )
        fig.update_traces(
            hovertemplate="%{customdata[0]} in %{customdata[1]}: <br>Democracy score: %{customdata[2]} <br>"
            "Upper bound: %{customdata[3]} <br>Lower bound: %{customdata[4]}"
        )
        fig.update_layout(
            legend=dict(
                # try to create the bar
                y=-0.15,
                x=0.1,
                orientation="h",
                valign="top",
                itemclick="toggleothers",
                title="Democracy score",
            )
        )

    else:

        dff = prepare_map(df_civil, value)
        palette_p = px.colors.sequential.YlGnBu
        palette_n = px.colors.sequential.Reds
        fig = px.choropleth(
            dff,
            locations="Code",
            color="civil_string",
            hover_name="Entity",
            hover_data=["civlib_eiu"],
            category_orders={
                "civil_string": [
                    "0 - 1",
                    "1 - 2",
                    "2 - 3",
                    "3 - 4",
                    "4 - 5",
                    "5 - 6",
                    "6 - 7",
                    "7 - 8",
                    "8 - 9",
                    "9 - 10",
                ]
            },
            color_discrete_map={
                "Missing Data": "LightGrey",
                "0 - 1": palette_n[7],
                "1 - 2": palette_n[6],
                "2 - 3": palette_n[5],
                "3 - 4": palette_n[3],
                "4 - 5": palette_p[1],
                "5 - 6": palette_p[2],
                "6 - 7": palette_p[4],
                "7 - 8": palette_p[5],
                "8 - 9": palette_p[6],
                "9 - 10": palette_p[8],
            },
            custom_data=["Entity", "Year", "civlib_eiu"],
            title="Civil liberties score",
        )

        fig.update_traces(
            hovertemplate="%{customdata[0]} in %{customdata[1]}: <br>Civil liberties score: %{customdata[2]}"
        )
        fig.update_layout(
            legend=dict(
                # try to create the bar
                y=-0.15,
                x=0.1,
                orientation="h",
                valign="top",
                itemclick="toggleothers",
                title="Civil liberties score",
            )
        )

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        geo=dict(
            showframe=False,
            showcountries=True,
            landcolor="White",
            projection_type="natural earth",
            lataxis_range=(-70, 100),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        dragmode="zoom",
        transition=dict(duration=0),
        clickmode="event+select",
    )

    return fig


# line plots
@callback(
    Output("line-country-dem", "figure"),
    Input("graph-electoral", "clickData"),
    Input("dropdown-1", "value"),
)
def line_id_country_dem(clickData, value_dropdown):
    if clickData is None:
        country = "Belgium"
    else:
        country = clickData["points"][0]["hovertext"]

    if value_dropdown == "Democracy Score":
        dff = prepare_line(df_electoral, country)
        dff = dff.fillna(0)
        palette = px.colors.sequential.YlGnBu
        fig = px.line(
            dff,
            x="Year",
            y="electdem_vdem_owid",  # 'electdem_vdem_high_owid', 'electdem_vdem_low_owid'],
            color="Entity",
            labels={"electdem_vdem_owid": "Democracy score"},
        )
        fig.update_traces(line_color=palette[-1], hovertemplate=None)
        # upper bound
        fig.add_trace(
            go.Line(
                x=dff["Year"],
                y=dff["electdem_vdem_high_owid"],
                opacity=0.6,
                line=dict(color="Grey"),
                name="Upper bound",
            )
        )
        # lower bound
        fig.add_trace(
            go.Line(
                x=dff["Year"],
                y=dff["electdem_vdem_low_owid"],
                opacity=0.6,
                line=dict(color="Grey"),
                name="Lower bound",
            )
        )
        fig.update_layout(
            title=f"Electoral democracy score for {country}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            hovermode="x",
        )
        fig.update_xaxes(
            showgrid=True,
            # color='LightGrey',
            gridcolor="LightGrey",
        )
        fig.update_yaxes(
            showgrid=True,
            range=(0, 1),
            # color='LightGrey',
            gridcolor="LightGrey",
        )
        return fig

    else:
        dff = prepare_line(df_civil, country)
        dff = dff.loc[dff.Year >= 2006]
        dff.fillna(method="bfill", inplace=True)

        palette = px.colors.sequential.YlGnBu
        fig = px.line(
            dff,
            x="Year",
            y="civlib_eiu",
            color="Entity",
            custom_data=["Year", "civlib_eiu"],
            labels={"civlib_eiu": "Civil liberties score"},
        )
        fig.update_traces(
            hovertemplate="%{customdata[0]}: <br>Civil liberties score: %{customdata[1]}"
        )
        fig.update_layout(
            title=f"Civil liberties score for {country}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            legend=dict(),
        )
        fig.update_traces(line_color=palette[-1])
        fig.update_xaxes(
            showgrid=True,
            # color='LightGrey',
            gridcolor="LightGrey",
        )
        fig.update_yaxes(
            showgrid=True,
            range=(0, 10),
            # color='LightGrey',
            gridcolor="LightGrey",
        )
        return fig


# area plot how many people live under what
@callback(Output("graph-line-democracy", "figure"), [Input("my-slider-7", "value")])
def plot_area_people_regime(value):
    palette = px.colors.sequential.Viridis
    dff = prepare_scatter(df_democracy, value)
    fig = px.area(
        dff,
        x="Year",
        y=[
            "no_regime_data",
            "closed_autocraties",
            "electoral_autocraties",
            "electoral_democraties",
            "liberal_democraties",
        ],
        color_discrete_map={
            "no_regime_data": "grey",
            "closed_autocraties": palette[0],
            "electoral_autocraties": palette[2],
            "electoral_democraties": palette[-2],
            "liberal_democraties": palette[-1],
        },
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # dragmode="zoom",
        transition=dict(duration=0),
        # clickmode="select",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, font_color="black"),
    )
    fig.update_xaxes(
        showgrid=False,
        gridcolor="LightGrey",
    )
    fig.update_yaxes(
        showgrid=False,
        gridcolor="LightGrey",
    )
    return fig
