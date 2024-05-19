def has_7_unique_reg_players(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that there are 7 unique players on the team that are in the subs and lower team list
    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
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
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """

    set_registered_team = set(registered_team['Name'].values)
    set_proposed_team = set(proposed_team.values())
    team_number = registered_team['Class'].iloc(0)[0]
    relevant_team_previous_weeks = previous_weeks[previous_weeks['Team'] == team_number]

    if len(set_registered_team) == 7:
        # this must be summer league
        position_list = ['S1', 'S2', 'S3', 'D1', 'D1B', 'D2', 'D2B']
    else:
        # this must be winter league
        position_list = ['D1', 'D1B', 'D2', 'D2B', 'D3', 'D3B']

    if set_registered_team == set_proposed_team:
        for position in position_list:
            proposed_player = proposed_team[position]
            proposed_players_reg_position = registered_team[registered_team['Name']==proposed_player]['Position'].iloc(0)[0]
            if position[0:2] != proposed_players_reg_position[0:2]: # note use of [0:2] at end to swap position D1B to D1
                return False, f"you are using the same players as your registered team but {proposed_player} is not playing in the registered position of {proposed_players_reg_position[0:2]}"

    for i in range(5):
        week = 'Week'+str(i+1)
        set_players_week_i = set(relevant_team_previous_weeks[week].values)
        if set_players_week_i == set_proposed_team:
            prev_team = relevant_team_previous_weeks[['Position', week]]
            for position in position_list:
                proposed_player = proposed_team[position]
                proposed_players_old_position = prev_team[prev_team[week] == proposed_player]['Position'].iloc(0)[0]
                if position[0:2] != proposed_players_old_position[0:2]:  # note use of [0:2] at end to swap position D1B to D1
                    return False, f"you are using the same players as week {i+1} team but {proposed_player} is not playing in the old position of {proposed_players_old_position[0:2]}"

    return True, None


def singles_right_order(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that no singles player is playing above someone who played above them before
    Checks that no singles player is playing above someone of a better class
    Checks that no singles player is playing above someone from a better team

    TODO fix this, Matthew O'Neill Bug
    Checks that no signles player is playing above someone who is registered at a higher singles position

    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    # used to get position in proposed team from the player name
    def get_key_from_value(d, value):
        return next((key for key, val in d.items() if val == value), None)

    registered_singles_1 = registered_team[registered_team['Position'] == 'S1']['Name'].iloc(0)[0]
    registered_singles_2 = registered_team[registered_team['Position'] == 'S2']['Name'].iloc(0)[0]
    registered_singles_3 = registered_team[registered_team['Position'] == 'S3']['Name'].iloc(0)[0]
    registered_singles_players = set([registered_singles_1, registered_singles_2, registered_singles_3])

    proposed_singles_1 = proposed_team['S1']
    proposed_singles_2 = proposed_team['S2']
    proposed_singles_3 = proposed_team['S3']
    proposed_singles_players = set([proposed_singles_1, proposed_singles_2, proposed_singles_3])

    # we only need to check the singles registration order if 2 or more of the proposed players are registered singles players
    set_registered_s_playing_s = registered_singles_players & proposed_singles_players

    if len(set_registered_s_playing_s) >= 2:
        # check that the registered order is being respected
        for player in set_registered_s_playing_s:
            proposed_position = int(get_key_from_value(proposed_team, player)[1])
            registered_position = int(registered_team[registered_team['Name']==player]['Position'].iloc(0)[0][1])

            # the other registered players are...
            for other_player in set_registered_s_playing_s:
                if player != other_player:
                    other_player_proposed_position = int(get_key_from_value(proposed_team, other_player)[1])
                    other_player_registered_position = int(registered_team[registered_team['Name'] == other_player]['Position'].iloc(0)[0][1])

                    if registered_position < other_player_registered_position:
                        # you are registered at a better level than this player, you have to play higher than them
                        if proposed_position > other_player_proposed_position:
                            return False, f'You are playing {other_player} ahead of {player} but {player} was registered ahead at singles {registered_position}, while {other_player} was registered at singles {other_player_registered_position}'

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
        player_class = team_subs_and_lower_teams[team_subs_and_lower_teams['Name']==player]['Class'].iloc(0)[0]
        if single_pos == 'S1':
            s2_class = team_subs_and_lower_teams[team_subs_and_lower_teams['Name']==proposed_team['S2']]['Class'].iloc(0)[0]
            if player_class > s2_class:
                return False, f'You are playing {player} (class {player_class}) ahead of {proposed_team["S2"]} (class {s2_class})'
        s3_class = team_subs_and_lower_teams[team_subs_and_lower_teams['Name']==proposed_team['S3']]['Class'].iloc(0)[0]
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


def summer_lg_doubles_team_and_class_checker(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that no doubles player is playing above someone of a better class
    Checks that no doubles player is playing above someone from a better team

    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    class_D1 = team_subs_and_lower_teams[team_subs_and_lower_teams['Name']==proposed_team['D1']]['Class'].iloc(0)[0]
    team_D1 = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['D1']]['Team'].iloc(0)[0]
    class_D1B = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['D1B']]['Class'].iloc(0)[0]
    team_D1B = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['D1B']]['Team'].iloc(0)[0]
    class_D2 = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['D2']]['Class'].iloc(0)[0]
    team_D2 = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['D2']]['Team'].iloc(0)[0]
    class_D2B = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['D2B']]['Class'].iloc(0)[0]
    team_D2B = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team['D2B']]['Team'].iloc(0)[0]

    # Checks that no doubles player is playing above someone of a better class
    weakest_class_d1_pair = max(class_D1, class_D1B)
    strongest_class_d2_pair = min(class_D2, class_D2B)
    if weakest_class_d1_pair > strongest_class_d2_pair:
        return False, f'Your 2nd doubles contains a class {strongest_class_d2_pair} player which is better than one of the players on your first doubles (class {weakest_class_d1_pair})'

    # Checks that no doubles player is playing above someone from a better team
    if (team_D1 != 'Sub') | (team_D1B != 'Sub'): # one of your D1 pair, is registered for a team instead of being a sub
        # find the max (worst) registered team in the D1 pair
        if (team_D1 != 'Sub') & (team_D1B != 'Sub'):
            max_D1_reg_team = max(team_D1, team_D1B)
        elif (team_D1 != 'Sub') & (team_D1B == 'Sub'):
            max_D1_reg_team = team_D1
        else:
            max_D1_reg_team = team_D1B

        # find the min (best) registered team in the D2 pair
        if (team_D2 != 'Sub') & (team_D2B != 'Sub'):
            min_D2_reg_team = min(team_D2, team_D2B)
        elif (team_D2 != 'Sub') & (team_D2B == 'Sub'):
            min_D2_reg_team = team_D2
        elif (team_D2 == 'Sub') & (team_D2B != 'Sub'):
            min_D2_reg_team = team_D2B
        else: # they are both subs
            min_D2_reg_team = 1000  # assign to a fictionally high team

        if min_D2_reg_team < max_D1_reg_team:
            return False, f'Your 2nd doubles contains a player registered to team {min_D2_reg_team} which is better than one of the players on your first doubles (registered to team {max_D1_reg_team})'

    return True, None


def summer_lg_doubles_right_order(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that no doubles pairing is playing above a different pairing that played above them before

    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    registered_4_doubles_players = set()
    proposed_4_doubles_players = set()
    for pos in ['D1', 'D1B', 'D2', 'D2B']:
        registered_4_doubles_players.add(registered_team[registered_team['Position']==pos]['Name'].iloc(0)[0])
        proposed_4_doubles_players.add(proposed_team[pos])
    if registered_4_doubles_players == proposed_4_doubles_players:
        # you must play D1 above D2
        first_doubles_reg_pair = set()
        first_doubles_reg_pair.add(registered_team[registered_team['Position'] == 'D1']['Name'].iloc(0)[0])
        first_doubles_reg_pair.add(registered_team[registered_team['Position'] == 'D1B']['Name'].iloc(0)[0])

        first_doubles_pair = set()
        first_doubles_pair.add(proposed_team['D1'])
        first_doubles_pair.add(proposed_team['D1B'])

        if first_doubles_reg_pair != first_doubles_pair:
            return False, 'all 4 registered players are playing doubles, but not in the right order'

    # Find any matches they have played TOGETHER previously, then build set_partnerships_above
    list_partnerships_above = [] # using list instead of set as you cant have nested sets in python due to hashable objects...
    for i in range(5):
        week = 'Week' + str(i + 1)
        that_week = previous_weeks[['Team', 'Position', week]]
        player1_played_previous = that_week[that_week[week] == proposed_team['D1']][['Team', 'Position']].values
        player2_played_previous = that_week[that_week[week] == proposed_team['D1B']][['Team', 'Position']].values
        # Check did they play on the same team, warning either player could have played twice or more times in same week
        for player_1_old_team, player_1_old_pos in player1_played_previous:
            for player_2_old_team, player_2_old_pos in player2_played_previous:
                if player_1_old_team == player_2_old_team:
                    set_old_pos = set()
                    set_old_pos.add(player_1_old_pos)
                    set_old_pos.add(player_2_old_pos)
                    if set_old_pos == {'D2', 'D2B'}: # we only care if they played D2 as we are looking for list of players who played above
                        higher_pairing = set()
                        D1_player = that_week[(that_week['Team'] == player_1_old_team) & (that_week['Position'] == 'D1')][week].iloc(0)[0]
                        higher_pairing.add(D1_player)
                        D1B_player = that_week[(that_week['Team'] == player_1_old_team) & (that_week['Position'] == 'D1B')][week].iloc(0)[0]
                        higher_pairing.add(D1B_player)
                        list_partnerships_above.append(higher_pairing)

    # check if the 2nd doubles pairing is in the list of doubles pairs who have ever played above
    second_doubles_pair = set()
    second_doubles_pair.add(proposed_team['D2'])
    second_doubles_pair.add(proposed_team['D2B'])
    if second_doubles_pair in list_partnerships_above:
        return False, 'Your 2nd doubles pairing have played above your first doubles pairing in a previous week'

    return True, None


def team_tied(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that nobody is team tied and if so, it does something...

    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    for player in proposed_team.values():
        teams_played_for = []
        for i in range(5):
            week = 'Week' + str(i + 1)
            that_week = previous_weeks[['Team', 'Position', week]]
            player1_played_previous = that_week[that_week[week] == player][['Team']].values
            for match in player1_played_previous:
                teams_played_for.append(match[0])

        # Check if they have played for a higher team more than once
        current_team = registered_team['Team'].iloc(0)[0]
        higher_teams = []
        for team in teams_played_for:
            if team < current_team:
                higher_teams.append(team)

        if len(higher_teams) > 1:
            return False, f'{player} is inelgiible due to team tying, he has played for a higher team on {len(higher_teams)} occasions'

    return True, None


def has_6_unique_reg_players(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that there are 6 unique players on the team that are in the subs and lower team list
    :param proposed_team: dict with key:val like 'D1':'Conor Waldron', it will always have 6 entires one for each D1, D1B, D2, D2B, D3, D3B
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    required_players = ['D1', 'D1B', 'D2', 'D2B', 'D3', 'D3B']
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


def winter_lg_doubles_team_and_class_checker(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that no doubles player is playing above someone of a better class
    Checks that no doubles player is playing above someone from a better team

    :param proposed_team: dict with key:val like 'D1':'Conor Waldron', it will always have 6 entires one for each D1, D1B, D2, D2B, D3, D3B
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    doubles_pairs = ['D1', 'D1B', 'D2', 'D2B', 'D3', 'D3B']  # Add the third doubles pairings

    # Iterate over each doubles pair except the bottom 1, and check if that pair is valid compared to the one below
    for i in range(0, len(doubles_pairs)-2, 2):
        player1 = proposed_team[doubles_pairs[i]]
        player2 = proposed_team[doubles_pairs[i + 1]]

        class_player1 = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == player1]['Class'].iloc(0)[0]
        team_player1 = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == player1]['Team'].iloc(0)[0]

        class_player2 = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == player2]['Class'].iloc(0)[0]
        team_player2 = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == player2]['Team'].iloc(0)[0]

        # Checks that no doubles player is playing above someone of a better class, by for each pair just comparing to the pair immediately below
        weakest_class_pair = max(class_player1, class_player2)
        strongest_class_pair_immediately_below = min(
            team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team[doubles_pairs[i + 2]]]['Class'].iloc(0)[0],
            team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team[doubles_pairs[i + 3]]]['Class'].iloc(0)[0]
        )

        if weakest_class_pair > strongest_class_pair_immediately_below:
            return False, f'Your {i // 2 + 1} doubles contains a class {weakest_class_pair} player which is better than one of the players on your {i // 2 + 2} doubles (class {strongest_class_pair_immediately_below})'

        # Checks that no doubles player is playing above someone from a better team
        if (team_player1 != 'Sub') or (team_player2 != 'Sub'):
            if team_player1 == 'Sub':
                team_player1 = 0 # set to lowest team possible
            if team_player2 == 'Sub':
                team_player2 = 0 # set to lowest team possible
            max_reg_team = max(team_player1, team_player2)
            # lower players could be subs
            team_of_player1_in_pairing_immediately_below = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team[doubles_pairs[i + 2]]]['Team'].iloc(0)[0]
            team_of_player2_in_pairing_immediately_below = team_subs_and_lower_teams[team_subs_and_lower_teams['Name'] == proposed_team[doubles_pairs[i + 3]]]['Team'].iloc(0)[0]
            if team_of_player1_in_pairing_immediately_below == 'Sub':
                team_of_player1_in_pairing_immediately_below = 100 # big number to show they are on a low team
            if team_of_player2_in_pairing_immediately_below == 'Sub':
                team_of_player2_in_pairing_immediately_below = 100  # big number to show they are on a low team

            min_reg_team_immediately_below = min(team_of_player1_in_pairing_immediately_below, team_of_player2_in_pairing_immediately_below)

            if min_reg_team_immediately_below < max_reg_team:
                return False, f'Your {i // 2 + 1} doubles contains a player registered to team {max_reg_team} which is better than one of the players on your {i // 2 + 2} doubles (registered to team {min_reg_team_immediately_below})'

    return True, None


def winter_lg_doubles_reg_6_right_order(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that if you are using your 6 registered players, that they match the registration order

    :param proposed_team: dict with key:val like 'D1':'Conor Waldron', it will always have 6 entires one for each D1, D1B, D2, D2B, D3, D3B
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    doubles_pairs = ['D1', 'D1B', 'D2', 'D2B', 'D3', 'D3B']  # Add the third doubles pairings

    registered_doubles_players = set()
    proposed_doubles_players = set()

    # Collect registered and proposed doubles players
    for pos in doubles_pairs:
        registered_doubles_players.add(registered_team[registered_team['Position'] == pos]['Name'].iloc(0)[0])
        proposed_doubles_players.add(proposed_team[pos])

    if registered_doubles_players == proposed_doubles_players:
        # Check the order of the doubles pairs
        for i in range(0, len(doubles_pairs), 2):
            reg_pair = set()
            reg_pair.add(registered_team[registered_team['Position'] == doubles_pairs[i]]['Name'].iloc(0)[0])
            reg_pair.add(registered_team[registered_team['Position'] == doubles_pairs[i + 1]]['Name'].iloc(0)[0])

            proposed_pair = set()
            proposed_pair.add(proposed_team[doubles_pairs[i]])
            proposed_pair.add(proposed_team[doubles_pairs[i + 1]])

            if reg_pair != proposed_pair:
                return False, 'All 6 registered players are playing, but not in the right order'
        return True, None # you are using your 6 registered players in the right order
    return True, None # you are not using your 6 registered players, so this function is not needed


def winter_lg_doubles_previous_orders(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that no doubles pairing is playing above a pairing that they previously played below on a prior week

    :param proposed_team: dict with key:val like 'D1':'Conor Waldron', it will always have 6 entires one for each D1, D1B, D2, D2B, D3, D3B
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name, Class and Team for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks: pd df with columns Team, Position, Week1, Week2...
    :return: bool, str: the string is the reason why the test failed if it failed
    """
    doubles_pairs = ['D1', 'D1B', 'D2', 'D2B', 'D3', 'D3B']  # Add the third doubles pairings

    # Build a dictionary with of your proposed pairings, where the keys are 1, 2, 3 and the values are sets of the 2 player names
    proposed_pairings_dict = {}
    # Build a dictionary with of lists of players who played above your proposed pairings, where the keys are 1, 2, 3 and the values are lists of sets of pairings who played ahead of them
    dict_of_who_played_above_pairings = {}
    for i in range(0, len(doubles_pairs), 2):
        # Take two players and but them into pairs at a time
        pair = doubles_pairs[i:i + 2]
        player_1_of_pairing = proposed_team[pair[0]]
        player_2_of_pairing = proposed_team[pair[1]]
        proposed_pairings_dict[i/2 + 1] = {player_1_of_pairing, player_2_of_pairing}
        dict_of_who_played_above_pairings[i/2 + 1] = [] # initilise the list of pairings who played above this proposed pairing as an empty list

    # Check in previous weeks have any of your proposed pairings every played together before?
    # If so then build up a dictionary of those pairings who played above them in the past.
    for i in range(5):
        week = 'Week' + str(i + 1)
        that_week = previous_weeks[['Team', 'Position', week]]
        for proposed_pairing_number, proposed_pairing in enumerate(proposed_pairings_dict.values()):
            proposed_pairing_tuple = tuple(proposed_pairing)
            player_1 = proposed_pairing_tuple[0]
            player_2 = proposed_pairing_tuple[1]

            player1_played_previous_raw = that_week[that_week[week] == player_1][['Team', 'Position']].values
            player2_played_previous_raw = that_week[that_week[week] == player_2][['Team', 'Position']].values
            try: # handle nulls if player has not played before
                player1_played_previous = player1_played_previous_raw[0]
            except:
                player1_played_previous = ['not played', 'not played']
            try:  # handle nulls if player has not played before
                player2_played_previous = player2_played_previous_raw[0]
            except:
                player2_played_previous = ['not played', 'not played']
            # check if they played together
            if player1_played_previous[0] == player2_played_previous[0]: # played on same team
                if player1_played_previous[1][0:2] == player2_played_previous[1][0:2]: # they were a pairing!
                    # add all the doubles players who played above them to a set to record who played above them
                    # Iterate through the list in reverse, taking two elements at a time
                    team_that_week = that_week[that_week['Team'] == player1_played_previous[0]][['Position', week]]
                    start_adding_higher_pairs = False
                    for i in range(len(doubles_pairs) - 1, 0, -2):
                        a_pair = doubles_pairs[i - 1:i + 1]
                        if start_adding_higher_pairs:
                            higher_player_1 = team_that_week[team_that_week['Position'] == a_pair[0]][week].values[0]
                            higher_player_2 = team_that_week[team_that_week['Position'] == a_pair[1]][week].values[0]
                            dict_of_who_played_above_pairings[proposed_pairing_number + 1].append({higher_player_1, higher_player_2})

                        if player1_played_previous[1][0:2] == a_pair[0][0:2]:
                            # you found what position they were playing in, now add all the higher pairs to the list
                            start_adding_higher_pairs = True

    # now that the dictionary is prepared, we should look to see if the proposed pairings violate the higher players in the dictionary
    # starting with the highest pairing, check if they are above any of the players in their own dict of players that played above them in previous weeks
    for doubles_position, pairing in proposed_pairings_dict.items():
        list_of_pairings_who_played_higher = dict_of_who_played_above_pairings[doubles_position]
        for higher_pairing in list_of_pairings_who_played_higher:
            # check if that is one of the proposed pairings
            if higher_pairing in proposed_pairings_dict.values():
                # find the position of the previous higher pairing
                for key, value in proposed_pairings_dict.items():
                    if value == higher_pairing:
                        previous_higher_pair_position = key
                        break
                if doubles_position < previous_higher_pair_position:
                    return False, f'Your {int(doubles_position)} doubles pairing is illegal as they are playing above a pairing who on a previous week had played higher than they had'

    return True, None