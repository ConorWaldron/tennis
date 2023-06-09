import pandas as pd
import os

from tennis.eligibility_rules import has_7_unique_reg_players, team_played_before, singles_right_order, \
    doubles_team_and_class_checker, doubles_right_order, team_tied



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
    lower_teams = team_df[team_df['Team'] > team_number][['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})

    subs_df = pd.read_csv('../assets/subs.csv')
    relevant_subs = subs_df[subs_df['Lowest_Class'] >= relevant_team_class].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = relevant_team[['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})
    team_subs_and_lower_teams = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)

    previous_weeks = pd.read_csv('../assets/previous_weeks.csv')

    # Start checking the proposed team
    for func in [has_7_unique_reg_players, team_played_before, singles_right_order, doubles_team_and_class_checker,
                 doubles_right_order, team_tied]:
        valid, warning = func(proposed_team, relevant_team, team_subs_and_lower_teams, previous_weeks)
        if valid == False:
            print(warning)
            break
    return valid


if __name__ == '__main__':
    my_proposed_team = {
        'S1': "Kabir Kalia",
        'S2': "Rory Aherne",
        'S3': "Darragh Moran",
        'D1': "Stephen O'Meara",
        'D1B': "Eoghan O'Meara",
        'D2': "Max Lebrocquy",
        'D2B': "Ryan McGrath",
    }

    eligible = main(7, my_proposed_team)
    if eligible:
        print('team is eligible')
    else:
        print('team is not eligible')