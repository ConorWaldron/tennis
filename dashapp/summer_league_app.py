from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
from leagues import summer_league_eligibility
from tennis_callbacks import update_suggested_player
import os
import io
import base64

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])  # you can pick from the different standard themes at https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/

server = app.server      # exposes server of dash app as an objective that gunicorn can pick
app.title = 'Summer League Eligibility Checker'  # set the title to appear in the tab


########################### Define all my data objects #####################################################################

reg_team = pd.read_csv('../assets/summer_league/teams.csv')
reg_team_relevant = reg_team[['Team', 'Position', 'Name']]
reg_team_relevant = reg_team_relevant.rename(columns={'Name': 'Registered'})

reg_subs = pd.read_csv('../assets/summer_league/subs.csv')

prev_weeks = pd.read_csv('../assets/summer_league/previous_weeks.csv')
reg_team_prev_weeks = pd.merge(reg_team_relevant, prev_weeks, on=['Team', 'Position'])

registered_players_df = pd.concat([reg_team[['Name', 'Class']], reg_subs[['Name', 'Class']]])
registered_players_list = registered_players_df['Name'].tolist()

########################### Define all my Styles #####################################################################


HEADING_STYLE = {
    "background-color": "#000080",  # Navy
    'text-align': 'center',
    'color': '#ffffff',  # white
}

SUB_HEADING_STYLE = {
    'text-align': 'center',
    'color': "#000080",  # Navy
}

CONTENT_STYLE = {
    "background-color": "#e0ffff",  # LIGHT CYAN
    "border-radius": "10px",  # Add border radius (adjust the value as needed)
    "border": "2px solid "#000080"",  # Border style and color (e.g., NAVY)

}


########################### Define all my content #####################################################################

gender_dropdown = html.Div([
    html.H4("Gender Selection"),
    dcc.Dropdown(
        id='gender-dropdown',
        options=[{'label': gender, 'value': gender} for gender in ['Male', 'Female']],
        value='Male',  # Set the default value to be None
        placeholder="Please select gender"  # Set the placeholder text
    ),
    html.Div(id='selected-gender-output')
])

# ToDo this is fixed to the number of teams in the template file, update this so the number changes with the new files uploaded
team_dropdown = html.Div([
    html.H4("Team Selection"),
    dcc.Dropdown(
        id='team_dropdown',
        options=[{'label': str(team), 'value': team} for team in reg_team['Team'].unique()],
        value=1  # Set the default value to the first team number
    ),
    html.Div(id='selected-team-output')
])


left_right_sections_team_gender = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(team_dropdown, width=5),
                dbc.Col(gender_dropdown, width=7)
            ]
        )
    ]
)

team_file = html.Div([
            html.H6('teams.xlsx', style={'textAlign': 'center'}),
            html.Button(id='DownLoadTeamsTemplateButton', n_clicks=0, children='Download template',
                        style={'width': '150px', 'height': '40px', 'font-size': '12px', 'margin-right': '10px', 'display': 'inline-block'}),
            dcc.Upload(id='uploadteam', children=html.Button('Upload file', style={'width': '150px', 'height': '40px', 'font-size': '12px', 'display': 'inline-block'}), multiple=False),
            html.Div(id='team_upload_error')
        ]),

sub_file = html.Div([
            html.H6('subs.xlsx', style={'textAlign': 'center'}),
            html.Button(id='DownLoadSubsTemplateButton', n_clicks=0, children='Download template',
                        style={'width': '150px', 'height': '40px', 'font-size': '12px', 'margin-right': '10px'}),
            dcc.Upload(id='uploadsub', children=html.Button('Upload file', style={'width': '150px', 'height': '40px', 'font-size': '12px', 'display': 'inline-block'}), multiple=False),
            html.Div(id='sub_upload_error')
        ]),

previous_week_file = html.Div([
            html.H6('previous_weeks.xlsx', style={'textAlign': 'center'}),
            html.Button(id='DownLoadPreviousWeeksTemplateButton', n_clicks=0, children='Download template',
                        style={'width': '150px', 'height': '40px', 'font-size': '10px', 'margin-right': '10px'}),
            dcc.Upload(id='uploadprevious', children=html.Button('Upload file', style={'width': '150px', 'height': '40px', 'font-size': '12px', 'display': 'inline-block'}), multiple=False),
            html.Div(id='prev_week_upload_error')
        ]),

