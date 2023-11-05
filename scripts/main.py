
from dashapp.summer_league import summer_league_eligibility


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

    eligible, warning = summer_league_eligibility(7, my_proposed_team)
    print(warning)
