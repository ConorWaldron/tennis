'''
run with    pytest test_summer.py -vv
if pytest is not installed properly, you can try to run with python -m pytest test_summer.py -vv
'''

import pytest
import pandas as pd
import os

from dashapp.eligibility_rules import has_7_unique_reg_players, team_played_before, singles_right_order,\
    summer_lg_doubles_team_and_class_checker, summer_lg_doubles_right_order, team_tied


def read_file_with_absolute_path(relative_path):
    """
    :param relative_path: str
    :return df: pd dataframe

    note we use relative paths so the unit tests run both on the local machine when the filepath is C:/Users/conor/repos/tennis/dashapp
    and on the github action runner when the filepath is /home/runner/work/tennis/tennis/dashapp
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(current_directory, relative_path)
    df = pd.read_csv(absolute_path)
    return df


# Define the fixtures
@pytest.fixture(scope='session')
def summer_team_7_df():
    team_df = read_file_with_absolute_path('unittest_data/summer_teams_test.csv')
    summer_team_7_df = team_df[team_df['Team'] == 7]
    return summer_team_7_df


@pytest.fixture(scope='session')
def summer_team_4_df():
    team_df = read_file_with_absolute_path('unittest_data/summer_teams_test.csv')
    summer_team_4_df = team_df[team_df['Team'] == 4]
    return summer_team_4_df


@pytest.fixture(scope='session')
def summer_team_3_df():
    team_df = read_file_with_absolute_path('unittest_data/summer_teams_test.csv')
    summer_team_3_df = team_df[team_df['Team'] == 3]
    return summer_team_3_df


@pytest.fixture(scope='session')
def summer_team_2_df():
    team_df = read_file_with_absolute_path('unittest_data/summer_teams_test.csv')
    summer_team_2_df = team_df[team_df['Team'] == 2]
    return summer_team_2_df


@pytest.fixture(scope='session')
def summer_team_7_subs_and_lower_class_df():
    team_df = read_file_with_absolute_path('unittest_data/summer_teams_test.csv')
    team_7_df = team_df[team_df['Team'] == 7]
    lower_teams = team_df[team_df['Team'] > 7][['Name', 'Class', 'Team']]

    subs_df = read_file_with_absolute_path('unittest_data/summer_subs_test.csv')
    relevant_subs = subs_df[subs_df['Class'] >= 7].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_7_df[['Name', 'Class', 'Team']]
    summer_team_7_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return summer_team_7_subs_and_lower_class_df


@pytest.fixture(scope='session')
def summer_team_4_subs_and_lower_class_df():
    team_df = read_file_with_absolute_path('unittest_data/summer_teams_test.csv')
    team_4_df = team_df[team_df['Team'] == 4]
    lower_teams = team_df[team_df['Team'] > 4][['Name', 'Class', 'Team']]

    subs_df = read_file_with_absolute_path('unittest_data/summer_subs_test.csv')
    relevant_subs = subs_df[subs_df['Class'] >= 4].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_4_df[['Name', 'Class', 'Team']]
    summer_team_4_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return summer_team_4_subs_and_lower_class_df


@pytest.fixture(scope='session')
def summer_team_3_subs_and_lower_class_df():
    team_df = read_file_with_absolute_path('unittest_data/summer_teams_test.csv')
    team_3_df = team_df[team_df['Team'] == 3]
    lower_teams = team_df[team_df['Team'] > 3][['Name', 'Class', 'Team']]

    subs_df = read_file_with_absolute_path('unittest_data/summer_subs_test.csv')
    relevant_subs = subs_df[subs_df['Class'] >= 3].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_3_df[['Name', 'Class', 'Team']]
    summer_team_3_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return summer_team_3_subs_and_lower_class_df


@pytest.fixture(scope='session')
def summer_team_2_subs_and_lower_class_df():
    team_df = read_file_with_absolute_path('unittest_data/summer_teams_test.csv')
    team_2_df = team_df[team_df['Team'] == 2]
    lower_teams = team_df[team_df['Team'] > 2][['Name', 'Class', 'Team']]

    subs_df = read_file_with_absolute_path('unittest_data/summer_subs_test.csv')
    relevant_subs = subs_df[subs_df['Class'] >= 2].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_2_df[['Name', 'Class', 'Team']]
    summer_team_2_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return summer_team_2_subs_and_lower_class_df


@pytest.fixture(scope='session')
def summer_prev_week1():
    summer_prev_week1 = read_file_with_absolute_path('unittest_data/summer_after_week1.csv')
    return summer_prev_week1


@pytest.fixture(scope='session')
def summer_prev_week2():
    summer_prev_week2 = read_file_with_absolute_path('unittest_data/summer_after_week2.csv')
    return summer_prev_week2


@pytest.fixture(scope='session')
def summer_prev_week3():
    summer_prev_week3 = read_file_with_absolute_path('unittest_data/summer_after_week3.csv')
    return summer_prev_week3


@pytest.fixture(scope='session')
def summer_proposed_team_6_players():
    summer_proposed_team_6_players = {
        'S1': "Adam Escalante",
        'S3': "Shane Bergin",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return summer_proposed_team_6_players


@pytest.fixture(scope='session')
def summer_proposed_team_same_player_twice():
    summer_proposed_team_same_player_twice = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Conor Waldron",
    }
    return summer_proposed_team_same_player_twice


@pytest.fixture(scope='session')
def summer_proposed_team_not_valid_sub():
    summer_proposed_team_not_valid_sub = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Owen Casey",
    }
    return summer_proposed_team_not_valid_sub


@pytest.fixture(scope='session')
def summer_valid_team_4():
    summer_valid_team_4 = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return summer_valid_team_4


@pytest.fixture(scope='session')
def summer_reg_team_4_wrong_order():
    summer_reg_team_4_wrong_order = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Andrew Synnott",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Shane Bergin",
    }
    return summer_reg_team_4_wrong_order


@pytest.fixture(scope='session')
def summer_team_4_same_as_week2_wrong_order():
    summer_team_4_same_as_week2_wrong_order = {
        'S1': "Adam Escalante",
        'S2': "James Fagan",
        'S3': "James Doyle",
        'D1': "Martin Henihan",
        'D1B': "Peter Morgan",
        'D2': "Russell Boland",
        'D2B': "Peter Johnston",
    }
    return summer_team_4_same_as_week2_wrong_order


@pytest.fixture(scope='session')
def summer_team_4_singles_out_order():
    summer_team_4_singles_out_order = {
        'S1': "Adam Escalante",
        'S2': "Shane Bergin",
        'S3': "Conor Waldron",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return summer_team_4_singles_out_order


@pytest.fixture(scope='session')
def summer_team_4_singles_out_order_class():
    summer_team_4_singles_out_order_class = {
        'S1': "Adam Escalante",
        'S2': "Brian Masterson",
        'S3': "Conor Waldron",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return summer_team_4_singles_out_order_class


@pytest.fixture(scope='session')
def summer_team_4_singles_out_order_team():
    summer_team_4_singles_out_order_team = {
        'S1': "Adam Escalante",
        'S2': "James Fagan",
        'S3': "Conor Waldron",
        'D1': "Peter Cloonan",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return summer_team_4_singles_out_order_team


@pytest.fixture(scope='session')
def summer_team_4_invalid_doubles_class():
    summer_team_4_invalid_doubles_class = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Brian Masterson",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return summer_team_4_invalid_doubles_class


@pytest.fixture(scope='session')
def summer_team_4_invalid_doubles_team():
    summer_team_4_invalid_doubles_team = {
        'S1': "Adam Escalante",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "Russell Boland",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return summer_team_4_invalid_doubles_team


@pytest.fixture(scope='session')
def summer_team_3_invalid_doubles_order():
    summer_team_3_invalid_doubles_order = {
        'S1': "Caleb Mok",
        'S2': "Mark Cloonan",
        'S3': "Conor Waldron",
        'D1': "Jerry Sheehan",
        'D1B': "Conor O'Neill",
        'D2': "Jimmy McDonogh",
        'D2B': "Justin Purcell",
    }
    return summer_team_3_invalid_doubles_order


@pytest.fixture(scope='session')
def summer_team_2_invalid_doubles_order():
    summer_team_2_invalid_doubles_order = {
        'S1': "Joe Kelleher",
        'S2': "Mark Cloonan",
        'S3': "Conor Waldron",
        'D1': "Tom Brophy",
        'D1B': "Eoin Donohoe",
        'D2': "Fernando Mayorga",
        'D2B': "Ivan Casinillo",
    }
    return summer_team_2_invalid_doubles_order


@pytest.fixture(scope='session')
def summer_valid_team_7():
    summer_valid_team_7 = {
        'S1': "Kabir Kalia",
        'S2': "Rory Aherne",
        'S3': "Darragh Moran",
        'D1': "Stephen O'Meara",
        'D1B': "Eoghan O'Meara",
        'D2': "Max Lebrocquy",
        'D2B': "Ryan McGrath",
    }
    return summer_valid_team_7


@pytest.fixture(scope='session')
def summer_invalid_team_7_team_tied():
    summer_invalid_team_7_team_tied = {
        'S1': "Kabir Kalia",
        'S2': "Rory Aherne",
        'S3': "Darragh Moran",
        'D1': "Stephen O'Meara",
        'D1B': "Eoghan O'Meara",
        'D2': "Max Lebrocquy",
        'D2B': "Ryan McGrath",
    }
    return summer_invalid_team_7_team_tied


#@pytest.mark.skip
def test_has_7_unique_reg_players(summer_proposed_team_6_players, summer_proposed_team_same_player_twice, summer_proposed_team_not_valid_sub,
                                  summer_valid_team_4, summer_team_4_df, summer_team_4_subs_and_lower_class_df):
    '''
    Checks that
    at least 7 playes are entered
    all 7 ployers are unique
    all 7 players are on that team, or lower teams or are subs at that class
    '''
    expected_value = False, 'no player was entered in position S2'
    actual_value = has_7_unique_reg_players(summer_proposed_team_6_players, summer_team_4_df, summer_team_4_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'you entered Conor Waldron twice'
    actual_value = has_7_unique_reg_players(summer_proposed_team_same_player_twice, summer_team_4_df, summer_team_4_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'Owen Casey is not in the list of valid subs or registered teams at or below this class level'
    actual_value = has_7_unique_reg_players(summer_proposed_team_not_valid_sub, summer_team_4_df, summer_team_4_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = True, None
    actual_value = has_7_unique_reg_players(summer_valid_team_4, summer_team_4_df, summer_team_4_subs_and_lower_class_df, None)
    assert expected_value == actual_value


#@pytest.mark.skip
def test_team_played_before(summer_valid_team_4, summer_reg_team_4_wrong_order, summer_team_4_same_as_week2_wrong_order,
                            summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week1, summer_prev_week2):
    """
    Checks that
    if your 7 players are your registered 7 that they play in those positions
    if your 7 players have all played on same day as before that they play in the same positions
    """
    expected_value = True, None
    actual_value = team_played_before(summer_valid_team_4, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, "you are using the same players as your registered team but Andrew Synnott is not playing in the registered position of D2"
    actual_value = team_played_before(summer_reg_team_4_wrong_order, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, "you are using the same players as week 2 team but James Fagan is not playing in the old position of S3"
    actual_value = team_played_before(summer_team_4_same_as_week2_wrong_order, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value


# @pytest.mark.skip
def test_singles_right_order(summer_valid_team_4, summer_team_4_singles_out_order,
                             summer_team_4_singles_out_order_class, summer_team_4_singles_out_order_team,
                             summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2):
    """
    Checks that
    you never play a singles player above someone who has played before them before
    you never play a singles player above someone of a better class
    you never play a singles player above someone from a higher team
    """
    expected_value = True, None
    actual_value = singles_right_order(summer_valid_team_4, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, 'You are playing Shane Bergin ahead of Conor Waldron but that violates a previous weeks order'
    actual_value = singles_right_order(summer_team_4_singles_out_order, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, 'You are playing Brian Masterson (class 5) ahead of Conor Waldron (class 4)'
    actual_value = singles_right_order(summer_team_4_singles_out_order_class, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, 'You are playing James Fagan (team 5) ahead of Conor Waldron (team 4)'
    actual_value = singles_right_order(summer_team_4_singles_out_order_team, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value


# @pytest.mark.skip
def test_doubles_team_and_class_checker(summer_valid_team_4, summer_team_4_invalid_doubles_class,
                                        summer_team_4_invalid_doubles_team,
                                        summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2):
    """
    Checks that
    you never play a doubles player above someone of a better class
    you never play a doubles player above someone from a higher team
    """
    expected_value = True, None
    actual_value = summer_lg_doubles_team_and_class_checker(summer_valid_team_4, summer_team_4_df, summer_team_4_subs_and_lower_class_df,
                                                            summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, 'Your 2nd doubles contains a class 4 player which is better than one of the players on your first doubles (class 5)'
    actual_value = summer_lg_doubles_team_and_class_checker(summer_team_4_invalid_doubles_class, summer_team_4_df,
                                                            summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, 'Your 2nd doubles contains a player registered to team 4 which is better than one of the players on your first doubles (registered to team 5)'
    actual_value = summer_lg_doubles_team_and_class_checker(summer_team_4_invalid_doubles_team, summer_team_4_df,
                                                            summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value


# @pytest.mark.skip
def test_doubles_right_order(summer_valid_team_4, summer_team_3_invalid_doubles_order, summer_team_2_invalid_doubles_order,
                             summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2,
                             summer_team_3_df, summer_team_3_subs_and_lower_class_df,
                             summer_team_2_df, summer_team_2_subs_and_lower_class_df):
    """
    Checks that
    you never play a doubles player above someone who has played before them before
    you never play a 2nd doubles reg team ahead of a 1st doubles reg team
    """
    expected_value = True, None
    actual_value = summer_lg_doubles_right_order(summer_valid_team_4, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, 'Your 2nd doubles pairing have played above your first doubles pairing in a previous week'
    actual_value = summer_lg_doubles_right_order(summer_team_2_invalid_doubles_order, summer_team_2_df, summer_team_2_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, 'all 4 registered players are playing doubles, but not in the right order'
    actual_value = summer_lg_doubles_right_order(summer_team_3_invalid_doubles_order, summer_team_3_df, summer_team_3_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value


# @pytest.mark.skip
def test_team_tied(summer_valid_team_4, summer_valid_team_7, summer_invalid_team_7_team_tied, summer_prev_week2, summer_prev_week3,
                   summer_team_4_df, summer_team_4_subs_and_lower_class_df,
                   summer_team_7_df, summer_team_7_subs_and_lower_class_df):
    expected_value = True, None
    actual_value = team_tied(summer_valid_team_4, summer_team_4_df, summer_team_4_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = True, None
    actual_value = team_tied(summer_valid_team_7, summer_team_7_df, summer_team_7_subs_and_lower_class_df, summer_prev_week2)
    assert expected_value == actual_value

    expected_value = False, 'Kabir Kalia is inelgiible due to team tying, he has played for a higher team on 2 occasions'
    actual_value = team_tied(summer_valid_team_7, summer_team_7_df, summer_team_7_subs_and_lower_class_df, summer_prev_week3)
    assert expected_value == actual_value