columns_for_upload = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(team_file, width=4),
                dbc.Col(sub_file, width=4),
                dbc.Col(previous_week_file, width=4)
            ]
        )
    ]
)

drop_down_menus = html.Div(
    [
        left_right_sections_team_gender,
        html.Br(),
        html.H4('Upload your own team information'),
        html.P('This website comes with team information that is pre-loaded by the website maintainer but if you want to upload team information for another club you can do this here by downloading the three template files, modifying them with your team information and uploading them to the website in the sections below.'),
        columns_for_upload,
        dcc.Download(id="downloadteam"),  # non visible componet for download return
        dcc.Download(id="downloadsub"),  # non visible componet for download return
        dcc.Download(id="downloadprevious"),  # non visible componet for download return
    ]
)

carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": "https://i.postimg.cc/mkcB9NqQ/donnybrook-ladies.jpg"},
        {"key": "2", "src": "https://i.postimg.cc/7P9161M5/donnybrook-bbq.jpg"},
        {"key": "3", "src": "https://i.postimg.cc/43fm7f7v/donnybrook-college-clash.jpg"},
        {"key": "4", "src": "https://i.postimg.cc/t4FPPhGQ/donnybrook-mens.jpg"},
    ],
    controls=True,
    indicators=False,
    interval=10000,
    ride="carousel",
    className="custom-carousel"  # Add a custom class name to apply CSS styles
)


# you can provide images from local files or url to the internet
instruct_tab = dbc.Card(
        html.Div(
            [
            html.Div(carousel, style={"height": "240px", "overflow": "hidden", "objectPosition": 'center'}),
            #dbc.CardImg(src="https://i.postimg.cc/mkcB9NqQ/donnybrook-ladies.jpg", top=True, style={'height':'65%', 'width':'65%'}),
            #dbc.CardImg(src="https://i.postimg.cc/7P9161M5/donnybrook-bbq.jpg", top=True, style={'height':'65%', 'width':'65%'}),
            #dbc.CardImg(src="https://i.postimg.cc/43fm7f7v/donnybrook-college-clash.jpg", top=True, style={'height':'65%', 'width':'65%'}),
            #dbc.CardImg(src="https://i.postimg.cc/t4FPPhGQ/donnybrook-mens.jpg", top=True, style={'height':'65%', 'width':'65%'}),
            dbc.CardBody(html.P("Interested in learning more about Donnybrook tennis, see https://www.donnybrookltc.ie/", className="card-text")),
            ],
            style={'textAlign': 'center'},
        )
)


player_selection = html.Div([
    html.Div(dbc.Button("Disable autoprompts", id="autoprompts-button", color="primary", className="me-1")),
    dcc.Input(id='input_player_1', type='text', placeholder='Singles 1'),
    html.Div(id='autoprompt-output-player-1'),
    dcc.Input(id='input_player_2', type='text', placeholder='Singles 2'),
    html.Div(id='autoprompt-output-player-2'),
    dcc.Input(id='input_player_3', type='text', placeholder='Singles 3'),
    html.Div(id='autoprompt-output-player-3'),
    dcc.Input(id='input_player_4', type='text', placeholder='Doubles 1'),
    html.Div(id='autoprompt-output-player-4'),
    dcc.Input(id='input_player_5', type='text', placeholder='Doubles 1'),
    html.Div(id='autoprompt-output-player-5'),
    dcc.Input(id='input_player_6', type='text', placeholder='Doubles 2'),
    html.Div(id='autoprompt-output-player-6'),
    dcc.Input(id='input_player_7', type='text', placeholder='Doubles 2'),
    html.Div(id='autoprompt-output-player-7'),
])

check_eligibility_area = html.Div([
    html.Div(dbc.Button("Check Team Eligibility", id="eligibility-button", n_clicks=0, color="primary", className="me-1")),
    html.Div([
        dbc.Button("Eligible", id="button-true", color="secondary",),
        dbc.Button("Ineligible", id="button-false", color="secondary",),
    ]),
    html.Div(id='eligibility-output'),
])

