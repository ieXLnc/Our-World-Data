from dash import Dash, dcc, html, Input, Output, register_page, callback
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df_vote = pd.read_csv(
    "C:/Users/xavier/PycharmProjects/Dashboard/gender/gender_equality_vote.csv"
)
df_right = pd.read_csv(
    "C:/Users/xavier/PycharmProjects/Dashboard/gender/gender_equality_right.csv"
)


def prepare_map(df, year):
    df_yr = df.loc[df["Year"] == year]
    df_yr = df_yr.fillna("No data")
    return df_yr


# -------------------Build layout--------------------------
text = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.H4("Universal right to vote for women"),
                        ],
                        style={"textAlign": "center", "height": "45vh"},
                    ),
                ]
            )
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
                                value=1800,
                                min=1800,
                                max=2021,
                                marks=None,
                                updatemode="drag",
                                tooltip={"placement": "bottom", "always_visible": True},
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
                                style={
                                    "width": "100%",
                                    "height": "100%",
                                    "Align": "center",
                                },
                            )
                        ]
                    ),
                ]
            )
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
                        ],
                        style={"textAlign": "center", "height": "45vh"},
                    ),
                ]
            )
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
                                value=1800,
                                min=1800,
                                max=2021,
                                marks=None,
                                updatemode="drag",
                                tooltip={"placement": "bottom", "always_visible": True},
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
                                    "width": "100%",
                                    "height": "100%",
                                    "Align": "center",
                                },
                            )
                        ]
                    ),
                ]
            )
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
            )
        )
    ]
)


# -------------- callbacks ------------------------------
@callback(Output("my-graph-3", "figure"), [Input("my-slider-3", "value")])
def update_map(value):
    dff = prepare_map(df_vote, value)
    palette = px.colors.sequential.YlGnBu
    fig = px.choropleth(
        dff,
        locations="Code",
        color="female_suffrage_lied",
        hover_name="Entity",
        hover_data=["female_suffrage_lied"],
        color_discrete_map={"No": palette[0], "Yes": palette[-1], "No Data": "grey"},
        # animation_frame="Year", animation_group="Code"
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(
            title="Voting right for women",
            # itemclick="toggleothers",
            traceorder="normal",
        ),
        geo=dict(
            showframe=False,
            showcountries=True,
            landcolor="LightGrey",
            projection_type="natural earth",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",  # autosize = True, #width=1300, height=500,
        # dragmode='zoom',
        dragmode=False,
        transition=dict(duration=50),
        clickmode="select",
    )

    return fig


@callback(Output("my-graph-4", "figure"), [Input("my-slider-4", "value")])
def update_map(value):
    dff = prepare_map(df_right, value)
    palette = px.colors.sequential.YlGnBu
    fig = px.choropleth(
        dff,
        locations="Code",
        color="accessjust_w_row_owid",
        hover_name="Entity",
        hover_data=["accessjust_w_row_owid"],
        color_discrete_map={"No": palette[0], "Yes": palette[-1], "No Data": "grey"},
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(
            title="Access to justice for women",
            # itemclick="toggleothers",
            traceorder="normal",
        ),
        geo=dict(
            showframe=False,
            showcountries=True,
            landcolor="LightGrey",
            projection_type="natural earth",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",  # autosize = True, #width=1300, height=500,
        dragmode=False,
        transition=dict(duration=50),
        clickmode="select",
    )

    return fig
