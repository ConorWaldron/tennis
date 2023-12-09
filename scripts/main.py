
from dashapp.leagues import summer_league_eligibility
import pandas as pd

if __name__ == '__main__':
    reg_team = pd.read_csv('../assets/summer_league/teams.csv')
    reg_subs = pd.read_csv('../assets/summer_league/subs.csv')
    prev_weeks = pd.read_csv('../assets/summer_league/previous_weeks.csv')

    my_proposed_team = {
        'S1': "Kabir Kalia",
        'S2': "Rory Aherne",
        'S3': "Darragh Moran",
        'D1': "Stephen O'Meara",
        'D1B': "Eoghan O'Meara",
        'D2': "Max Lebrocquy",
        'D2B': "Ryan McGrath",
    }

    eligible, warning = summer_league_eligibility(7, my_proposed_team, reg_team, reg_subs, prev_weeks)
    print(warning)
