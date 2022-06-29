import pytest

from src.player.player import PayoffMatrix, MatchHistory
from src.player.always_action_zero import AlwaysActionZero

from typing import Dict, Optional, Union


PlayerFuncParam = Union[str, PayoffMatrix, Optional[MatchHistory]]


@pytest.fixture(scope="function")
def always_zero() -> AlwaysActionZero:
    return AlwaysActionZero()


@pytest.fixture(scope="function")
def empty_params() -> Dict[str, PlayerFuncParam]:
    return {
        "game_type": "",
        "adversary_id": "",
        "match_history": None,
        "row_or_col": ""
    }


def test_always_zero_one_one(
    payoff_matrix_one_one: PayoffMatrix,
    empty_params: PlayerFuncParam,
    always_zero: AlwaysActionZero
) -> None:

    for _ in range(30):
        assert 0 == always_zero.get_action(
            payoff_matrix = payoff_matrix_one_one,
            **empty_params
        )


def test_always_zero_one_two(
    payoff_matrix_one_two: PayoffMatrix,
    empty_params: PlayerFuncParam,
    always_zero: AlwaysActionZero
) -> None:

    for _ in range(30):
        assert 0 == always_zero.get_action(
            payoff_matrix = payoff_matrix_one_two,
            **empty_params
        )


def test_always_zero_two_one(
    payoff_matrix_two_one: PayoffMatrix, 
    empty_params: PlayerFuncParam,
    always_zero: AlwaysActionZero
) -> None:

    for _ in range(30):
        assert 0 == always_zero.get_action(
            payoff_matrix = payoff_matrix_two_one,
            **empty_params
        )


def test_always_zero_two_two(
    payoff_matrix_two_two: PayoffMatrix, 
    empty_params: PlayerFuncParam,
    always_zero: AlwaysActionZero
) -> None:

    for _ in range(30):
        assert 0 == always_zero.get_action(
            payoff_matrix = payoff_matrix_two_two,
            **empty_params
        )

def test_always_zero_three_two(
    payoff_matrix_three_two: PayoffMatrix, 
    empty_params: PlayerFuncParam,
    always_zero: AlwaysActionZero
) -> None:

    for _ in range(30):
        assert 0 == always_zero.get_action(
            payoff_matrix = payoff_matrix_three_two,
            **empty_params
        )

def test_always_zero_three_three(
    payoff_matrix_three_three: PayoffMatrix, 
    empty_params: PlayerFuncParam,
    always_zero: AlwaysActionZero
) -> None:

    for _ in range(30):
        assert 0 == always_zero.get_action(
            payoff_matrix = payoff_matrix_three_three,
            **empty_params
        )