left_right_sections_for_team_selection_area = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(player_selection, width=5),
                dbc.Col(check_eligibility_area, width=7)
            ]
        )
    ]
)

team_selection_area = html.Div([
    html.H2('Select Your Team Here', style=SUB_HEADING_STYLE),
    html.H6("The text boxes will display all the registered players in the system which match the spelling of what you have typed so far. You still need to write the player's complete name, warning it is case sensitive"),
    left_right_sections_for_team_selection_area,
], style=CONTENT_STYLE)


available_players = html.Div([
    html.H2('Below is the list of players registered at or below this team', style=SUB_HEADING_STYLE),
    html.Div([
        dash_table.DataTable(
            id='available_player_table',
            columns=[{'name': col, 'id': col} for col in registered_players_df.columns],
            data=registered_players_df.to_dict('records'),
            style_table={'maxHeight': '300px', 'maxWidth': '300px', 'overflowY': 'auto'},  # Limit height and enable scrolling
            fixed_rows={'headers': True, 'data': 0},  # Fix header row
            style_cell={'textAlign': 'left'},  # Left-align text in all cells
            style_cell_conditional=[
                        {'if': {'column_id': 'Name'}, 'minWidth': '100px', 'maxWidth': '150px'},
                        {'if': {'column_id': 'Class'}, 'minWidth': '50px', 'maxWidth': '100px'},
                    ]
            )
        ], style={'margin-left': '50px'}
    )
], style=CONTENT_STYLE)

RegPrevWeekTable = html.Div(
    [
    html.H2('Here is a table showing the registered team, and who played on this team in previous weeks', style=SUB_HEADING_STYLE),
    html.Div([
        dash_table.DataTable(
            id='RegPrevWeekTable',
            columns=[{"name": i, "id": i} for i in reg_team_prev_weeks.columns],
            data=reg_team_prev_weeks.to_dict('records'),
            style_table={'maxWidth': '1300px', 'overflowY': 'auto'},  # Limit height and enable scrolling
            style_cell={'textAlign': 'left'},  # Left-align text in all cells
            style_cell_conditional=[
                            {'if': {'column_id': 'Team'}, 'minWidth': '50px', 'maxWidth': '50px'},
                            {'if': {'column_id': 'Position'}, 'minWidth': '50px', 'maxWidth': '50px'},
                            {'if': {'column_id': 'Registered'}, 'minWidth': '100px', 'maxWidth': '100px'},
                            {'if': {'column_id': 'Week1'}, 'minWidth': '100px', 'maxWidth': '100px'},
                            {'if': {'column_id': 'Week2'}, 'minWidth': '100px', 'maxWidth': '100px'},
                            {'if': {'column_id': 'Week3'}, 'minWidth': '100px', 'maxWidth': '100px'},
                            {'if': {'column_id': 'Week4'}, 'minWidth': '100px', 'maxWidth': '100px'},
                            {'if': {'column_id': 'Week5'}, 'minWidth': '100px', 'maxWidth': '100px'},
                        ]
            )
        ], style={'margin-left': '100px'}
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
                dbc.Col(team_selection_area, width=6),
                dbc.Col(available_players, width=6)
            ]
        )
    ]
)

full_section = html.Div(
    [
    html.H2('Web App to Check if Summer League Team meets DLTC Eligibility Rules',  style=HEADING_STYLE),
    html.Br(),
    left_right_sections_for_top,
    html.Br(),
    left_right_sections_for_middle,
    html.Br(),
    RegPrevWeekTable
    ]
)


content = html.Div(
    [
    dcc.Store(id='team-store', storage_type='session'),  # Store the team dataframe in the session
    dcc.Store(id='sub-store', storage_type='session'),  # Store the sub dataframe in the session
    dcc.Store(id='previous-week-store', storage_type='session'),  # Store the previous week dataframe in the session
    full_section,
    ]
)
app.layout = content

########################### Define all my callbacks ####################################################################

# We use a session variable to update the teams, subs and previous week df if a user uploads one


