from numpy import empty_like
import pytest
from src.player.player import MatchHistoryKey, Player, PayoffMatrix, MatchHistory

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


#_______________________________________
#_______________________________________
#_______________________________________


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

class TestInitiallyEmpty:

    def test_all_is_empty(
        self,
        empty_class: EmptyClass, 
        empty_params: Dict[str, PlayerFuncParam]
    ) -> None:
        
        assert empty_class.name == ""
        assert empty_class.match_history == dict()
        assert empty_class.get_action(**empty_params) is None
        assert empty_class.get_match_history(0, "") is None
        assert empty_class.get_match_history(1, "l") is None


    def test_update_symmetric(
        self,
        empty_class: EmptyClass
    ) -> None:

        game_symmetric = True
        game_id = 0
        adversary_id = "adv"
        row_or_col = "row"
        action = 0
        adversary_action = 1

        empty_class.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        key: MatchHistoryKey = (game_id, adversary_id)
        assert len(empty_class.match_history.keys()) == 1
        assert key in empty_class.match_history
        
        match_history: MatchHistory = empty_class.get_match_history(game_id, adversary_id)
        assert match_history["all"] == [(action, adversary_action)]
        assert match_history["row"] is match_history["all"]
        assert match_history["col"] is match_history["all"]


    def test_update_asymmetric(
        self,
        empty_class: EmptyClass
    ) -> None:

        game_symmetric = False
        game_id = 0
        adversary_id = "adv"
        row_or_col = "row"
        action = 0
        adversary_action = 1

        empty_class.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        key: MatchHistoryKey = (game_id, adversary_id)
        assert len(empty_class.match_history.keys()) == 1
        assert key in empty_class.match_history
        
        match_history: MatchHistory = empty_class.get_match_history(game_id, adversary_id)
        assert match_history["all"] == [(action, adversary_action)]
        assert match_history["row"] == [(action, adversary_action)]
        assert match_history["col"] == []

        row_or_col = "col"

        empty_class.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = adversary_action,
            adversary_action = action
        )

        assert len(empty_class.match_history.keys()) == 1

        match_history: MatchHistory = empty_class.get_match_history(game_id, adversary_id)
        assert match_history["all"] == [(action, adversary_action), (adversary_action, action)]
        assert match_history["row"] == [(action, adversary_action)]
        assert match_history["col"] == [(adversary_action, action)]


#_______________________________________
#_______________________________________
#_______________________________________


@pytest.fixture(scope="function")
def empty_class_one_match_symmetric() -> EmptyClass:

    empty_class = EmptyClass()

    game_symmetric = True
    game_id = 0
    adversary_id = "adv"
    row_or_col = "row"
    action = 0
    adversary_action = 1

    empty_class.update_match_history(
        game_symmetric = game_symmetric,
        game_id = game_id,
        adversary_id = adversary_id,
        row_or_col = row_or_col,
        action = action,
        adversary_action = adversary_action
    )

    return empty_class


