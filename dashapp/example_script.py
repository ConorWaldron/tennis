from leagues import summer_league_eligibility, winter_league_eligibility
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
        'D1': "Neil Stokes",
        'D1B': "Ronan O'Brien",
        'D2': "Adam Escalante",
        'D2B': "James Doyle",
        'D3': "Mark Cloonan",
        'D3B': "Conor Waldron",
    }

    eligible, warning = winter_league_eligibility(3, winter_my_proposed_team, winter_reg_team, winter_reg_subs,
                                                  winter_prev_weeks)
    print(warning)