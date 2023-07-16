"""
This APP simulates first order batch reactions
"""
from dash import Dash, dcc, html, dash_table, dependencies
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from scipy.integrate import odeint
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server      # exposes server of dash app as an objective that gunicorn can pick
app.title = 'Tennis League Eligibility Checker'  # set the title to appear in the tab

########################### Define all my content #####################################################################

gender_dropdown = dbc.DropdownMenu(
    label="Select Gender",
    children=[
        dbc.DropdownMenuItem("Ladies"),
        dbc.DropdownMenuItem("Men's"),
    ],
)

team_dropdown = dbc.DropdownMenu(
    label="Team Number",
    children=[
        dbc.DropdownMenuItem("1"),
        dbc.DropdownMenuItem("2"),
        dbc.DropdownMenuItem("3"),
        dbc.DropdownMenuItem("4"),
        dbc.DropdownMenuItem("5"),
        dbc.DropdownMenuItem("6"),
        dbc.DropdownMenuItem("7"),
    ],
)

# you can provide images from local files or url to the internet
instruct_tab = dbc.Card(
        html.Div(
            [
            #dbc.CardImg(src="https://i.postimg.cc/wBxrRxy9/batch-reactor-image.png", top=True, style={'height':'65%', 'width':'65%'}),
            dbc.CardImg(src='../assets/batch-reactor-image.png', top=True, style={'height':'65%', 'width':'65%'}),
            dbc.CardBody(html.P("Interested in learning more about Donnybrook tennis, see https://www.donnybrookltc.ie/", className="card-text")),
            ],
            style={'textAlign': 'center'},
        )
)

drop_down_menus = html.Div(
    [
        gender_dropdown,
        team_dropdown
    ]
)

reg_team = pd.read_csv('../assets/teams.csv')
reg_team_relevant = reg_team[['Team', 'Position', 'Name']]
reg_team_relevant = reg_team_relevant.rename(columns={'Name': 'Registered'})

prev_weeks = pd.read_csv('../assets/previous_weeks.csv')
reg_team_prev_weeks = pd.merge(reg_team_relevant, prev_weeks, on=['Team', 'Position'])

DashTableMainBody = html.Div(
    [
    dash_table.DataTable(
        id='RegPrevWeekTable',
        columns=[{"name": i, "id": i} for i in reg_team_prev_weeks.columns],
        data=reg_team_prev_weeks.to_dict('records'),
        )
    ]
)

left_right_sections_for_top = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(drop_down_menus, width=6),
                dbc.Col(instruct_tab, width=6)
            ]

        )

    ]
)


top_section = html.Div(
    [
    html.H2('Web App to Check if League Team meets DLTC Eligibility Rules'),
    DashTableMainBody
    ]
)


content = html.Div(
    [
    top_section,
    ]
)
app.layout = content


if __name__ == '__main__':
    app.run_server(debug=True)  # Set debug to true makes webapp automatically update, when user clicks refresh
    #app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
