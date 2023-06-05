'run with pytest test.py -vv'

import pytest
import pandas as pd

from tennis.eligibility_rules import has_7_unique_reg_players, team_played_before, singles_right_order,\
    doubles_team_and_class_checker, doubles_right_order, team_tied


# Define the fixtures

@pytest.fixture(scope='session')
def team_7_df():
    team_df = pd.read_csv('teams_test.csv')
    team_7_df = team_df[team_df['Team'] == 7]
    return team_7_df


@pytest.fixture(scope='session')
def team_4_df():
    team_df = pd.read_csv('teams_test.csv')
    team_4_df = team_df[team_df['Team'] == 4]
    return team_4_df


@pytest.fixture(scope='session')
def team_3_df():
    team_df = pd.read_csv('teams_test.csv')
    team_3_df = team_df[team_df['Team'] == 3]
    return team_3_df


@pytest.fixture(scope='session')
def team_2_df():
    team_df = pd.read_csv('teams_test.csv')
    team_2_df = team_df[team_df['Team'] == 2]
    return team_2_df


@pytest.fixture(scope='session')
def team_7_subs_and_lower_class_df():
    team_df = pd.read_csv('teams_test.csv')
    team_7_df = team_df[team_df['Team'] == 7]
    lower_teams = team_df[team_df['Team'] > 7][['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})

    subs_df = pd.read_csv('subs_test.csv')
    relevant_subs = subs_df[subs_df['Lowest_Class'] >= 7].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_7_df[['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})
    team_7_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return team_7_subs_and_lower_class_df


@pytest.fixture(scope='session')
def team_4_subs_and_lower_class_df():
    team_df = pd.read_csv('teams_test.csv')
    team_4_df = team_df[team_df['Team'] == 4]
    lower_teams = team_df[team_df['Team'] > 4][['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})

    subs_df = pd.read_csv('subs_test.csv')
    relevant_subs = subs_df[subs_df['Lowest_Class'] >= 4].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_4_df[['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})
    team_4_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return team_4_subs_and_lower_class_df


@pytest.fixture(scope='session')
def team_3_subs_and_lower_class_df():
    team_df = pd.read_csv('teams_test.csv')
    team_3_df = team_df[team_df['Team'] == 3]
    lower_teams = team_df[team_df['Team'] > 3][['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})

    subs_df = pd.read_csv('subs_test.csv')
    relevant_subs = subs_df[subs_df['Lowest_Class'] >= 3].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_3_df[['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})
    team_3_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return team_3_subs_and_lower_class_df


@pytest.fixture(scope='session')
def team_2_subs_and_lower_class_df():
    team_df = pd.read_csv('teams_test.csv')
    team_2_df = team_df[team_df['Team'] == 2]
    lower_teams = team_df[team_df['Team'] > 2][['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})

    subs_df = pd.read_csv('subs_test.csv')
    relevant_subs = subs_df[subs_df['Lowest_Class'] >= 2].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_2_df[['Name', 'Class', 'Team']].rename(columns={'Class': 'Lowest_Class'})
    team_2_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return team_2_subs_and_lower_class_df


@pytest.fixture(scope='session')
def prev_week1_team_4():
    prev_week1 = pd.read_csv('after_week1.csv')
    prev_week1_team_4 = prev_week1[prev_week1['Team'] == 4]
    return prev_week1_team_4


@pytest.fixture(scope='session')
def prev_week2_team_4():
    prev_week2 = pd.read_csv('after_week2.csv')
    prev_week2_team_4 = prev_week2[prev_week2['Team'] == 4]
    return prev_week2_team_4


@pytest.fixture(scope='session')
def prev_week2_team_3():
    prev_week2 = pd.read_csv('after_week2.csv')
    prev_week2_team_3 = prev_week2[prev_week2['Team'] == 3]
    return prev_week2_team_3


@pytest.fixture(scope='session')
def prev_week2_team_2():
    prev_week2 = pd.read_csv('after_week2.csv')
    prev_week2_team_2 = prev_week2[prev_week2['Team'] == 2]
    return prev_week2_team_2


@pytest.fixture(scope='session')
def prev_week3_team_7():
    prev_week3 = pd.read_csv('after_week3.csv')
    prev_week3_team_7 = prev_week3[prev_week3['Team'] == 7]
    return prev_week3_team_7


@pytest.fixture(scope='session')
def proposed_team_6_players():
    proposed_team_6_players = {
        'S1': "Adam Escalante",
        'S3': "Shane Bergin",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return proposed_team_6_players


@pytest.fixture(scope='session')
def proposed_team_same_player_twice():
    proposed_team_same_player_twice = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Conor Waldron",
    }
    return proposed_team_same_player_twice


@pytest.fixture(scope='session')
def proposed_team_not_valid_sub():
    proposed_team_not_valid_sub = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Owen Casey",
    }
    return proposed_team_not_valid_sub


@pytest.fixture(scope='session')
def valid_team_4():
    valid_team_4 = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return valid_team_4


@pytest.fixture(scope='session')
def reg_team_4_wrong_order():
    reg_team_4_wrong_order = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Andrew Synnott",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Shane Bergin",
    }
    return reg_team_4_wrong_order


@pytest.fixture(scope='session')
def team_4_same_as_week2_wrong_order():
    team_4_same_as_week2_wrong_order = {
        'S1': "Adam Escalante",
        'S2': "James Fagan",
        'S3': "James Doyle",
        'D1': "Martin Henihan",
        'D1B': "Peter Morgan",
        'D2': "Russell Boland",
        'D2B': "Peter Johnston",
    }
    return team_4_same_as_week2_wrong_order


@pytest.fixture(scope='session')
def team_4_singles_out_order():
    team_4_singles_out_order = {
        'S1': "Adam Escalante",
        'S2': "Shane Bergin",
        'S3': "Conor Waldron",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return team_4_singles_out_order


@pytest.fixture(scope='session')
def team_4_singles_out_order_class():
    team_4_singles_out_order_class = {
        'S1': "Adam Escalante",
        'S2': "Brian Masterson",
        'S3': "Conor Waldron",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return team_4_singles_out_order_class


@pytest.fixture(scope='session')
def team_4_singles_out_order_team():
    team_4_singles_out_order_team = {
        'S1': "Adam Escalante",
        'S2': "James Fagan",
        'S3': "Conor Waldron",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return team_4_singles_out_order_team


@pytest.fixture(scope='session')
def team_4_invalid_doubles_class():
    team_4_invalid_doubles_class = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Brian Masterson",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return team_4_invalid_doubles_class


@pytest.fixture(scope='session')
def team_4_invalid_doubles_team():
    team_4_invalid_doubles_team = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Russell Boland",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return team_4_invalid_doubles_team


@pytest.fixture(scope='session')
def team_3_invalid_doubles_order():
    team_3_invalid_doubles_order = {
        'S1': "Caleb Mok",
        'S2': "Mark Cloonan",
        'S3': "Conor Waldron",
        'D1': "Jerry Sheehan",
        'D1B': "Conor O'Neill",
        'D2': "Jimmy McDonogh",
        'D2B': "Justin Purcell",
    }
    return team_3_invalid_doubles_order


@pytest.fixture(scope='session')
def team_2_invalid_doubles_order():
    team_2_invalid_doubles_order = {
        'S1': "Joe Kelleher",
        'S2': "Mark Cloonan",
        'S3': "Conor Waldron",
        'D1': "Tom Brophy",
        'D1B': "Eoin Donohoe",
        'D2': "Fernando Mayorga",
        'D2B': "Ivan Casinillo",
    }
    return team_2_invalid_doubles_order


@pytest.fixture(scope='session')
def valid_team_7():
    valid_team_7 = {
        'S1': "Kabir Kalia",
        'S2': "Rory Aherne",
        'S3': "Darragh Moran",
        'D1': "Stephen O'Meara",
        'D1B': "Eoghan O'Meara",
        'D2': "Max Lebrocquy",
        'D2B': "Ryan McGrath",
    }
    return valid_team_7


@pytest.fixture(scope='session')
def invalid_team_7_team_tied():
    invalid_team_7_team_tied = {
        'S1': "Kabir Kalia",
        'S2': "Rory Aherne",
        'S3': "Darragh Moran",
        'D1': "Stephen O'Meara",
        'D1B': "Eoghan O'Meara",
        'D2': "Max Lebrocquy",
        'D2B': "Ryan McGrath",
    }
    return invalid_team_7_team_tied


#@pytest.mark.skip
def test_has_7_unique_reg_players(proposed_team_6_players, proposed_team_same_player_twice, proposed_team_not_valid_sub,
                                  valid_team_4, team_4_df, team_4_subs_and_lower_class_df):
    '''
    Checks that
    at least 7 playes are entered
    all 7 ployers are unique
    all 7 players are on that team, or lower teams or are subs at that class
    '''
    expected_value = False, 'no player was entered in position S2'
    actual_value = has_7_unique_reg_players(proposed_team_6_players, team_4_df, team_4_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'you entered Conor Waldron twice'
    actual_value = has_7_unique_reg_players(proposed_team_same_player_twice, team_4_df, team_4_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'Owen Casey is not in the list of valid subs or registered teams at or below this class level'
    actual_value = has_7_unique_reg_players(proposed_team_not_valid_sub, team_4_df, team_4_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = True, None
    actual_value = has_7_unique_reg_players(valid_team_4, team_4_df, team_4_subs_and_lower_class_df, None)
    assert expected_value == actual_value


#@pytest.mark.skip
def test_team_played_before(valid_team_4, reg_team_4_wrong_order, team_4_same_as_week2_wrong_order,
                            team_4_df, team_4_subs_and_lower_class_df, prev_week1_team_4, prev_week2_team_4):
    """
    Checks that
    if your 7 players are your registered 7 that they play in those positions
    if your 7 players have all played on same day as before that they play in the same positions
    """
    expected_value = True, None
    actual_value = team_played_before(valid_team_4, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = False, "you are using the same 7 players as your registered team but Andrew Synnott is not playing in the registered position of D2"
    actual_value = team_played_before(reg_team_4_wrong_order, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = False, "you are using the same 7 players as week 2 team but James Fagan is not playing in the old position of S3"
    actual_value = team_played_before(team_4_same_as_week2_wrong_order, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value


# @pytest.mark.skip
def test_singles_right_order(valid_team_4, team_4_singles_out_order, team_4_singles_out_order_class, team_4_singles_out_order_team,
                             team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4):
    """
    Checks that
    you never play a singles player above someone who has played before them before
    you never play a singles player above someone of a better class
    you never play a singles player above someone from a higher team
    """
    expected_value = True, None
    actual_value = singles_right_order(valid_team_4, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = False, 'You are playing Shane Bergin ahead of Conor Waldron but that violates a previous weeks order'
    actual_value = singles_right_order(team_4_singles_out_order, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = False, 'You are playing Brian Masterson (class 5) ahead of Conor Waldron (class 4)'
    actual_value = singles_right_order(team_4_singles_out_order_class, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = False, 'You are playing James Fagan (team 5) ahead of Conor Waldron (team 4)'
    actual_value = singles_right_order(team_4_singles_out_order_team, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value


# @pytest.mark.skip
def test_doubles_team_and_class_checker(valid_team_4, team_4_invalid_doubles_class, team_4_invalid_doubles_team,
                             team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4):
    """
    Checks that
    you never play a doubles player above someone of a better class
    you never play a doubles player above someone from a higher team
    """
    expected_value = True, None
    actual_value = doubles_team_and_class_checker(valid_team_4, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = False, 'Your 2nd doubles contains a class 4 player which is better than one of the players on your first doubles (class 5)'
    actual_value = doubles_team_and_class_checker(team_4_invalid_doubles_class, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = False, 'Your 2nd doubles contains a player registered to team 4 which is better than one of the players on your first doubles (registered to team 5)'
    actual_value = doubles_team_and_class_checker(team_4_invalid_doubles_team, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value


# @pytest.mark.skip
def test_doubles_right_order(valid_team_4, team_3_invalid_doubles_order, team_2_invalid_doubles_order,
                             team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4,
                             team_3_df, team_3_subs_and_lower_class_df, prev_week2_team_3,
                             team_2_df, team_2_subs_and_lower_class_df, prev_week2_team_2):
    """
    Checks that
    you never play a doubles player above someone who has played before them before
    you never play a 2nd doubles reg team ahead of a 1st doubles reg team
    """
    expected_value = True, None
    actual_value = doubles_right_order(valid_team_4, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = False, 'Your 2nd doubles pairing have played above your first doubles pairing in a previous week'
    actual_value = doubles_right_order(team_2_invalid_doubles_order, team_2_df, team_2_subs_and_lower_class_df, prev_week2_team_2)
    assert expected_value == actual_value

    expected_value = False, 'all 4 registered players are playing doubles, but not in the right order'
    actual_value = doubles_right_order(team_3_invalid_doubles_order, team_3_df, team_3_subs_and_lower_class_df, prev_week2_team_3)
    assert expected_value == actual_value


# @pytest.mark.skip
def test_team_tied(valid_team_4, valid_team_7, invalid_team_7_team_tied,
                   team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4,
                   team_7_df, team_7_subs_and_lower_class_df, prev_week3_team_7):
    expected_value = True, None
    actual_value = team_tied(valid_team_4, team_4_df, team_4_subs_and_lower_class_df, prev_week2_team_4)
    assert expected_value == actual_value

    expected_value = ?
    actual_value = team_tied(valid_team_7, team_7_df, team_7_subs_and_lower_class_df, prev_week3_team_7)
    assert expected_value == actual_value

    # warning something strange, kabir is team tied after week 3 but rule is not trigger here!

    #expected_value = False, '{player} is inelgiible due to team tying, he has played for a higher team on {len(higher_teams)} occasions'
    #actual_value = team_tied(invalid_team_7_team_tied, team_7_df, team_7_subs_and_lower_class_df, prev_week3_team_7)
    #assert expected_value == actual_value
