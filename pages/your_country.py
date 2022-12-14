from dash import Dash, dcc, html, Input, Output, register_page, callback
import os
import sqlite3
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from constant import STATIC, DB, C_1, C_2, C_3, C_4

# connect to database
con = sqlite3.connect(os.path.join(STATIC, DB))
cur = con.cursor()

df_co2 = pd.read_sql_query(
    "SELECT Code, Entity, Year, Annual_CO2_emissions "
    "from World_data WHERE Year >= 1800",
    con,
)

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

df_electoral = pd.read_sql_query(
    "SELECT Code, Entity, Year, electdem_vdem_owid, electdem_vdem_high_owid, electdem_vdem_low_owid "
    "from World_data "
    "WHERE Year >= 1800",
    con,
)

df_civil = pd.read_sql_query(
    "SELECT Code, Entity, Year, civlib_eiu " "from World_data " "WHERE Year >= 1800",
    con,
)


def get_empty_map(df):
    dff = df.loc[df.Year == 2020, ["Code", "Entity"]]
    dff = dff.drop(dff.loc[dff["Entity"] == "Antarctica"].index)
    dff["values"] = 0
    return dff


def map_selection():
    dff = get_empty_map(df_co2)
    palette = px.colors.sequential.YlGnBu
    fig = px.choropleth(
        dff,
        locations="Code",
        color="values",
        hover_name="Entity",
        hover_data=["Entity"],
        color_continuous_scale=palette,
        custom_data=["Entity"],
    )
    fig.update_traces(hovertemplate="%{customdata[0]}")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title={
            "text": "Select a country!",
            "y": 0.99,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        margin=dict(t=25, b=0, l=0, r=0),
        geo=dict(
            showframe=False,
            showcountries=True,
            landcolor="LightGrey",
            projection_type="natural earth",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        dragmode="zoom",
        transition=dict(duration=0),
        clickmode="event+select",
    )
    fig.update(layout_coloraxis_showscale=False)

    return fig


def gender_infos(df, selectedData, var):
    if selectedData is None:
        mask = "Belgium"
        dff_g = df[df["Entity"] == mask]
    else:
        mask = selectedData["points"][0]["hovertext"]
        dff_g = df[df["Entity"] == mask]

    max_year = dff_g.Year.max()
    if dff_g.loc[dff_g.Year == max_year, var].values[0] == "No":
        year = -1
        return mask, year
    else:
        year = dff_g.loc[dff_g[var] == "Yes", "Year"].min()
        return mask, year


# CO2 line plot
def prepare_scatter(df, year, selectedData):
    # record the last one to remove selection if double click
    if selectedData is None:
        mask = "Belgium"
        df_p = df[df["Entity"] == mask]
    else:
        mask = selectedData["points"][0]["hovertext"]
        df_p = df[df["Entity"] == mask]

    df_p_yr = df_p.loc[df["Year"] <= year]
    # drop na for the graph
    df_p_yr.dropna(axis=0, inplace=True)

    return mask, df_p_yr


def prepare_line(df, country):
    df = df[df["Entity"] == country]
    # df = df.fillna(method='bfill')
    return df


# -------------------Build layout--------------------------
about_your_country = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("What about your country?"),
                    html.P("Find out the statistics on a specific country!"),
                    html.P("Select a country on the map to know more about it"),
                ],
                style={"height": "45vh"},
            ),
            color=C_3,
            style={"border-color": "rgba(0,0,0,0)"},
        )
    ]
)

map_select = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Center(
                        dcc.Graph(
                            id="map-selection-country",
                            figure=map_selection(),
                            style={"height": "40vh"},
                            config={
                                "displaylogo": False,
                                "displayModeBar": False,
                            },
                        )
                    )
                ],
                style={"height": "45vh"},
            ),
            style={"border-color": "rgba(0,0,0,0)"},
        )
    ]
)

gender_tab = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("Gender Equality"),
                    html.Div(id="gender-equality-info", style={"font-size": "25px"}),
                ],
                style={"height": "45vh"},
            ),
            style={"border-color": "rgba(0,0,0,0)"},
            color=C_4,
        )
    ]
)


co2_tab = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Slider(
                        id="my-slider-8",
                        value=df_co2["Year"].max(),
                        min=df_co2["Year"].min(),
                        max=df_co2["Year"].max(),
                        marks=None,
                        updatemode="drag",
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Graph(
                        id="co2-graph",
                        style={"height": "35vh"},
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
                    ),
                ],
                style={"height": "45vh"},
            ),
            style={"border-color": "rgba(0,0,0,0)"},
            color=C_4,
        )
    ]
)

dem_tab = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="graph-democracy-score",
                        style={"height": "40vh"},
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
                    )
                ],
                style={"height": "45vh"},
            ),
            style={"border-color": "rgba(0,0,0,0)"},
            color=C_4,
        )
    ]
)

