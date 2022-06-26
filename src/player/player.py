from abc import ABC, abstractmethod

from typing import Dict, Tuple, Union

class Player(ABC):
    def __init__(self) -> None:
        '''
        memory format: 
        {
            'game_type': {
                'adversary_id': [
                    'action_taken': str
                    'available_action': []
                    'adversary_action_taken': str,
                    'adversary_available_action': [] 
                ]
            }
        }
        '''
        self.name = ''        
        self.memory = dict()
    
    @abstractmethod
    def get_action(self, game_type: str, 
                        adversary_id: str,
                        available_actions: Tuple[str], 
                        adversary_available_actions: Tuple[str], 
                        payoff_matrix: Dict[str, Dict[str, Union[float, int]]]) -> str:
        ...

    def update_knowledge(self, game_type: str, 
                                adversary_id: str, 
                                payoff_matrix: Dict[str, Dict[str, Union[float, int]]], 
                                action_taken: str, 
                                available_actions: Tuple[str], 
                                action_taken_by_adversary: str, 
                                adversary_available_actions: Tuple[str]) -> None:

        if game_type not in self.memory:
            self.memory[game_type] = dict()

        if adversary_id not in self.memory[game_type]:
            self.memory[game_type][adversary_id] = list()

        self.memory[game_type][adversary_id].append({
            'action_taken': action_taken,
            'available_actions': available_actions,
            'adversary_action_taken': action_taken_by_adversary,
            'adversary_available_actions': adversary_available_actions,
            'payoff_matrix': payoff_matrix
        })

    
