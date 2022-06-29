import pytest
from enum import Enum

class Action(Enum):
    COOPERATE = 0
    DEFECT = 1

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

