'''
run with    pytest test_winter.py -vv
if pytest is not installed properly, you can try to run with python -m pytest test_winter.py -vv
'''

import pytest
import pandas as pd
import os

from dashapp.eligibility_rules import team_played_before, winter_lg_doubles_team_and_class_checker,\
    winter_lg_doubles_reg_6_right_order, team_tied, has_6_unique_reg_players, winter_lg_doubles_previous_orders

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
def winter_team_7_df():
    team_df = read_file_with_absolute_path('unittest_data/winter_teams_test.csv')
    winter_team_7_df = team_df[team_df['Team'] == 7]
    return winter_team_7_df


@pytest.fixture(scope='session')
def winter_team_4_df():
    team_df = read_file_with_absolute_path('unittest_data/winter_teams_test.csv')
    winter_team_4_df = team_df[team_df['Team'] == 4]
    return winter_team_4_df


@pytest.fixture(scope='session')
def winter_team_3_df():
    team_df = read_file_with_absolute_path('unittest_data/winter_teams_test.csv')
    winter_team_3_df = team_df[team_df['Team'] == 3]
    return winter_team_3_df


@pytest.fixture(scope='session')
def winter_team_2_df():
    team_df = read_file_with_absolute_path('unittest_data/winter_teams_test.csv')
    winter_team_2_df = team_df[team_df['Team'] == 2]
    return winter_team_2_df


@pytest.fixture(scope='session')
def winter_team_7_subs_and_lower_class_df():
    team_df = read_file_with_absolute_path('unittest_data/winter_teams_test.csv')
    team_7_df = team_df[team_df['Team'] == 7]
    lower_teams = team_df[team_df['Team'] > 7][['Name', 'Class', 'Team']]

    subs_df = read_file_with_absolute_path('unittest_data/winter_subs_test.csv')
    relevant_subs = subs_df[subs_df['Class'] >= 7].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_7_df[['Name', 'Class', 'Team']]
    winter_team_7_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return winter_team_7_subs_and_lower_class_df


@pytest.fixture(scope='session')
def winter_team_4_subs_and_lower_class_df():
    team_df = read_file_with_absolute_path('unittest_data/winter_teams_test.csv')
    team_4_df = team_df[team_df['Team'] == 4]
    lower_teams = team_df[team_df['Team'] > 4][['Name', 'Class', 'Team']]

    subs_df = read_file_with_absolute_path('unittest_data/winter_subs_test.csv')
    relevant_subs = subs_df[subs_df['Class'] >= 4].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_4_df[['Name', 'Class', 'Team']]
    winter_team_4_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return winter_team_4_subs_and_lower_class_df


@pytest.fixture(scope='session')
def winter_team_3_subs_and_lower_class_df():
    team_df = read_file_with_absolute_path('unittest_data/winter_teams_test.csv')
    team_3_df = team_df[team_df['Team'] == 3]
    lower_teams = team_df[team_df['Team'] > 3][['Name', 'Class', 'Team']]

    subs_df = read_file_with_absolute_path('unittest_data/winter_subs_test.csv')
    relevant_subs = subs_df[subs_df['Class'] >= 3].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_3_df[['Name', 'Class', 'Team']]
    winter_team_3_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return winter_team_3_subs_and_lower_class_df


@pytest.fixture(scope='session')
def winter_team_2_subs_and_lower_class_df():
    team_df = read_file_with_absolute_path('unittest_data/winter_teams_test.csv')
    team_2_df = team_df[team_df['Team'] == 2]
    lower_teams = team_df[team_df['Team'] > 2][['Name', 'Class', 'Team']]

    subs_df = read_file_with_absolute_path('unittest_data/winter_subs_test.csv')
    relevant_subs = subs_df[subs_df['Class'] >= 2].copy()
    relevant_subs['Team'] = 'Sub'
    team_of_interest = team_2_df[['Name', 'Class', 'Team']]
    winter_team_2_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return winter_team_2_subs_and_lower_class_df


@pytest.fixture(scope='session')
def winter_prev_week1():
    winter_prev_week1 = read_file_with_absolute_path('unittest_data/winter_after_week1.csv')
    return winter_prev_week1


@pytest.fixture(scope='session')
def winter_prev_week2():
    winter_prev_week2 = read_file_with_absolute_path('unittest_data/winter_after_week2.csv')
    return winter_prev_week2


@pytest.fixture(scope='session')
def winter_prev_week3():
    winter_prev_week3 = read_file_with_absolute_path('unittest_data/winter_after_week3.csv')
    return winter_prev_week3

@pytest.fixture(scope='session')
def winter_prev_week4():
    winter_prev_week4 = read_file_with_absolute_path('unittest_data/winter_after_week4.csv')
    return winter_prev_week4


@pytest.fixture(scope='session')
def winter_proposed_team_3_valid():
    winter_proposed_team_3_valid = {
        'D1': "Ronan O'Brien",
        'D1B': "Neil Stokes",
        'D2': "Adam Escalante",
        'D2B': "James Doyle",
        'D3': "Mark Cloonan",
        'D3B': "Conor Waldron",
    }
    return winter_proposed_team_3_valid

