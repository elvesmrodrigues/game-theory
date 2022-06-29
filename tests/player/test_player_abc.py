import pytest
from src.player.player import Player, PayoffMatrix, MatchHistory

from typing import Tuple, Dict, Union, Optional

PlayerFuncParam = Union[str, Tuple[str], Dict[str, Dict[str, Union[None, float, int, Dict]]]]


class EmptyClass (Player):
    
    
    def __init__(self) -> None:
        self.name = ""
        self.match_history = dict()


    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: str
    ) -> int:
                        
        return None


@pytest.fixture(scope="function")
def empty_class() -> EmptyClass:
    return EmptyClass()


@pytest.fixture(scope="function")
def empty_params() -> Dict[str, PlayerFuncParam]:
    return {
        "game_type": "",
        "adversary_id": "",
        "payoff_matrix": tuple(),
        "match_history": None,
        "row_or_col": ""
    }


def test_all_is_empty(
    empty_class: EmptyClass, 
    empty_params: Dict[str, PlayerFuncParam]
):
    
    assert empty_class.name == ""
    assert empty_class.match_history == dict()
    assert empty_class.get_action(**empty_params) is None
