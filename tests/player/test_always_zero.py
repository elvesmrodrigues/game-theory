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


def test_always_zero_arbitraty_matrices(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    always_zero: AlwaysActionZero
) -> None:

    for payoff_matrix in arbitrary_payoff_matrices:
        assert 0 == always_zero.get_action(
            payoff_matrix = payoff_matrix,
            **empty_params
        )


def test_always_zero_common_two_by_two(
    common_two_by_two_games: PayoffMatrix,
    empty_params: PlayerFuncParam,
    always_zero: AlwaysActionZero
) -> None:

    for payoff_matrix in common_two_by_two_games:
        assert 0 == always_zero.get_action(
            payoff_matrix = payoff_matrix,
            **empty_params
        )