class TestThereWasMatchSymmetric:


    def test_update_same_adversary(
        self,
        empty_class_one_match_symmetric: EmptyClass
    ) -> None:

        game_symmetric = True
        game_id = 0
        adversary_id = "adv"
        row_or_col = "col"
        action = 2
        adversary_action = 3

        match_history_original: MatchHistory = empty_class_one_match_symmetric.get_match_history(
            game_id, adversary_id
        )

        empty_class_one_match_symmetric.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        key: MatchHistoryKey = (game_id, adversary_id)
        assert len(empty_class_one_match_symmetric.match_history.keys()) == 1
        assert key in empty_class_one_match_symmetric.match_history
        
        match_history: MatchHistory = empty_class_one_match_symmetric.get_match_history(
            game_id, adversary_id
        )
        assert match_history_original["all"] is match_history["all"]
        assert match_history["all"] == [(0, 1), (action, adversary_action)]
        assert match_history["row"] is match_history["all"]
        assert match_history["col"] is match_history["all"]


    def test_update_other_adversary(
        self,
        empty_class_one_match_symmetric: EmptyClass
    ) -> None:

        game_symmetric = True
        game_id = 0
        adversary_id = "adv_2"
        row_or_col = "row"
        action = 0
        adversary_action = 1

        empty_class_one_match_symmetric.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        key: MatchHistoryKey = (game_id, "adv")
        assert len(empty_class_one_match_symmetric.match_history.keys()) == 2
        assert key in empty_class_one_match_symmetric.match_history
        
        match_history_adv: MatchHistory = empty_class_one_match_symmetric.get_match_history(
            game_id, "adv"
        )
        assert match_history_adv["all"] == [(0, 1)]
        assert match_history_adv["row"] is match_history_adv["all"]
        assert match_history_adv["col"] is match_history_adv["all"]


        key: MatchHistoryKey = (game_id, adversary_id)
        assert len(empty_class_one_match_symmetric.match_history.keys()) == 2
        assert key in empty_class_one_match_symmetric.match_history
        
        match_history_adv_2: MatchHistory = empty_class_one_match_symmetric.get_match_history(
            game_id, adversary_id
        )
        assert match_history_adv_2 is not match_history_adv
        assert match_history_adv_2["all"] == [(action, adversary_action)]
        assert match_history_adv_2["row"] is match_history_adv_2["all"]
        assert match_history_adv_2["col"] is match_history_adv_2["all"]

    
    def test_update_other_game(
        self,
        empty_class_one_match_symmetric: EmptyClass
    ) -> None:

        game_symmetric = True
        game_id = 1
        adversary_id = "adv"
        row_or_col = "row"
        action = 0
        adversary_action = 1

        empty_class_one_match_symmetric.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        key: MatchHistoryKey = (0, adversary_id)
        assert len(empty_class_one_match_symmetric.match_history.keys()) == 2
        assert key in empty_class_one_match_symmetric.match_history
        
        match_history_adv: MatchHistory = empty_class_one_match_symmetric.get_match_history(
            0, adversary_id
        )
        assert match_history_adv["all"] == [(0, 1)]
        assert match_history_adv["row"] is match_history_adv["all"]
        assert match_history_adv["col"] is match_history_adv["all"]


        key: MatchHistoryKey = (game_id, adversary_id)
        assert len(empty_class_one_match_symmetric.match_history.keys()) == 2
        assert key in empty_class_one_match_symmetric.match_history
        
        match_history_adv_2: MatchHistory = empty_class_one_match_symmetric.get_match_history(
            game_id, adversary_id
        )
        assert match_history_adv_2 is not match_history_adv
        assert match_history_adv_2["all"] == [(action, adversary_action)]
        assert match_history_adv_2["row"] is match_history_adv_2["all"]
        assert match_history_adv_2["col"] is match_history_adv_2["all"]

#_______________________________________
#_______________________________________
#_______________________________________


@pytest.fixture(scope="function")
def empty_class_one_match_asymmetric() -> EmptyClass:

    empty_class = EmptyClass()

    game_symmetric = False
    game_id = 0
    adversary_id = "adv"
    row_or_col = "row"
    action = 0
    adversary_action = 1

    empty_class.update_match_history(
        game_symmetric = game_symmetric,
        game_id = game_id,
        adversary_id = adversary_id,
        row_or_col = row_or_col,
        action = action,
        adversary_action = adversary_action
    )

    return empty_class