@app.callback(
    Output('team-store', 'data'),
    Output('team_upload_error', 'children'),
    Input('uploadteam', 'contents'),
    prevent_initial_call=True
)
def update_team_file(contents):
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Assuming the uploaded file is a CSV file
    df = pd.read_excel(io.BytesIO(decoded))

    # Check for expected column names
    expected_columns = ['Name', 'Team', 'Class', 'Position']
    if not set(expected_columns).issubset(df.columns):
        warning_message = f"Warning: The uploaded Excel file did not contain the required columns {', '.join(expected_columns)}. Upload rejected, still using old values"
        old_df = pd.read_csv('../assets/summer_league/teams_template.csv')
        return old_df.to_dict('records'), warning_message

    return df.to_dict('records'), ''


@app.callback(
    Output('sub-store', 'data'),
    Output('sub_upload_error', 'children'),
    Input('uploadsub', 'contents'),
    prevent_initial_call=True
)
def update_sub_file(contents):
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Assuming the uploaded file is a CSV file
    df = pd.read_excel(io.BytesIO(decoded))

    # Check for expected column names
    expected_columns = ['Name', 'Class']
    if not set(expected_columns).issubset(df.columns):
        warning_message = f"Warning: The uploaded Excel file did not contain the required columns {', '.join(expected_columns)}. Upload rejected, still using old values"
        old_df = pd.read_csv('../assets/summer_league/subs_template.csv')
        return old_df.to_dict('records'), warning_message

    return df.to_dict('records'), ''


@app.callback(
    Output('previous-week-store', 'data'),
    Output('prev_week_upload_error', 'children'),
    Input('uploadprevious', 'contents'),
    prevent_initial_call=True
)
def update_prev_week_file(contents):
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Assuming the uploaded file is a CSV file
    df = pd.read_excel(io.BytesIO(decoded))

    # Check for expected column names
    expected_columns = ['Team', 'Position', 'Week1', 'Week2', 'Week3', 'Week4', 'Week5']
    if not set(expected_columns).issubset(df.columns):
        warning_message = f"Warning: The uploaded Excel file did not contain the required columns {', '.join(expected_columns)}. Upload rejected, still using old values"
        old_df = pd.read_csv('../assets/summer_league/previous_weeks_template.csv')
        return old_df.to_dict('records'), warning_message

    return df.to_dict('records'), ''




"""
@app.callback(
    Output('selected-gender-output', 'children'),
    [Input('gender-dropdown', 'value')]
)
def update_gender_output(selected_gender):
    if selected_gender is not None:
        return f"You have selected gender: {selected_gender}"
    else:
        return "Please select gender"
"""


@app.callback(
    Output('selected-team-output', 'children'),
    [Input('team_dropdown', 'value')]
)
def update_team_output(selected_team):
    return f"You have chosen team {selected_team}"


@app.callback(
    Output(component_id="downloadteam", component_property="data"),
    Input(component_id="DownLoadTeamsTemplateButton", component_property="n_clicks"),
)
def download_team_template(nclickslocal):
    if nclickslocal == 0:
        raise PreventUpdate
    else:
        teams_template_df = pd.read_csv('../assets/summer_league/teams_template.csv')
        return dcc.send_data_frame(teams_template_df.to_excel, "TeamsTemplate.xlsx")


@app.callback(
    Output(component_id="downloadsub", component_property="data"),
    Input(component_id="DownLoadSubsTemplateButton", component_property="n_clicks"),
)
def download_sub_template(nclickslocal):
    if nclickslocal == 0:
        raise PreventUpdate
    else:
        subs_template_df = pd.read_csv('../assets/summer_league/subs_template.csv')
        return dcc.send_data_frame(subs_template_df.to_excel, "SubsTemplate.xlsx")


@app.callback(
    Output(component_id="downloadprevious", component_property="data"),
    Input(component_id="DownLoadPreviousWeeksTemplateButton", component_property="n_clicks"),
)
def download_previous_week_template(nclickslocal):
    if nclickslocal == 0:
        raise PreventUpdate
    else:
        previous_weeks_template_df = pd.read_csv('../assets/summer_league/previous_weeks_template.csv')
        return dcc.send_data_frame(previous_weeks_template_df.to_excel, "PreviousWeeksTemplate.xlsx")


