"""
This APP simulates first order batch reactions
"""
import dash
from dash import Dash, dcc, html, dash_table, dependencies, Input, Output, State, MATCH
from dash.dependencies import ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from scipy.integrate import odeint
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

from dashapp.tennis_callbacks import update_suggested_player

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server      # exposes server of dash app as an objective that gunicorn can pick
app.title = 'Tennis League Eligibility Checker'  # set the title to appear in the tab


########################### Define all my data objects #####################################################################

reg_team = pd.read_csv('../assets/teams.csv')
reg_team_relevant = reg_team[['Team', 'Position', 'Name']]
reg_team_relevant = reg_team_relevant.rename(columns={'Name': 'Registered'})

reg_subs = pd.read_csv('../assets/subs.csv')

prev_weeks = pd.read_csv('../assets/previous_weeks.csv')
reg_team_prev_weeks = pd.merge(reg_team_relevant, prev_weeks, on=['Team', 'Position'])

registered_players_series = pd.concat([reg_team['Name'], reg_subs['Name']])
registered_players_df = pd.DataFrame({'Name': registered_players_series})
registered_players_list = registered_players_series.tolist()


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

drop_down_menus = html.Div(
    [
        gender_dropdown,
        team_dropdown
    ]
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

player_selection = html.Div([
    html.H2('Select Your Team Here'),
    html.H6("The text boxes will display all the registered players in the system which match the spelling of what you have typed so far. You still need to write the player's coplete name"),
    dcc.Input(id='input-player-1', type='text', placeholder='Singles 1'),
    html.Div(id='output-player-1'),
    dcc.Input(id='input-player-2', type='text', placeholder='Singles 2'),
    html.Div(id='output-player-2'),
    dcc.Input(id='input-player-3', type='text', placeholder='Singles 3'),
    html.Div(id='output-player-3'),
    dcc.Input(id='input-player-4', type='text', placeholder='Doubles 1'),
    html.Div(id='output-player-4'),
    dcc.Input(id='input-player-5', type='text', placeholder='Doubles 1'),
    html.Div(id='output-player-5'),
    dcc.Input(id='input-player-6', type='text', placeholder='Doubles 2'),
    html.Div(id='output-player-6'),
    dcc.Input(id='input-player-7', type='text', placeholder='Doubles 2'),
    html.Div(id='output-player-7'),
])

available_players = html.Div([
    html.H2('Below is the list of registered players who could play on this team'),
    dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in registered_players_df.columns],
            data=registered_players_df.to_dict('records'),
            style_table={'maxHeight': '300px', 'maxWidth': '200px', 'overflowY': 'auto'},  # Limit height and enable scrolling
            fixed_rows={'headers': True, 'data': 0}  # Fix header row
        )
])

RegPrevWeekTable = html.Div(
    [
    html.H2('Here is a table showing the registered team, and who played on this team in previous weeks'),
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

left_right_sections_for_middle = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(player_selection, width=6),
                dbc.Col(available_players, width=6)
            ]
        )
    ]
)


top_section = html.Div(
    [
    html.H2('Web App to Check if League Team meets DLTC Eligibility Rules'),
    left_right_sections_for_top,
    left_right_sections_for_middle,
    RegPrevWeekTable
    ]
)


content = html.Div(
    [
    top_section,
    ]
)
app.layout = content

########################### Define all my callbacks #####################################################################
"""
# auto suggestion for many text boxes, but it doesnt work for me
@app.callback(
    Output({'type': 'output-player', 'index': MATCH}, 'children'),
    [Input({'type': 'input-player', 'index': MATCH}, 'value')]
)
def update_output(value):
    if value is not None and value != '':
        matched_players = [player for player in registered_players_list if player.lower().startswith(value.lower())]
        suggestions = html.Ul([html.Li(player) for player in matched_players])
        return suggestions
    else:
        return ''
"""


# auto suggestion for a single text box
@app.callback(
    Output('output-player-1', 'children'),
    [Input('input-player-1', 'value')]
)
def update_suggested_player_1(value):
    return update_suggested_player(value, registered_players_list)


@app.callback(
    Output('output-player-2', 'children'),
    [Input('input-player-2', 'value')]
)
def update_suggested_player_2(value):
    return update_suggested_player(value, registered_players_list)


@app.callback(
    Output('output-player-3', 'children'),
    [Input('input-player-3', 'value')]
)
def update_suggested_player_3(value):
    return update_suggested_player(value, registered_players_list)


@app.callback(
    Output('output-player-4', 'children'),
    [Input('input-player-4', 'value')]
)
def update_suggested_player_4(value):
    return update_suggested_player(value, registered_players_list)


@app.callback(
    Output('output-player-5', 'children'),
    [Input('input-player-5', 'value')]
)
def update_suggested_player_5(value):
    return update_suggested_player(value, registered_players_list)


@app.callback(
    Output('output-player-6', 'children'),
    [Input('input-player-6', 'value')]
)
def update_suggested_player_6(value):
    return update_suggested_player(value, registered_players_list)


@app.callback(
    Output('output-player-7', 'children'),
    [Input('input-player-7', 'value')]
)
def update_suggested_player_7(value):
    return update_suggested_player(value, registered_players_list)


if __name__ == '__main__':
    app.run_server(debug=True)  # Set debug to true makes webapp automatically update, when user clicks refresh
    #app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
