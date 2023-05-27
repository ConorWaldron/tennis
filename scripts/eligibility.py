import pandas as pd
import os


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


def team_played_before(proposed_team, registered_team, team_subs_and_lower_teams, previous_weeks):
    """
    Checks that this exact group of 7 players hasnt played before, and if so that they play in the exact same prior order
    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :param registered_team: pd df with columns Name, Team, Class, Position for the registered team
    :param team_subs_and_lower_teams: pd df with columns Name and Lowest_Class, for team of interest and all lower teams, and all subs of class >= class of team of interest
    :param previous_weeks:
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

    return True, None


def main(team_number, proposed_team):
    """
    :param team_number, int
    :param proposed_team: dict with key:val like 'S1':'Conor Waldron', it will always have 7 entires one for each S1, S2, S3, D1, D1b, D2, D2b
    :return:
    """
    # Load in the registered teams and subs, then filter for relevant teams and relevant subs
    assert ((os.path.isfile('../assets/teams.csv')) & (os.path.isfile('../assets/teams.csv'))), 'the teams.csv and sub.csv file were not found in the assets folder'
    team_df = pd.read_csv('../assets/teams.csv')
    relevant_team = team_df[team_df['Team'] == team_number]
    relevant_team_class = relevant_team['Class'].iloc(0)[0]
    lower_teams = team_df[team_df['Team'] > team_number][['Name', 'Class']].rename(columns={'Class': 'Lowest_Class'})

    subs_df = pd.read_csv('../assets/subs.csv')
    relevant_subs = subs_df[subs_df['Lowest_Class'] >= relevant_team_class]
    team_of_interest = relevant_team[['Name', 'Class']].rename(columns={'Class': 'Lowest_Class'})
    team_subs_and_lower_teams = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)

    previous_weeks = None
    # Start checking the proposed team
    for func in [has_7_unique_reg_players, team_played_before]:
        valid, warning = func(proposed_team, relevant_team, team_subs_and_lower_teams, previous_weeks)
        if valid == False:
            print(warning)
            break
    return valid


if __name__ == '__main__':
    my_proposed_team = dict()
    my_proposed_team['S1'] = 'Adam Escalate'
    my_proposed_team['S2'] = 'Shane Bergin'
    my_proposed_team['S3'] = 'Conor Waldron'
    my_proposed_team['D1'] = 'PETER CLOONAN'
    my_proposed_team['D1B'] = "Bernard O'Sullivan"
    my_proposed_team['D2B'] = 'Peter Morgan'
    my_proposed_team['D2'] = 'Andrew Synnott'

    eligible = main(4, my_proposed_team)
    if eligible:
        print('team is eligible')
    else:
        print('team is not eligible')