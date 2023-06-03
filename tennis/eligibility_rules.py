def has_7_unique_reg_players(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that there are 7 unique players on the team that are in the subs and lower team list
    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name and Lowest_Class, for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks:
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    required_players = ['S1', 'S2', 'S3', 'D1', 'D1B', 'D2', 'D2B']
    team = set()
    for position in required_players:
        if position not in proposed_team.keys():
            return False, f'no player was entered in position {position}'
        if proposed_team[position] in team:
            return False, f'you entered {proposed_team[position]} twice'
        if proposed_team[position] not in team_subs_and_lower_teams['Name'].values:
            return False, f'{proposed_team[position]} is not in the list of valid subs or registered teams at or below this class level'
        team.add(proposed_team[position])
    return True, None


def team_played_before(proposed_team, registered_team, team_subs_and_lower_teams, relevant_team_previous_weeks):
    """
    Checks that this exact group of 7 players hasnt played before, and if so that they play in the exact same prior order
    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name and Lowest_Class, for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param relevant_team_previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """

    set_registered_team = set(registered_team['Name'].values)
    set_proposed_team = set(proposed_team.values())

    if set_registered_team == set_proposed_team:
        for position in ['S1', 'S2', 'S3', 'D1', 'D1B', 'D2', 'D2B']:
            proposed_player = proposed_team[position]
            proposed_players_reg_position = registered_team[registered_team['Name']==proposed_player]['Position'].iloc(0)[0]
            if position[0:2] != proposed_players_reg_position[0:2]: # note use of [0:2] at end to swap position D1B to D1
                return False, f"you are using the same 7 players as your registered team but {proposed_player} is not playing in the registered position of {proposed_players_reg_position[0:2]}"

    for i in range(5):
        week = 'Week'+str(i+1)
        set_players_week_i = set(relevant_team_previous_weeks[week].values)
        if set_players_week_i == set_proposed_team:
            prev_team = relevant_team_previous_weeks[['Position', week]]
            for position in ['S1', 'S2', 'S3', 'D1', 'D1B', 'D2', 'D2B']:
                proposed_player = proposed_team[position]
                proposed_players_old_position = prev_team[prev_team[week] == proposed_player]['Position'].iloc(0)[0]
                if position[0:2] != proposed_players_old_position[0:2]:  # note use of [0:2] at end to swap position D1B to D1
                    return False, f"you are using the same 7 players as week {i+1} team but {proposed_player} is not playing in the old position of {proposed_players_old_position[0:2]}"

    return True, None