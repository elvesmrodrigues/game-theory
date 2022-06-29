import pytest

@pytest.fixture(scope="function")
def payoff_matrix_one_one():
    return (((1,2),),)

@pytest.fixture(scope="function")
def payoff_matrix_one_two():
    return (((1,2), (2,1)),)

@pytest.fixture(scope="function")
def payoff_matrix_two_one():
    return (
        ((1,2),),
        ((2,3),)
    )

@pytest.fixture(scope="function")
def payoff_matrix_two_two():
    return (
        ((1,2), (2,1)),
        ((2,3), (3,4))
    )

@pytest.fixture(scope="function")
def payoff_matrix_three_two():
    return (
        ((1,2), (2,1)),
        ((2,3), (3,4)),
        ((2,3), (3,4))
    )

@pytest.fixture(scope="function")
def payoff_matrix_three_three():
    return (
        ((1,2), (2,1), (5,6)),
        ((2,3), (3,4), (7,3)),
        ((2,3), (3,4), (8,2))
    )

@pytest.fixture(scope="function")
def payoff_prisioners_dilemma():
    return (
        ((3,3), (0,5)),
        ((5,0), (1,1))
    )

@pytest.fixture(scope="function")
def payoff_stag_hunt():
    return (
        ((5,5), (0,3)),
        ((3,0), (3,3))
    )

@pytest.fixture(scope="function")
def payoff_hawk_dove():
    return (
        ((3,3), (1,5)),
        ((5,1), (0,0))
    )

