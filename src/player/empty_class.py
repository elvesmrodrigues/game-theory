from player import Player

from typing import List, Dict, Union


class EmptyClass (Player):
    
    
    def get_action(self, game_type: str, 
                        adversary_id: str,
                        available_actions: List[str], 
                        adversary_available_actions: List[str], 
                        payoff_matrix: Dict[str, Dict[str, Union[float, int]]]) -> str:
                        
        return ""
                