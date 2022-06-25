from typing import List, Union


class Player:
    def __init__(self) -> None:
        pass
    
    def get_action(self, game_type: str, 
                        adversary_id: str,
                        available_action: List[int], 
                        adversary_available_action: List[int], 
                        payoff_matrix: List[List[Union[float, int]]], 
                        adversary_payoff_matrix: List[List[Union[float, int]]]) -> int:

        '''Retorna a ação do jogador quando ele recebe a matrix de payoff, suas ações disponíveis, etc
        '''
        raise NotImplementedError('You must implement your own method')

    def update_knowledge(self, game_type: str, payoff: Union[float,int], action_taken: int, adversary_id: str, action_taken_by_adversary: int)