from typing import Optional
from typing_extensions import Literal

from src.player.player import Player, PayoffMatrix, MatchHistory 

class PlayerMock(Player):
    def __init__(self, action: int, name: str = None) -> None:
        super().__init__()

        self.name: str = f'Always action {action}' if name is None else name
        self.action: int = action

    def get_action(self, game_type: str, payoff_matrix: PayoffMatrix, 
                        adversary_id: str, match_history: Optional[MatchHistory], 
                        row_or_col: Literal['row', 'col']) -> int:
        
        return self.action