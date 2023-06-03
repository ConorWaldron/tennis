'run with pytest test.py -vv'

import pytest
import pandas as pd

from tennis.eligibility_rules import has_7_unique_reg_players, team_played_before, singles_right_order, doubles_right_order, team_tied


# Define the fixtures

@pytest.fixture(scope='session')
def team_4_df():
    team_df = pd.read_csv('teams_test.csv')
    team_4_df = team_df[team_df['Team'] == 4]
    return team_4_df


@pytest.fixture(scope='session')
def team_4_subs_and_lower_class_df():
    team_df = pd.read_csv('teams_test.csv')
    team_4_df = team_df[team_df['Team'] == 4]
    lower_teams = team_df[team_df['Team'] > 4][['Name', 'Class']].rename(columns={'Class': 'Lowest_Class'})

    subs_df = pd.read_csv('subs_test.csv')
    relevant_subs = subs_df[subs_df['Lowest_Class'] >= 4]
    team_of_interest = team_4_df[['Name', 'Class']].rename(columns={'Class': 'Lowest_Class'})
    team_4_subs_and_lower_class_df = pd.concat([relevant_subs, lower_teams, team_of_interest], ignore_index=True)
    return team_4_subs_and_lower_class_df


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
def proposed_team_6_players():
    proposed_team_6_players = {
        'S1':"Adam Escalate",
        'S3': "Shane Bergin",
        'D1': "PETER CLOONAN",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return proposed_team_6_players


@pytest.fixture(scope='session')
def proposed_team_same_player_twice():
    proposed_team_same_player_twice = {
        'S1':"Adam Escalate",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "PETER CLOONAN",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Conor Waldron",
    }
    return proposed_team_same_player_twice


@pytest.fixture(scope='session')
def proposed_team_not_valid_sub():
    proposed_team_not_valid_sub = {
        'S1': "Adam Escalate",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "PETER CLOONAN",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Owen Casey",
    }
    return proposed_team_not_valid_sub


@pytest.fixture(scope='session')
def valid_team_4():
    valid_team_4 = {
        'S1':"Adam Escalate",
        'S2': "Conor Waldron",
        'S3': "Shane Bergin",
        'D1': "PETER CLOONAN",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Andrew Synnott",
    }
    return valid_team_4


@pytest.fixture(scope='session')
def reg_team_4_wrong_order():
    reg_team_4_wrong_order = {
        'S1':"Adam Escalate",
        'S2': "Conor Waldron",
        'S3': "Andrew Synnott",
        'D1': "PETER CLOONAN",
        'D1B': "Bernard O'Sullivan",
        'D2': "Peter Morgan",
        'D2B': "Shane Bergin",
    }
    return reg_team_4_wrong_order

@pytest.fixture(scope='session')
def team_4_same_as_week2_wrong_order():
    team_4_same_as_week2_wrong_order = {
        'S1': "Adam Escalate",
        'S2': "James Fagan",
        'S3': "James Doyle",
        'D1': "Martin Henihan",
        'D1B': "Peter Morgan",
        'D2': "Russell Boland",
        'D2B': "Peter Johnston",
    }
    return team_4_same_as_week2_wrong_order


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
def test_singles_right_order():
    pass


# @pytest.mark.skip
def test_doubles_right_order():
    pass


# @pytest.mark.skip
def test_team_tied():
    pass
