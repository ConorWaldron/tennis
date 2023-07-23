import dash
from dash import Dash, dcc, html, dash_table, dependencies, Input, Output, State, MATCH
from dash.dependencies import ALL


def update_suggested_player(value, registered_players_list):
    if value is not None and value != '':
        matched_players = [player for player in registered_players_list if player.lower().startswith(value.lower())]
        suggestions = html.Ul([html.Li(player) for player in matched_players])
        return suggestions
    else:
        return ''
