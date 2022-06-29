import pytest

from src.player.player import PayoffMatrix, MatchHistory
from src.player.forgiving_tit_for_tat import Action, ForgivingTitForTat

from typing import Dict, Optional, Union


PlayerFuncParam = Union[str, PayoffMatrix, Optional[MatchHistory]]


@pytest.fixture(scope="function")
def forgiving_tit_for_tat() -> ForgivingTitForTat:
    return ForgivingTitForTat()


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


def test_forgiving_tit_for_tat_all_empty(
    empty_params_payoff_also: PlayerFuncParam,
    empty_match_history: PlayerFuncParam,
    forgiving_tit_for_tat: ForgivingTitForTat
) -> None:

    assert Action.COOPERATE.value == forgiving_tit_for_tat.get_action(
        match_history = empty_match_history,
        **empty_params_payoff_also
    )


def test_forgiving_tit_for_tat_empty_payoffs_both_coop(
    empty_params_payoff_also: PlayerFuncParam,
    both_cooperate_last_match: PlayerFuncParam,
    forgiving_tit_for_tat: ForgivingTitForTat
) -> None:

    for match_history in both_cooperate_last_match:
        assert Action.COOPERATE.value == forgiving_tit_for_tat.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_forgiving_tit_for_tat_empty_payoffs_coop_defect(
    empty_params_payoff_also: PlayerFuncParam,
    coop_defect_last_match: PlayerFuncParam,
    forgiving_tit_for_tat: ForgivingTitForTat
) -> None:

    for match_history in coop_defect_last_match:
        assert Action.DEFECT.value == forgiving_tit_for_tat.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_forgiving_tit_for_tat_empty_payoffs_defect(
    empty_params_payoff_also: PlayerFuncParam,
    defect_last_match: PlayerFuncParam,
    forgiving_tit_for_tat: ForgivingTitForTat
) -> None:

    for match_history in defect_last_match:
        assert Action.COOPERATE.value == forgiving_tit_for_tat.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_forgiving_tit_for_tat_arbitrary_matrices_first_match(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    empty_match_history: PlayerFuncParam,
    forgiving_tit_for_tat: ForgivingTitForTat
) -> None:

    for payoff_matrix in arbitrary_payoff_matrices:
        assert Action.COOPERATE.value == forgiving_tit_for_tat.get_action(
            payoff_matrix = payoff_matrix,
            match_history = empty_match_history,
            **empty_params
        )


def test_forgiving_tit_for_tat_arbitrary_matrices_both_coop(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    both_cooperate_last_match: PlayerFuncParam,
    forgiving_tit_for_tat: ForgivingTitForTat
) -> None:

    for match_history in both_cooperate_last_match:
        for payoff_matrix in arbitrary_payoff_matrices:
            assert Action.COOPERATE.value == forgiving_tit_for_tat.get_action(
                payoff_matrix = payoff_matrix,
                match_history = match_history,
                **empty_params
            )


def test_forgiving_tit_for_tat_arbitrary_matrices_coop_defect(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    coop_defect_last_match: PlayerFuncParam,
    forgiving_tit_for_tat: ForgivingTitForTat
) -> None:

    for match_history in coop_defect_last_match:
        for payoff_matrix in arbitrary_payoff_matrices:
            assert Action.DEFECT.value == forgiving_tit_for_tat.get_action(
                payoff_matrix = payoff_matrix,
                match_history = match_history,
                **empty_params
            )


def test_forgiving_tit_for_tat_arbitrary_matrices_defect(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    defect_last_match: PlayerFuncParam,
    forgiving_tit_for_tat: ForgivingTitForTat
) -> None:

    for match_history in defect_last_match:
        for payoff_matrix in arbitrary_payoff_matrices:
            assert Action.COOPERATE.value == forgiving_tit_for_tat.get_action(
                payoff_matrix = payoff_matrix,
                match_history = match_history,
                **empty_params
            )