import pytest

from src.player.player import PayoffMatrix, MatchHistory
from src.player.tit_for_tat import Action, TitForTat

from typing import Dict, Optional, Union


PlayerFuncParam = Union[str, PayoffMatrix, Optional[MatchHistory]]


@pytest.fixture(scope="function")
def tit_for_tat() -> TitForTat:
    return TitForTat()


@pytest.fixture(scope="function")
def empty_params() -> Dict[str, PlayerFuncParam]:
    return {
        "game_type": "",
        "adversary_id": "",
        "row_or_col": "all"
    }


@pytest.fixture(scope="function")
def empty_params_payoff_also() -> Dict[str, PlayerFuncParam]:
    return {
        "game_type": "",
        "payoff_matrix": None,
        "adversary_id": "",
        "row_or_col": "all"
    }


def test_tit_for_tat_all_empty(
    empty_params_payoff_also: PlayerFuncParam,
    empty_match_history: PlayerFuncParam,
    tit_for_tat: TitForTat
) -> None:

    assert Action.COOPERATE.value == tit_for_tat.get_action(
        match_history = empty_match_history,
        **empty_params_payoff_also
    )


def test_tit_for_tat_empty_payoffs_cooperate(
    empty_params_payoff_also: PlayerFuncParam,
    adv_cooperate_last_match: PlayerFuncParam,
    tit_for_tat: TitForTat
) -> None:

    for match_history in adv_cooperate_last_match:
        assert Action.COOPERATE.value == tit_for_tat.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_tit_for_tat_empty_payoffs_defect(
    empty_params_payoff_also: PlayerFuncParam,
    adv_defect_last_match: PlayerFuncParam,
    tit_for_tat: TitForTat
) -> None:

    for match_history in adv_defect_last_match:
        assert Action.DEFECT.value == tit_for_tat.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_tit_for_tat_arbitrary_matrices_first_match(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    empty_match_history: PlayerFuncParam,
    tit_for_tat: TitForTat
) -> None:

    for payoff_matrix in arbitrary_payoff_matrices:
        assert Action.COOPERATE.value == tit_for_tat.get_action(
            payoff_matrix = payoff_matrix,
            match_history = empty_match_history,
            **empty_params
        )


def test_tit_for_tat_arbitrary_matrices_cooperate(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    adv_cooperate_last_match: PlayerFuncParam,
    tit_for_tat: TitForTat
) -> None:

    for match_history in adv_cooperate_last_match:
        for payoff_matrix in arbitrary_payoff_matrices:
            assert Action.COOPERATE.value == tit_for_tat.get_action(
                payoff_matrix = payoff_matrix,
                match_history = match_history,
                **empty_params
            )


def test_tit_for_tat_arbitrary_matrices_defect(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    adv_defect_last_match: PlayerFuncParam,
    tit_for_tat: TitForTat
) -> None:

    for match_history in adv_defect_last_match:
        for payoff_matrix in arbitrary_payoff_matrices:
            assert Action.DEFECT.value == tit_for_tat.get_action(
                payoff_matrix = payoff_matrix,
                match_history = match_history,
                **empty_params
            )