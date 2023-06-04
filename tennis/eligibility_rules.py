def has_7_unique_reg_players(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that there are 7 unique players on the team that are in the subs and lower team list
    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Lowest_Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
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


def team_played_before(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that this exact group of 7 players hasnt played before, and if so that they play in the exact same prior order
    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Lowest_Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """

    set_registered_team = set(registered_team['Name'].values)
    set_proposed_team = set(proposed_team.values())
    team_number = registered_team['Class'].iloc(0)[0]
    relevant_team_previous_weeks = previous_weeks[previous_weeks['Team'] == team_number]

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


def singles_right_order(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that no singles player is playing above someone who played above them before
    Checks that no singles player is playing above someone of a better class
    Checks that no singles player is playing above someone from a better team

    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Lowest_Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    for single_pos in ['S1', 'S2']:  # dont need to check S3
        player = proposed_team[single_pos]

        # build set of players who have ever played higher singles in past
        set_players_above = set()
        for i in range(5):
            week = 'Week'+str(i+1)
            that_week = previous_weeks[['Team', 'Position', week]]
            player_played_previous = that_week[that_week[week]==player][['Team', 'Position']].values
            for old_team, old_pos in player_played_previous:
                if old_pos in ['S2', 'S3']:
                    s1_player = that_week[(that_week['Team']==old_team) & (that_week['Position']=='S1')][week].iloc(0)[0]
                    set_players_above.add(s1_player)
                if old_pos == 'S3':
                    s2_player = that_week[(that_week['Team']==old_team) & (that_week['Position']=='S2')][week].iloc(0)[0]
                    set_players_above.add(s2_player)

        # check if the lower singles have ever played above higher singles
        if single_pos == 'S1':
            if proposed_team['S2'] in set_players_above:
                return False, f'You are playing {player} ahead of {proposed_team["S2"]} but that violates a previous weeks order'
        if proposed_team['S3'] in set_players_above:
            return False, f'You are playing {player} ahead of {proposed_team["S3"]} but that violates a previous weeks order'

        # check if the lower singles players are of a higher (better) class
        player_class = team_subs_and_lower_teams[team_subs_and_lower_teams['Name']==player]['Lowest_Class'].iloc(0)[0]
        if single_pos == 'S1':
            s2_class = team_subs_and_lower_teams[team_subs_and_lower_teams['Name']==proposed_team['S2']]['Lowest_Class'].iloc(0)[0]
            if player_class > s2_class:
                return False, f'You are playing {player} (class {player_class}) ahead of {proposed_team["S2"]} (class {s2_class})'
        s3_class = team_subs_and_lower_teams[team_subs_and_lower_teams['Name']==proposed_team['S3']]['Lowest_Class'].iloc(0)[0]
        if player_class > s3_class:
            return False, f'You are playing {player} (class {player_class}) ahead of {proposed_team["S3"]} (class {s3_class})'

        # check if the lower singles players are from a higher (better) registered team
        player_team = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == player]['Team'].iloc(0)[0]
        if player_team != 'Sub':  # subs of the same class can go above
            if single_pos == 'S1':
                s2_team = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['S2']]['Team'].iloc(0)[0]
                if s2_team != 'Sub':
                    if player_team > s2_team:
                        return False, f'You are playing {player} (team {player_team}) ahead of {proposed_team["S2"]} (team {s2_team})'
            s3_team = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['S3']]['Team'].iloc(0)[0]
            if s3_team != 'Sub':
                if player_team > s3_team:
                    return False, f'You are playing {player} (team {player_team}) ahead of {proposed_team["S3"]} (team {s3_team})'

    return True, None



def doubles_right_order(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that no doubles pairing is playing above a different pairing that played above them before

    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Lowest_Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    pass


def team_tied(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that nobody is team tied and if so, it does something...

    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Lowest_Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    pass