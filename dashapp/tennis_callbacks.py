from dash import html


def update_suggested_player(value, registered_players_list, n_clicks=0):
    if n_clicks is None or n_clicks % 2 == 0:
        if value is not None and value != '':
            matched_players = [player for player in registered_players_list if player.lower().startswith(value.lower())]
            suggestions = html.Ul([html.Li(player) for player in matched_players])
            return suggestions
        else:
            return ''
    else:
        # Disable autoprompts
        return ''