class TestThereWasMatchAsymmetric:


    def test_update_same_adversary_same_position(
        self,
        empty_class_one_match_asymmetric: EmptyClass
    ) -> None:

        game_symmetric = False
        game_id = 0
        adversary_id = "adv"
        row_or_col = "row"
        action = 2
        adversary_action = 3

        match_history_original: MatchHistory = empty_class_one_match_asymmetric.get_match_history(
            game_id, adversary_id
        )

        empty_class_one_match_asymmetric.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        key: MatchHistoryKey = (game_id, adversary_id) 
        assert len(empty_class_one_match_asymmetric.match_history.keys()) == 1
        assert key in empty_class_one_match_asymmetric.match_history

        match_history: MatchHistory = empty_class_one_match_asymmetric.get_match_history(
            game_id, adversary_id
        )
        assert match_history_original["all"] is match_history["all"]
        assert match_history_original["row"] is match_history["row"]
        assert match_history_original["col"] is match_history["col"]

        assert match_history["all"] == [(0, 1), (action, adversary_action)]
        assert match_history["row"] == [(0, 1), (action, adversary_action)]
        assert match_history["col"] == []


    def test_update_same_adversary_other_position(
        self,
        empty_class_one_match_asymmetric: EmptyClass
    ) -> None:

        game_symmetric = False
        game_id = 0
        adversary_id = "adv"
        row_or_col = "col"
        action = 2
        adversary_action = 3

        match_history_original: MatchHistory = empty_class_one_match_asymmetric.get_match_history(
            game_id, adversary_id
        )

        empty_class_one_match_asymmetric.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        key: MatchHistoryKey = (game_id, adversary_id)
        assert len(empty_class_one_match_asymmetric.match_history.keys()) == 1
        assert key in empty_class_one_match_asymmetric.match_history

        match_history: MatchHistory = empty_class_one_match_asymmetric.get_match_history(
            game_id, adversary_id
        )

        assert match_history_original["all"] is match_history["all"]
        assert match_history_original["row"] is match_history["row"]
        assert match_history_original["col"] is match_history["col"]

        assert match_history["all"] == [(0, 1), (action, adversary_action)]
        assert match_history["row"] == [(0, 1)]
        assert match_history["col"] == [(action, adversary_action)]


    def test_update_other_adversary(
        self,
        empty_class_one_match_asymmetric: EmptyClass
    ) -> None:

        game_symmetric = False
        game_id = 0
        adversary_id = "adv_2"
        row_or_col = "col"
        action = 0
        adversary_action = 1

        empty_class_one_match_asymmetric.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        key: MatchHistoryKey = (game_id, "adv")
        assert len(empty_class_one_match_asymmetric.match_history.keys()) == 2
        assert key in empty_class_one_match_asymmetric.match_history
        
        match_history_adv: MatchHistory = empty_class_one_match_asymmetric.get_match_history(
            game_id, "adv"
        )
        assert match_history_adv["all"] == [(0, 1)]
        assert match_history_adv["row"] == [(0, 1)]
        assert match_history_adv["col"] == []


        key: MatchHistoryKey = (game_id, adversary_id)
        assert len(empty_class_one_match_asymmetric.match_history.keys()) == 2
        assert key in empty_class_one_match_asymmetric.match_history
        
        match_history_adv_2: MatchHistory = empty_class_one_match_asymmetric.get_match_history(
            game_id, adversary_id
        )
        assert match_history_adv_2 is not match_history_adv
        assert match_history_adv_2["all"] == [(action, adversary_action)]
        assert match_history_adv_2["row"] == []
        assert match_history_adv_2["col"] == [(action, adversary_action)]


    def test_update_two_matches_adversary(
        self,
        empty_class_one_match_asymmetric: EmptyClass
    ) -> None:

        game_symmetric = False
        game_id = 0
        adversary_id = "adv_2"
        row_or_col = "col"
        action = 0
        adversary_action = 1

        empty_class_one_match_asymmetric.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action,
            adversary_action = adversary_action
        )

        row_or_col = "row"
        action_two = 2
        adversary_action_two = 3

        empty_class_one_match_asymmetric.update_match_history(
            game_symmetric = game_symmetric,
            game_id = game_id,
            adversary_id = adversary_id,
            row_or_col = row_or_col,
            action = action_two,
            adversary_action = adversary_action_two
        )

        key: MatchHistoryKey = (game_id, "adv")
        assert len(empty_class_one_match_asymmetric.match_history.keys()) == 2
        assert key in empty_class_one_match_asymmetric.match_history
        
        match_history_adv: MatchHistory = empty_class_one_match_asymmetric.get_match_history(
            game_id, "adv"
        )
        assert match_history_adv["all"] == [(0, 1)]
        assert match_history_adv["row"] == [(0, 1)]
        assert match_history_adv["col"] == []


        key: MatchHistoryKey = (game_id, adversary_id)
        assert len(empty_class_one_match_asymmetric.match_history.keys()) == 2
        assert key in empty_class_one_match_asymmetric.match_history
        
        match_history_adv_2: MatchHistory = empty_class_one_match_asymmetric.get_match_history(
            game_id, adversary_id
        )
        assert match_history_adv_2 is not match_history_adv
        assert match_history_adv_2["all"] == [(action, adversary_action), (action_two, adversary_action_two)]
        assert match_history_adv_2["row"] == [(action_two, adversary_action_two)]
        assert match_history_adv_2["col"] == [(action, adversary_action)]