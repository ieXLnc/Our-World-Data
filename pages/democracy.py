from dash import Dash, dcc, html, Input, Output, register_page, callback
import os
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

static = "static/"
df_electoral = pd.read_csv(os.path.join(static, "democracy.csv"))
df_civil = pd.read_csv(os.path.join(static, "civil-liberties-eiu.csv"))
df_democracy = pd.read_csv(os.path.join(static, "democracies_autocracies.csv"))


def prepare_map(df, year):
    df_yr = df.loc[df["Year"] == year]
    df_yr = df_yr.drop(df_yr.loc[df_yr["Entity"] == "Antarctica"].index)
    df_yr = df_yr.fillna("No data")
    return df_yr


def prepare_line(df, country):
    mask = df[df["Entity"] == country]
    return mask


def prepare_scatter(df, year):
    df_w = df.loc[df["Entity"] == "World"]
    df_yr = df_w.loc[df_w["Year"] <= year]
    df_yr = df_yr.fillna("No data")

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
            color="#D6CDA4",
            style={"height": "40vh", "border-color": "rgba(0,0,0,0)"},
        )
    ]
)

text_exp_2 = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "Electoral democracy",
                    ),  # style={'font-size':"90%"}
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
            color="#D6CDA4",
            style={"height": "45vh", "border-color": "rgba(0,0,0,0)"},
        )
    ]
)

text_exp_3 = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "Civil liberties",
                    ),  # style={'font-size':"90%"}
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
            color="#D6CDA4",
            style={"height": "45vh", "border-color": "rgba(0,0,0,0)"},
        )
    ]
)

id_country_dem = html.Div(
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
            color="#EEF2E6",
            style={"height": "45vh", "border-color": "rgba(0,0,0,0)"},
        )
    ]
)

id_country_civ = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(id="text-country", style={"TextAlign": "center"}),
                    #
                    dcc.Graph(
                        id="line-country-civ",
                        style={"height": "40vh"},
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
                    ),
                ]
            ),
            color="#EEF2E6",
            style={"height": "45vh", "border-color": "rgba(0,0,0,0)"},
        )
    ]
)

map_elect = html.Div(
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

map_civil_lib = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Slider(
                        id="my-slider-6",
                        value=df_civil["Year"].max(),
                        min=df_civil["Year"].min(),
                        max=df_civil["Year"].max(),
                        step=1,
                        marks=None,
                        updatemode="drag",
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Graph(
                        id="graph-civil",
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
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
            color="#EEF2E6",
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
                            dbc.Col(text_exp_2, width=2),
                            dbc.Col(id_country_dem, width=4),
                            dbc.Col(text_exp_3, width=2),
                            dbc.Col(id_country_civ, width=4),
                        ],
                        align="center",
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(map_elect, width=6),
                            dbc.Col(map_civil_lib, width=6),
                        ],
                        align="center",
                    ),
                ]
            ),
            color="#EEF2E6",
        )
    ]
)

# ----------------Callbacks--------------------------
@callback(Output("graph-electoral", "figure"), [Input("my-slider-5", "value")])
def map_electoral_democracy(value):
    dff = prepare_map(df_electoral, value)
    palette = px.colors.sequential.YlGnBu
    fig = px.choropleth(
        dff,
        locations="Code",
        color="electdem_vdem_owid",
        hover_name="Entity",
        hover_data=["electdem_vdem_owid"],
        color_continuous_scale=palette,
        range_color=(0, 1),
        custom_data=[
            "Entity",
            "Year",
            "electdem_vdem_owid",
            "electdem_vdem_high_owid",
            "electdem_vdem_low_owid",
        ],
    )
    fig.update_traces(
        hovertemplate="%{customdata[0]} in %{customdata[1]}: <br>Democracy score: %{customdata[2]} <br>"
        "Upper bound: %{customdata[3]} <br>Lower bound: %{customdata[4]}"
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        geo=dict(
            showframe=False,
            showcountries=True,
            landcolor="LightGrey",
            projection_type="natural earth",
            fitbounds="locations",
            visible=False,
        ),
        legend=dict(),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        dragmode="zoom",
        transition=dict(duration=0),
        clickmode="event+select",
    )
    fig.update_coloraxes(
        colorbar=dict(
            y=-0.15, orientation="h", len=0.7, thickness=15, title="Democracy score"
        )
    )
    return fig


@callback(
    Output("line-country-dem", "figure"),
    Input("graph-electoral", "clickData"),
)
def line_id_country_dem(clickData):
    if clickData is None:
        country = "Belgium"
    else:
        country = clickData["points"][0]["hovertext"]
    dff = prepare_line(df_electoral, country)
    palette = px.colors.sequential.YlGnBu
    fig = px.line(
        dff,
        x="Year",
        y="electdem_vdem_owid",  #'electdem_vdem_high_owid', 'electdem_vdem_low_owid'],
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


@callback(Output("graph-civil", "figure"), [Input("my-slider-6", "value")])
def map_civil_liberties(value):
    dff = prepare_map(df_civil, value)
    palette = px.colors.sequential.YlGnBu
    fig = px.choropleth(
        dff,
        locations="Code",
        color="civlib_eiu",
        hover_name="Entity",
        hover_data=["civlib_eiu"],
        color_continuous_scale=px.colors.sequential.YlGnBu,
        range_color=(0, 10),
        custom_data=["Entity", "Year", "civlib_eiu"],
    )
    fig.update_traces(
        hovertemplate="%{customdata[0]} in %{customdata[1]}: <br>Civil liberties score: %{customdata[2]}"
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        geo=dict(
            showframe=False,
            showcountries=True,
            landcolor="LightGrey",
            projection_type="natural earth",
            fitbounds="locations",
            visible=False,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        dragmode="zoom",
        transition=dict(duration=0),
        clickmode="event+select",
    )
    fig.update_coloraxes(
        colorbar=dict(
            y=-0.15,
            orientation="h",
            len=0.7,
            thickness=15,
            title="Civil liberties score",
        )
    )
    return fig


@callback(Output("line-country-civ", "figure"), [Input("graph-civil", "clickData")])
def line_id_country_civ(clickData):
    if clickData is None:
        country = "Belgium"
    else:
        country = clickData["points"][0]["hovertext"]
    dff = prepare_line(df_civil, country)
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


@callback(Output("graph-line-democracy", "figure"), [Input("my-slider-7", "value")])
def map_people_democracies(value):
    palette = px.colors.sequential.Viridis
    dff = prepare_scatter(df_democracy, value)
    fig = px.area(
        dff,
        x="Year",
        y=[
            "no regime data",
            "closed autocraties",
            "electoral autocraties",
            "electoral democraties",
            "liberal democraties",
        ],
        color_discrete_map={
            "no regime data": "grey",
            "closed autocraties": palette[0],
            "electoral autocraties": palette[2],
            "electoral democraties": palette[-2],
            "liberal democraties": palette[-1],
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
