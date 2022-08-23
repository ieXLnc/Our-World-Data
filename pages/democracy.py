from dash import Dash, dcc, html, Input, Output, register_page, callback
import dash
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df_electoral = pd.read_csv(
    "C:/Users/xavier/PycharmProjects/Dashboard/democracy/democracy.csv"
)
df_civil = pd.read_csv(
    "C:/Users/xavier/PycharmProjects/Dashboard/democracy/civil-liberties-eiu.csv"
)
df_democracy = pd.read_csv(
    "C:/Users/xavier/PycharmProjects/Dashboard/democracy/people-living-in-democracies-womsuffr-bmr.csv"
)


def prepare_map(df, year):
    df_yr = df.loc[df["Year"] == year]
    df_yr = df_yr.fillna("No data")
    return df_yr


def prepare_line(df, country):
    mask = df[df["Entity"] == country]
    return mask


def prepare_scatter(df, year):
    df_yr = df.loc[df["Year"] <= year]
    df_yr = df_yr.fillna("No data")

    return df_yr


# -------------------Build layout--------------------------
text_exp = html.Div(
    [dbc.Card(dbc.CardBody([html.P("Cool exp here", style={"TextAlign": "center"})]))]
)

id_country = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(id="text-country", style={"TextAlign": "center"}),
                    #
                    dcc.Graph(
                        id="line-country",
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

map_elect = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Slider(
                        id="my-slider-5",
                        value=1800,
                        min=1800,
                        max=df_civil["Year"].max(),
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
                        value=df_civil["Year"].min(),
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
                        value=df_democracy["Year"].min(),
                        min=df_democracy["Year"].min(),
                        max=df_democracy["Year"].max(),
                        marks=None,
                        updatemode="drag",
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Graph(id="graph-line-democracy"),
                ]
            )
        )
    ]
)


# -------------------Build app-----------------------------
register_page(__name__, path="/democracy", external_stylesheets=[dbc.themes.MINTY])

layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(text_exp, width=2),
                            dbc.Col(id_country, width=4),
                            dbc.Col(map_elect, width=6),
                        ],
                        align="center",
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(map_civil_lib, width=6),
                            dbc.Col(line_democracy, width=6),
                        ]
                    ),
                ]
            )
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
        color_continuous_scale=px.colors.sequential.YlGnBu,
        range_color=(0, 1),
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
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
        transition=dict(duration=50),
        clickmode="select",
    )
    fig.update_coloraxes(
        colorbar=dict(
            y=-0.15, orientation="h", len=0.7, thickness=15, title="Democracy score"
        )
    )
    return fig


@callback(
    Output("line-country", "figure"),
    Input("graph-electoral", "hoverData"),
)
def line_id_country(hoverData):
    if hoverData is None:
        country = "Belgium"
    else:
        country = hoverData["points"][0]["hovertext"]
    dff = prepare_line(df_electoral, country)
    palette = px.colors.sequential.YlGnBu
    fig = px.line(
        dff,
        x="Year",
        y=["electdem_vdem_owid"],  # 'electdem_vdem_high_owid', 'electdem_vdem_low_owid'
        color="Entity",
    )
    fig.update_layout(
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
        range=(0, 1),
        # color='LightGrey',
        gridcolor="LightGrey",
    )

    return fig


@callback(
    Output("text-country", "children"),
    Input("graph-electoral", "hoverData"),
)
def text_country(hoverData):
    if hoverData is None:
        country = "Belgium"
    else:
        country = hoverData["points"][0]["hovertext"]
    return f"Electoral democracy score for {country}"


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
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
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
        transition=dict(duration=50),
        clickmode="select",
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


@callback(Output("graph-line-democracy", "figure"), [Input("my-slider-7", "value")])
def map_people_democracies(value):
    dff = prepare_scatter(df_democracy, value)
    fig = px.area(
        dff,
        x="Year",
        y=[
            "pop_missreg_bmr_owid",
            "pop_nondem_womsuffr_bmr_owid",
            "pop_dem_womsuffr_bmr_owid",
        ],
        color=[
            "pop_missreg_bmr_owid",
            "pop_nondem_womsuffr_bmr_owid",
            "pop_dem_womsuffr_bmr_owid",
        ],
    )
    return fig
