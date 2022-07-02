from src.player.player import Player, MatchHistory, PayoffMatrix

from typing import Optional
from typing_extensions import Literal
from random import randint


class RandomPlayer(Player):


    def __init__(self) -> None:
        self.name = "Random Player"
        self.match_history = dict()


    def get_action(self,
        game_type: str, 
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:

        return randint(0, len(payoff_matrix)-1)