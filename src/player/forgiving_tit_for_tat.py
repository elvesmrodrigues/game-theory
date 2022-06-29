from enum import Enum
from typing import Optional
from src.player.player import Player, MatchHistory, PayoffMatrix


class Action(Enum):
    COOPERATE: int = 0
    DEFECT: int = 1


class ForgivingTitForTat(Player):


    def __init__(self) -> None:
        self.name = "Forgiving Tit for Tat"
        self.match_history = dict()


    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: str
    ) -> int:

        if match_history is None:
            return Action.COOPERATE.value
        
        previous_action, adversary_previous_action = match_history[row_or_col][-1]

        # go back to cooperating if defected
        defected = (previous_action == Action.DEFECT.value)
        if defected:
            return Action.COOPERATE.value

        return adversary_previous_action

        