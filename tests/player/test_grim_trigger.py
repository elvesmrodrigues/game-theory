import pytest

from src.player.player import PayoffMatrix, MatchHistory
from src.player.grim_trigger import Action, GrimTrigger

from typing import Dict, Optional, Union


PlayerFuncParam = Union[str, PayoffMatrix, Optional[MatchHistory]]


@pytest.fixture(scope="function")
def grim_trigger() -> GrimTrigger:
    return GrimTrigger()


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


def test_grim_trigger_all_empty(
    empty_params_payoff_also: PlayerFuncParam,
    empty_match_history: PlayerFuncParam,
    grim_trigger: GrimTrigger
) -> None:

    assert Action.COOPERATE.value == grim_trigger.get_action(
        match_history = empty_match_history,
        **empty_params_payoff_also
    )


def test_grim_trigger_empty_payoffs_both_coop(
    empty_params_payoff_also: PlayerFuncParam,
    both_cooperate_last_match: PlayerFuncParam,
    grim_trigger: GrimTrigger
) -> None:

    for match_history in both_cooperate_last_match:
        assert Action.COOPERATE.value == grim_trigger.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_grim_trigger_empty_payoffs_adv_defect(
    empty_params_payoff_also: PlayerFuncParam,
    adv_defect_last_match: PlayerFuncParam,
    grim_trigger: GrimTrigger
) -> None:

    for match_history in adv_defect_last_match:
        assert Action.DEFECT.value == grim_trigger.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_grim_trigger_empty_payoffs_defect(
    empty_params_payoff_also: PlayerFuncParam,
    defect_last_match: PlayerFuncParam,
    grim_trigger: GrimTrigger
) -> None:

    for match_history in defect_last_match:
        assert Action.DEFECT.value == grim_trigger.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_grim_trigger_empty_payoffs_both_coop(
    empty_params_payoff_also: PlayerFuncParam,
    both_cooperate_last_match: PlayerFuncParam,
    grim_trigger: GrimTrigger
) -> None:

    for match_history in both_cooperate_last_match:
        assert Action.COOPERATE.value == grim_trigger.get_action(
            match_history = match_history,
            **empty_params_payoff_also
        )


def test_grim_trigger_arbitrary_matrices_adv_defect(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    adv_defect_last_match: PlayerFuncParam,
    grim_trigger: GrimTrigger
) -> None:

    for match_history in adv_defect_last_match:
        for payoff_matrix in arbitrary_payoff_matrices:
            assert Action.DEFECT.value == grim_trigger.get_action(
                payoff_matrix = payoff_matrix,
                match_history = match_history,
                **empty_params
            )


def test_grim_trigger_arbitrary_matrices_defect(
    arbitrary_payoff_matrices: PayoffMatrix,
    empty_params: PlayerFuncParam,
    defect_last_match: PlayerFuncParam,
    grim_trigger: GrimTrigger
) -> None:

    for match_history in defect_last_match:
        for payoff_matrix in arbitrary_payoff_matrices:
            assert Action.DEFECT.value == grim_trigger.get_action(
                payoff_matrix = payoff_matrix,
                match_history = match_history,
                **empty_params
            )