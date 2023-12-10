from leagues import summer_league_eligibility, winter_league_eligibility
from eligibility_rules import winter_lg_doubles_team_and_class_checker, winter_lg_doubles_reg_6_right_order, winter_lg_doubles_previous_orders
import pandas as pd

if __name__ == '__main__':
    summer_reg_team = pd.read_csv('../assets/summer_league/teams.csv')
    summer_reg_subs = pd.read_csv('../assets/summer_league/subs.csv')
    summer_prev_weeks = pd.read_csv('../assets/summer_league/previous_weeks.csv')

    summer_my_proposed_team = {
        'S1': "Kabir Kalia",
        'S2': "Rory Aherne",
        'S3': "Darragh Moran",
        'D1': "Stephen O'Meara",
        'D1B': "Eoghan O'Meara",
        'D2': "Max Lebrocquy",
        'D2B': "Ryan McGrath",
    }

    #eligible, warning = summer_league_eligibility(7, summer_my_proposed_team, summer_reg_team, summer_reg_subs, summer_prev_weeks)
    #print(warning)

    winter_reg_team = pd.read_csv('../assets/winter_league/teams.csv')
    winter_reg_subs = pd.read_csv('../assets/winter_league/subs.csv')
    winter_prev_weeks = pd.read_csv('../assets/winter_league/previous_weeks.csv')

    winter_my_proposed_team = {
        'D1': "Ronan O'Brien",
        'D1B': "Adam Casey",
        'D2': "Conor Waldron",
        'D2B': "Mark Cloonan",
        'D3': "Joseph Kelleher",
        'D3B': "Shane Bergin",
    }

    #eligible, warning = winter_league_eligibility(3, winter_my_proposed_team, winter_reg_team, winter_reg_subs, winter_prev_weeks)
    #print(warning)
    team_number = 3
    relevant_team = winter_reg_team[winter_reg_team['Team'] == team_number]
    relevant_team_class = relevant_team['Class'].iloc(0)[0]
    lower_teams = winter_reg_team[winter_reg_team['Team'] > team_number][['Name', 'Class', 'Team']]

    relevant_subs = winter_reg_subs[winter_reg_subs['Class'] >= relevant_team_class].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = relevant_team[['Name', 'Class', 'Team']]
    team_subs_and_lower_teams = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    previous_weeks = winter_prev_weeks

    #valid, message = winter_lg_doubles_team_and_class_checker(winter_my_proposed_team, relevant_team, team_subs_and_lower_teams, previous_weeks)
    #print(message)

    valid, message = winter_lg_doubles_team_and_class_checker(winter_my_proposed_team, relevant_team,
                                                         team_subs_and_lower_teams, previous_weeks)
    print(message)