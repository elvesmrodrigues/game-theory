from player import Player

from typing import List, Dict, Union


class TestClass (Player):
    
    
    def __init__(self) -> None:
        super().__init__()

    def get_action(self, game_type: str, 
                        adversary_id: str,
                        available_actions: List[str], 
                        adversary_available_actions: List[str], 
                        payoff_matrix: Dict[str, Dict[str, Union[float, int]]]) -> str:
                        
        print("Method exists!")
                