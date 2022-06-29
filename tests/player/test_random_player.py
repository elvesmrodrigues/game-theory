import pytest

from src.player.player import PayoffMatrix, MatchHistory
from src.player.random_player import RandomPlayer

from typing import Dict, List, Optional, Union

from tests.player.conftest import payoff_hawk_dove


PlayerFuncParam = Union[str, PayoffMatrix, Optional[MatchHistory]]


@pytest.fixture(scope="function")
def random_player() -> RandomPlayer:
    return RandomPlayer()


@pytest.fixture(scope="function")
def empty_params() -> Dict[str, PlayerFuncParam]:
    return {
        "game_type": "",
        "adversary_id": "",
        "match_history": None,
        "row_or_col": ""
    }


def test_random_player_one_one(
    payoff_matrix_one_one: PayoffMatrix,
    empty_params: PlayerFuncParam,
    random_player: RandomPlayer
) -> None:

    for _ in range(30):
        assert 0 == random_player.get_action(
            payoff_matrix = payoff_matrix_one_one,
            **empty_params
        )


def test_random_player_one_two(
    payoff_matrix_one_two: PayoffMatrix,
    empty_params: PlayerFuncParam,
    random_player: RandomPlayer
) -> None:

    for _ in range(30):
        assert 0 == random_player.get_action(
            payoff_matrix = payoff_matrix_one_two,
            **empty_params
        )


def test_random_player_two_one(
    payoff_matrix_two_one: PayoffMatrix, 
    empty_params: PlayerFuncParam,
    random_player: RandomPlayer
) -> None:

    for _ in range(30):
        action: int =  random_player.get_action(
            payoff_matrix = payoff_matrix_two_one,
            **empty_params
        )
        assert action in [0,1]


def test_random_player_two_two(
    payoff_matrix_two_two: PayoffMatrix, 
    empty_params: PlayerFuncParam,
    random_player: RandomPlayer
) -> None:

    for _ in range(30):
        action: int =  random_player.get_action(
            payoff_matrix = payoff_matrix_two_two,
            **empty_params
        )
        assert action in [0,1]


def test_random_player_three_two(
    payoff_matrix_three_two: PayoffMatrix, 
    empty_params: PlayerFuncParam,
    random_player: RandomPlayer
) -> None:

    for _ in range(30):
        action: int =  random_player.get_action(
            payoff_matrix = payoff_matrix_three_two,
            **empty_params
        )
        assert action in [0,1,2]

def test_random_player_three_three(
    payoff_matrix_three_three: PayoffMatrix, 
    empty_params: PlayerFuncParam,
    random_player: RandomPlayer
) -> None:

    for _ in range(30):
        action: int =  random_player.get_action(
            payoff_matrix = payoff_matrix_three_three,
            **empty_params
        )
        assert action in [0,1,2]
