from enum import Enum
from typing import Optional
from typing_extensions import Literal
from src.player.player import Player, MatchHistory, PayoffMatrix


class Action(Enum):
    COOPERATE: int = 0
    DEFECT: int = 1


class GrimTrigger(Player):


    def __init__(self) -> None:
        self.name = "Grim Trigger"
        self.match_history = dict()


    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:

        desired_col: str = row_or_col

        if match_history is None or match_history[desired_col] == []:
            return Action.COOPERATE.value
        
        previous_action, adversary_previous_action = match_history[desired_col][-1]

        defected = (previous_action == Action.DEFECT.value)
        adv_defected = (adversary_previous_action == Action.DEFECT.value)

        if defected or adv_defected:
            return Action.DEFECT.value
        
        return Action.COOPERATE.value