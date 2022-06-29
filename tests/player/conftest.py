import pytest
from enum import Enum

class Action(Enum):
    COOPERATE: int = 0
    DEFECT: int = 1

#_______________________________

        # PAYOFF MATRICES

#_______________________________


@pytest.fixture(scope="session")
def arbitrary_payoff_matrices():
    return (
        (((1,2),),),
        (((1,2), (2,1)),),
        (((1,2),),((2,3),)),
        (((1,2), (2,1)),((2,3), (3,4))),
        (((1,2), (2,1)),((2,3), (3,4)),((2,3), (3,4))),
        (((1,2), (2,1), (5,6)),((2,3), (3,4), (7,3)),((2,3), (3,4), (8,2)))
    )

@pytest.fixture(scope="session")
def common_two_by_two_games():
    return (
        (((3,3), (0,5)),((5,0), (1,1))), # prisoner's dilemma
        (((5,5), (0,3)),((3,0), (3,3))), # stag hunt
        (((3,3), (1,5)),((5,1), (0,0)))  # hawk dove
    )

#_______________________________

        # MATCH HISTORY

#_______________________________

@pytest.fixture(scope="function")
def empty_match_history():
    return None

@pytest.fixture(scope="function")
def cooperate_last_match():
    return [
        {"all": [(Action.COOPERATE.value, None)]},
        {"all": [(None, None), (None, None), (Action.COOPERATE.value, None)]}
    ]

@pytest.fixture(scope="function")
def adv_cooperate_last_match():
    return [
        {"all": [(None, Action.COOPERATE.value)]},
        {"all": [(None, None), (None, None), (None, Action.COOPERATE.value)]}
    ]

@pytest.fixture(scope="function")
def defect_last_match():
    return [
        {"all": [(Action.DEFECT.value, None)]},
        {"all": [(None, None), (None, None), (Action.DEFECT.value, None)]}
    ]

@pytest.fixture(scope="function")
def adv_defect_last_match():
    return [
        {"all": [(None, Action.DEFECT.value)]},
        {"all": [(None, None), (None, None), (None, Action.DEFECT.value)]}
    ]

@pytest.fixture(scope="function")
def both_cooperate_last_match():
    return [
        {"all": [(Action.COOPERATE.value, Action.COOPERATE.value)]},
        {"all": [(None, None), (None, None), (Action.COOPERATE.value, Action.COOPERATE.value)]}
    ]

@pytest.fixture(scope="function")
def coop_defect_last_match():
    return [
        {"all": [(Action.COOPERATE.value, Action.DEFECT.value)]},
        {"all": [(None, None), (None, None), (Action.COOPERATE.value, Action.DEFECT.value)]}
    ]