civil_tab = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="graph-civil-score",
                        style={"height": "40vh"},
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
                    )
                ],
                style={"height": "45vh"},
            ),
            style={"border-color": "rgba(0,0,0,0)"},
            color=C_4,
        )
    ]
)

# -------------------Build page-------------------------------
register_page(
    __name__,
    use_pages=True,
    path="/your-country",
    external_stylesheets=[dbc.themes.LUX],
)

layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(about_your_country, width=4),
                            dbc.Col(map_select, width=8),
                        ],
                        align="center",
                        justify="center",
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(gender_tab, width=4),
                            dbc.Col(dem_tab, width=4),
                            dbc.Col(civil_tab, width=4),
                        ],
                        align="center",
                        justify="center",
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(co2_tab, width=12),
                        ],
                        align="center",
                        justify="center",
                    ),
                ]
            ),
            color=C_4,
        )
    ]
)


# ----------------Callbacks--------------------------
@callback(
    Output("gender-equality-info", "children"),
    Input("map-selection-country", "clickData"),
)
def gender_text(clickData):

    country, year_vote = gender_infos(df_vote, clickData, "female_suffrage_lied")
    country, year_right = gender_infos(df_right, clickData, "accessjust_w_row_owid")

    if year_vote != -1 and year_right != -1:
        s = (
            f"In {country}, women obtained the right to vote in {year_vote}."
            + f"They have secure access to justice since {year_right}."
        )

    elif year_vote != -1 and year_right == -1:
        s = (
            f"In {country}, women obtained the right to vote in {year_vote}. "
            f"Unfortunately, they still do not have secure access to justice."
        )
    else:
        s = (
            f"In {country}, women do not have the right to vote. "
            f"They do not have secure access to justice."
        )

    return s


@callback(
    Output("co2-graph", "figure"),
    [Input("my-slider-8", "value"), Input("map-selection-country", "clickData")],
)
def update_graph(value, clickData):
    country, dff = prepare_scatter(df_co2, value, clickData)
    fig = px.line(
        dff,
        x="Year",
        y="Annual_CO2_emissions",
        color="Entity",
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=25, b=0, l=25, r=25),
        showlegend=False,
        title={
            "text": f"CO2 Emissions for {country}",
            "y": 0.99,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )
    fig.update_xaxes(
        showgrid=True,
        range=[dff.Year.min(), dff.Year.max()],
        gridcolor="LightGrey",
    )
    fig.update_yaxes(
        showgrid=True,
        # color='LightGrey',
        gridcolor="LightGrey",
    )
    return fig


@callback(
    Output("graph-democracy-score", "figure"),
    Input("map-selection-country", "clickData"),
)
def update_graph(clickData):
    if clickData is None:
        country = "Belgium"
    else:
        country = clickData["points"][0]["hovertext"]
    dff_d = prepare_line(df_electoral, country)
    dff_d = dff_d.dropna(axis=0)
    fig = px.line(
        dff_d,
        x="Year",
        y="electdem_vdem_owid",
        color="Entity",
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
        custom_data=["Entity", "Year", "electdem_vdem_owid"],
        labels={"electdem_vdem_owid": "Democracy score"},
    )
    fig.update_traces(
        hovertemplate="%{customdata[1]}<br>" "Democracy score: %{customdata[2]}"
    )
    fig.update_layout(
        title=f"Electoral democracy score for {country}",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    fig.update_xaxes(
        showgrid=True,
        range=[dff_d.Year.min(), dff_d.Year.max()],
        gridcolor="LightGrey",
    )
    fig.update_yaxes(
        showgrid=True,
        range=(0, 1),
        gridcolor="LightGrey",
    )
    return fig


@callback(
    Output("graph-civil-score", "figure"),
    Input("map-selection-country", "clickData"),
)
def update_graph(clickData):
    if clickData is None:
        country = "Belgium"
    else:
        country = clickData["points"][0]["hovertext"]
    dff_c = prepare_line(df_civil, country)
    dff_c = dff_c.loc[dff_c.Year >= 2006]
    dff_c = dff_c.fillna(method="bfill")
    fig = px.line(
        dff_c,
        x="Year",
        y="civlib_eiu",
        color="Entity",
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
        custom_data=["Entity", "Year", "civlib_eiu"],
        labels={"civlib_eiu": "Civil liberties score"},
    )
    fig.update_traces(
        hovertemplate="%{customdata[1]}<br>" "Civil liberties score: %{customdata[2]}"
    )
    fig.update_layout(
        title=f"Civil liberties score for {country}",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    fig.update_xaxes(
        showgrid=True,
        range=[dff_c.Year.min(), dff_c.Year.max()],
        gridcolor="LightGrey",
    )
    fig.update_yaxes(
        showgrid=True,
        range=(0, 10),
        gridcolor="LightGrey",
    )
    return fig
