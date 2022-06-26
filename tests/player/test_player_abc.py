import pytest
from src.player.player import Player

from typing import Tuple, Dict, Union

PlayerFuncParam = Union[str, Tuple[str], Dict[str, Dict[str, Union[float, int]]]]


class EmptyClass (Player):
    
    
    def get_action(self, game_type: str, 
                        adversary_id: str,
                        available_actions: Tuple[str], 
                        adversary_available_actions: Tuple[str], 
                        payoff_matrix: Dict[str, Dict[str, Union[float, int]]]) -> str:
                        
        return ""


@pytest.fixture(scope="function")
def empty_class() -> EmptyClass:
    return EmptyClass()


@pytest.fixture(scope="function")
def empty_get_action_params() -> Dict[str, PlayerFuncParam]:
    return {
        "game_type": "",
        "adversary_id": "",
        "available_actions": tuple(),
        "adversary_available_actions": tuple(),
        "payoff_matrix": dict()
    }


class TestEmpty:

    def test_all_is_empty(
        self, 
        empty_class: EmptyClass, 
        empty_get_action_params: Dict[str, PlayerFuncParam]
    ):
        
        assert empty_class.name == ""
        assert empty_class.memory == dict()
        assert empty_class.get_action(**empty_get_action_params) == ""
