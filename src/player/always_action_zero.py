from typing import Optional
from typing_extensions import Literal
from src.player.player import Player, MatchHistory, PayoffMatrix

class AlwaysActionZero(Player):


    def __init__(self) -> None:
        self.name = "Always action zero"
        self.match_history = dict()

    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:

        return 0