# going to reuse this callback function 3 times
def upload_file(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # You can save the uploaded file to a specific location or process it as needed
        # For example, you can read it into a pandas DataFrame
        df = pd.read_excel(io.BytesIO(decoded))

        # You can perform further processing on the DataFrame or display it in your app
        return html.Div([
            html.H5('Uploaded Excel Data'),
            dash_table.DataTable(data=df.to_dict('records'), columns=[{'name': col, 'id': col} for col in df.columns])
        ])

"""
We no longer want to display the output of the upload files to the web app

@app.callback(
    Output('output-team-upload', 'children'), #turning off output as we dont want to display it
    Input('uploadteam', 'contents'),
    prevent_initial_call=True
)
def upload_team_file(contents):
    return upload_file(contents)


@app.callback(
    Output('output-sub-upload', 'children'), #turning off output as we dont want to display it
    Input('uploadsub', 'contents'),
    prevent_initial_call=True
)
def upload_sub_file(contents):
    return upload_file(contents)


@app.callback(
    Output('output-previous-upload', 'children'), #turning off output as we dont want to display it
    Input('uploadprevious', 'contents'),
    prevent_initial_call=True
)
def upload_team_file(contents):
    return upload_file(contents)
"""


@app.callback(
    Output("autoprompts-button", "color"),
    Input("autoprompts-button", "n_clicks"),
)
def toggle_autoprompts(n_clicks):
    if n_clicks is None:
        n_clicks = 0

    # Toggle between primary color (on) and secondary color (off)
    if n_clicks % 2 == 1:
        new_color = "secondary"
    else:
        new_color = "primary"

    return new_color

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
    Output('autoprompt-output-player-1', 'children'),
    Input('input_player_1', 'value'),
    Input("autoprompts-button", "n_clicks"),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
)
def update_suggested_player_1(value, n_clicks, team_data, sub_data):
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    available_df = pd.concat([team_df[['Name', 'Class']], sub_df[['Name', 'Class']]])
    available_players_list = available_df['Name'].tolist()
    return update_suggested_player(value, available_players_list, n_clicks)


@app.callback(
    Output('autoprompt-output-player-2', 'children'),
    Input('input_player_2', 'value'),
    Input("autoprompts-button", "n_clicks"),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
)
def update_suggested_player_2(value, n_clicks, team_data, sub_data):
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    available_df = pd.concat([team_df[['Name', 'Class']], sub_df[['Name', 'Class']]])
    available_players_list = available_df['Name'].tolist()
    return update_suggested_player(value, available_players_list, n_clicks)


@app.callback(
    Output('autoprompt-output-player-3', 'children'),
    Input('input_player_3', 'value'),
    Input("autoprompts-button", "n_clicks"),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
)
def update_suggested_player_3(value, n_clicks, team_data, sub_data):
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    available_df = pd.concat([team_df[['Name', 'Class']], sub_df[['Name', 'Class']]])
    available_players_list = available_df['Name'].tolist()
    return update_suggested_player(value, available_players_list, n_clicks)


@app.callback(
    Output('autoprompt-output-player-4', 'children'),
    Input('input_player_4', 'value'),
    Input("autoprompts-button", "n_clicks"),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
)
def update_suggested_player_4(value, n_clicks, team_data, sub_data):
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    available_df = pd.concat([team_df[['Name', 'Class']], sub_df[['Name', 'Class']]])
    available_players_list = available_df['Name'].tolist()
    return update_suggested_player(value, available_players_list, n_clicks)


@app.callback(
    Output('autoprompt-output-player-5', 'children'),
    Input('input_player_5', 'value'),
    Input("autoprompts-button", "n_clicks"),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
)
def update_suggested_player_5(value, n_clicks, team_data, sub_data):
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    available_df = pd.concat([team_df[['Name', 'Class']], sub_df[['Name', 'Class']]])
    available_players_list = available_df['Name'].tolist()
    return update_suggested_player(value, available_players_list, n_clicks)


@app.callback(
    Output('autoprompt-output-player-6', 'children'),
    Input('input_player_6', 'value'),
    Input("autoprompts-button", "n_clicks"),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
)
def update_suggested_player_6(value, n_clicks, team_data, sub_data):
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    available_df = pd.concat([team_df[['Name', 'Class']], sub_df[['Name', 'Class']]])
    available_players_list = available_df['Name'].tolist()
    return update_suggested_player(value, available_players_list, n_clicks)