@pytest.fixture(scope='session')
def winter_proposed_team_3_invalid_wrong_order():
    winter_proposed_team_3_invalid_wrong_order = {
        'D1': "Ronan O'Brien",
        'D1B': "Conor Waldron",
        'D2': "Adam Escalante",
        'D2B': "James Doyle",
        'D3': "Mark Cloonan",
        'D3B': "Neil Stokes",
    }
    return winter_proposed_team_3_invalid_wrong_order

@pytest.fixture(scope='session')
def winter_proposed_team_3_only_5_players():
    winter_proposed_team_3_only_5_players = {
        'D1': "Ronan O'Brien",
        'D1B': "Neil Stokes",
        'D2': "Adam Escalante",
        'D2B': "James Doyle",
        'D3B': "Conor Waldron",
    }
    return winter_proposed_team_3_only_5_players

@pytest.fixture(scope='session')
def winter_proposed_team_3_repeated_player():
    winter_proposed_team_3_repeated_player = {
        'D1': "Ronan O'Brien",
        'D1B': "Neil Stokes",
        'D2': "Adam Escalante",
        'D2B': "James Doyle",
        'D3': "Conor Waldron",
        'D3B': "Conor Waldron",
    }
    return winter_proposed_team_3_repeated_player

@pytest.fixture(scope='session')
def winter_proposed_team_3_owen():
    winter_proposed_team_3_owen = {
        'D1': "Ronan O'Brien",
        'D1B': "Neil Stokes",
        'D2': "Adam Escalante",
        'D2B': "James Doyle",
        'D3': "Conor Waldron",
        'D3B': "Owen Casey",
    }
    return winter_proposed_team_3_owen

@pytest.fixture(scope='session')
def winter_proposed_team_3_invalid_better_class():
    winter_proposed_team_3_invalid_better_class = {
        'D1': "Darren Cappelli",
        'D1B': "Neil Stokes",
        'D2': "Adam Escalante",
        'D2B': "James Doyle",
        'D3': "Mark Cloonan",
        'D3B': "Conor Waldron",
    }
    return winter_proposed_team_3_invalid_better_class

@pytest.fixture(scope='session')
def winter_proposed_team_3_invalid_better_class2():
    winter_proposed_team_3_invalid_better_class2 = {
        'D1': "Ronan O'Brien",
        'D1B': "Neil Stokes",
        'D2': "Adam Escalante",
        'D2B': "Max Ryan",
        'D3': "Mark Cloonan",
        'D3B': "Conor Waldron",
    }
    return winter_proposed_team_3_invalid_better_class2

@pytest.fixture(scope='session')
def winter_proposed_team_2_valid():
    winter_proposed_team_2_valid = {
        'D1': "Tom Brophy",
        'D1B': "Freddie Bracken",
        'D2': "Rico Raymundo",
        'D2B': "Ivan Ray Casinillo",
        'D3': "David Spillane",
        'D3B': "Edoardo Bortolato",
    }
    return winter_proposed_team_2_valid


@pytest.fixture(scope='session')
def winter_proposed_team_2_invalid_better_team():
    winter_proposed_team_2_invalid_better_team = {
        'D1': "Tom Brophy",
        'D1B': "Freddie Bracken",
        'D2': "Rico Raymundo",
        'D2B': "Conor Waldron",
        'D3': "David Spillane",
        'D3B': "Edoardo Bortolato",
    }
    return winter_proposed_team_2_invalid_better_team

@pytest.fixture(scope='session')
def winter_proposed_team_7_valid():
    winter_proposed_team_7_valid = {
        'D1': "Kabir Kalia",
        'D1B': "Nitin Swarup",
        'D2': "Max LeBrocquy",
        'D2B': "Matthew Hanrahan",
        'D3': "Ryan McGrath",
        'D3B': "Owen McGuigan",
    }
    return winter_proposed_team_7_valid

@pytest.fixture(scope='session')
def winter_proposed_team_7_invalid_order():
    winter_proposed_team_7_invalid_order = {
        'D1': "Kabir Kalia",
        'D1B': "Nitin Swarup",
        'D2': "Max LeBrocquy",
        'D2B': "Owen McGuigan",
        'D3': "Ryan McGrath",
        'D3B': "Conor O'Leary",
    }
    return winter_proposed_team_7_invalid_order


@pytest.fixture(scope='session')
def winter_proposed_team_3_invalid_order():
    winter_proposed_team_3_invalid_order = {
        'D1': "Ronan O'Brien",
        'D1B': "Adam Casey",
        'D2': "Conor Waldron",
        'D2B': "Mark Cloonan",
        'D3': "Joseph Kelleher",
        'D3B': "Shane Bergin",
    }
    return winter_proposed_team_3_invalid_order

#######################################################################################################################

