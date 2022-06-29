from codecs import ascii_encode
import pytest

from src.player.player import PayoffMatrix, MatchHistory
from src.player.random_player import RandomPlayer

from typing import Dict, List, Optional, Union


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


def test_random_player_arbitraty_matrices(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    random_player: RandomPlayer
) -> None:

    for payoff_matrix in arbitrary_payoff_matrices[:2]:
        for _ in range(30):
            assert 0 == random_player.get_action(
                payoff_matrix = payoff_matrix,
                **empty_params
            )

    for payoff_matrix in arbitrary_payoff_matrices[2:4]:
        for _ in range(30):
            action: int = random_player.get_action(
                payoff_matrix = payoff_matrix,
                **empty_params
            )
            assert action in [0,1]

    for payoff_matrix in arbitrary_payoff_matrices[4:]:
        for _ in range(30):
            action: int = random_player.get_action(
                payoff_matrix = payoff_matrix,
                **empty_params
            )
            assert action in [0,1,2]


def test_random_player_common_two_by_two(
    common_two_by_two_games: PayoffMatrix,
    empty_params: PlayerFuncParam,
    random_player: RandomPlayer
) -> None:

    for payoff_matrix in common_two_by_two_games:
        for _ in range(30):
            action: int = random_player.get_action(
                payoff_matrix = payoff_matrix,
                **empty_params
            )
            assert action in [0,1]