@app.callback(
    Output('autoprompt-output-player-7', 'children'),
    Input('input_player_7', 'value'),
    Input("autoprompts-button", "n_clicks"),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
)
def update_suggested_player_7(value, n_clicks, team_data, sub_data):
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    available_df = pd.concat([team_df[['Name', 'Class']], sub_df[['Name', 'Class']]])
    available_players_list = available_df['Name'].tolist()
    return update_suggested_player(value, available_players_list, n_clicks)


@app.callback(
    Output("button-true", "color"),
    Output("button-false", "color"),
    Output("eligibility-output", "children"),
    Input("eligibility-button", "n_clicks"),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
    Input('previous-week-store', 'data'),  # Input the previous week dataframe from the dcc.Store
    State("team_dropdown", "value"),
    State("input_player_1", "value"),
    State("input_player_2", "value"),
    State("input_player_3", "value"),
    State("input_player_4", "value"),
    State("input_player_5", "value"),
    State("input_player_6", "value"),
    State("input_player_7", "value"),
)
def update_eligibility_result_button_state(n_clicks, team_data, sub_data, previous_week_data, team_dropdown,
                                           input_player_1, input_player_2, input_player_3, input_player_4,
                                           input_player_5, input_player_6, input_player_7):
    if n_clicks is None or n_clicks == 0:
        return 'secondary', 'secondary', 'Have not run eligibility checker yet'

    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    prev_week_df = pd.DataFrame(previous_week_data) if previous_week_data else prev_weeks

    my_proposed_team = {
        'S1': input_player_1,
        'S2': input_player_2,
        'S3': input_player_3,
        'D1': input_player_4,
        'D1B': input_player_5,
        'D2': input_player_6,
        'D2B': input_player_7,
    }
    eligible_result, warning = summer_league_eligibility(int(team_dropdown), my_proposed_team,
                                                         team_df, sub_df, prev_week_df)
    if eligible_result:
        return 'primary', 'secondary', warning
    else:
        return 'secondary', 'primary', 'Your team is ineligible, please ensure you correctly spelled all team members full names correctly. Reason: '+warning


@app.callback(
    Output('available_player_table', 'data'),
    Input('team_dropdown', 'value'),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('sub-store', 'data'),  # Input the sub dataframe from the dcc.Store
)
def update_table_registered_player_data(selected_team, team_data, sub_data):
    # Filter the registered_players_df based on the selected_team
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    sub_df = pd.DataFrame(sub_data) if sub_data else reg_subs
    registered_players_df_local = pd.concat([team_df[['Name', 'Class']], sub_df[['Name', 'Class']]])
    filtered_df = registered_players_df_local[registered_players_df_local['Class'] >= selected_team]
    sorted_filtered_df = filtered_df.sort_values(by=['Class', 'Name'])
    # Convert the filtered DataFrame to dict to update DataTable data
    return sorted_filtered_df.to_dict('records')


@app.callback(
    Output('RegPrevWeekTable', 'data'),
    Input('team_dropdown', 'value'),
    Input('team-store', 'data'),  # Input the team dataframe from the dcc.Store
    Input('previous-week-store', 'data'),  # Input the previous week dataframe from the dcc.Store
)
def update_table_previous_week_data(selected_team, team_data, previous_week_data):
    team_df = pd.DataFrame(team_data) if team_data else reg_team
    team_df_relevant = team_df[['Team', 'Position', 'Name']]
    team_df_relevant = team_df_relevant.rename(columns={'Name': 'Registered'})
    prev_week_df = pd.DataFrame(previous_week_data) if previous_week_data else prev_weeks
    reg_team_prev_weeks_local = pd.merge(team_df_relevant, prev_week_df, on=['Team', 'Position'])

    # Filter the registered_players_df based on the selected_team
    filtered_df = reg_team_prev_weeks_local[reg_team_prev_weeks_local['Team'] == selected_team]
    # Convert the filtered DataFrame to dict to update DataTable data
    return filtered_df.to_dict('records')


if __name__ == '__main__':
    #app.run_server(debug=True)  # Set debug to true makes webapp automatically update, when user clicks refresh, runs on a standard port

    # used when you are actually running app with docker as you specify the port here, this must match the port specified in the Dockerfile
    # Note if you are trying to view it from your loacl machine it returns two urls, but only the second one works http://192.168.0.38:5000/
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