#@pytest.mark.skip
def test_has_6_unique_reg_players(winter_team_3_df, winter_team_3_subs_and_lower_class_df,
                                  winter_proposed_team_3_valid, winter_proposed_team_3_only_5_players,
                                  winter_proposed_team_3_repeated_player, winter_proposed_team_3_owen):
    '''
    Checks that
    at least 6 players are entered
    all 5 ployers are unique
    all 6 players are on that team, or lower teams or are subs at that class
    '''
    expected_value = True, None
    actual_value = has_6_unique_reg_players(winter_proposed_team_3_valid, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'no player was entered in position D3'
    actual_value = has_6_unique_reg_players(winter_proposed_team_3_only_5_players, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'you entered Conor Waldron twice'
    actual_value = has_6_unique_reg_players(winter_proposed_team_3_repeated_player, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'Owen Casey is not in the list of valid subs or registered teams at or below this class level'
    actual_value = has_6_unique_reg_players(winter_proposed_team_3_owen, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value


#@pytest.mark.skip
def test_winter_lg_doubles_team_and_class_checker(winter_team_3_df, winter_team_3_subs_and_lower_class_df,
                                  winter_team_2_df, winter_team_2_subs_and_lower_class_df,
                                  winter_proposed_team_3_valid, winter_proposed_team_3_invalid_better_class,
                                  winter_proposed_team_3_invalid_better_class2,
                                  winter_proposed_team_2_valid, winter_proposed_team_2_invalid_better_team,
                                  winter_proposed_team_3_invalid_order):
    '''
    Checks that
    you never play a doubles player above someone of a better class
    you never play a doubles player above someone from a higher team
    '''
    expected_value = True, None
    actual_value = winter_lg_doubles_team_and_class_checker(winter_proposed_team_3_valid, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = True, None
    actual_value = winter_lg_doubles_team_and_class_checker(winter_proposed_team_2_valid, winter_team_2_df, winter_team_2_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'Your 1 doubles contains a class 5 player which is better than one of the players on your 2 doubles (class 3)'
    actual_value = winter_lg_doubles_team_and_class_checker(winter_proposed_team_3_invalid_better_class, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'Your 2 doubles contains a class 6 player which is better than one of the players on your 3 doubles (class 3)'
    actual_value = winter_lg_doubles_team_and_class_checker(winter_proposed_team_3_invalid_better_class2, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'Your 2 doubles contains a player registered to team 3 which is better than one of the players on your 3 doubles (registered to team 2)'
    actual_value = winter_lg_doubles_team_and_class_checker(winter_proposed_team_2_invalid_better_team,  winter_team_2_df, winter_team_2_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = True, None
    actual_value = winter_lg_doubles_team_and_class_checker(winter_proposed_team_3_invalid_order, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value


def test_winter_lg_doubles_reg_6_right_order(winter_team_3_df, winter_team_3_subs_and_lower_class_df,
                                             winter_proposed_team_3_valid, winter_proposed_team_3_invalid_wrong_order,
                                             winter_proposed_team_3_invalid_order):
    '''
    Checks that no doubles pairing is playing above a different pairing that played above them before
    '''
    expected_value = True, None
    actual_value = winter_lg_doubles_reg_6_right_order(winter_proposed_team_3_valid, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = False, 'All 6 registered players are playing, but not in the right order'
    actual_value = winter_lg_doubles_reg_6_right_order(winter_proposed_team_3_invalid_wrong_order, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value

    expected_value = True, None
    actual_value = winter_lg_doubles_reg_6_right_order(winter_proposed_team_3_invalid_order, winter_team_3_df, winter_team_3_subs_and_lower_class_df, None)
    assert expected_value == actual_value


def test_winter_lg_doubles_previous_orders(winter_team_3_df, winter_team_3_subs_and_lower_class_df,
                                           winter_team_7_df, winter_team_7_subs_and_lower_class_df,
                                           winter_prev_week3, winter_prev_week4,
                                           winter_proposed_team_3_valid, winter_proposed_team_7_valid,
                                           winter_proposed_team_7_invalid_order, winter_proposed_team_3_invalid_order):
    '''
    Checks that no doubles pairing is playing above a different pairing that played above them before
    '''
    expected_value = True, None
    actual_value = winter_lg_doubles_previous_orders(winter_proposed_team_3_valid, winter_team_3_df, winter_team_3_subs_and_lower_class_df, winter_prev_week3)
    assert expected_value == actual_value

    expected_value = True, None
    actual_value = winter_lg_doubles_previous_orders(winter_proposed_team_7_valid, winter_team_7_df, winter_team_7_subs_and_lower_class_df, winter_prev_week3)
    assert expected_value == actual_value

    expected_value = False, 'Your 2 doubles pairing is illegal as they are playing above a pairing who on a previous week had played higher than they had'
    actual_value = winter_lg_doubles_previous_orders(winter_proposed_team_7_invalid_order, winter_team_7_df, winter_team_7_subs_and_lower_class_df, winter_prev_week3)
    assert expected_value == actual_value

    expected_value = False, 'Your 2 doubles pairing is illegal as they are playing above a pairing who on a previous week had played higher than they had'
    actual_value = winter_lg_doubles_previous_orders(winter_proposed_team_3_invalid_order, winter_team_3_df, winter_team_3_subs_and_lower_class_df, winter_prev_week4)
    assert expected_value == actual_value

