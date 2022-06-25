from typing import Dict, List, Union
from random import randint

class Player:
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
        self.memory = dict()
    
    def get_action(self, game_type: str, 
                        adversary_id: str,
                        available_action: List[str], 
                        adversary_available_action: List[str], 
                        payoff_matrix: Dict[str, Dict[str, Union[float, int]]]) -> str:

        '''Retorna a ação do jogador quando ele recebe a matrix de payoff, suas ações disponíveis, etc
        '''
        raise NotImplementedError('You must implement your own method')

    def update_knowledge(self, game_type: str, 
                                adversary_id: str, 
                                payoff_matrix: Dict[str, Dict[str, Union[float, int]]], 
                                action_taken: str, 
                                available_actions: List[str] , 
                                action_taken_by_adversary: str, 
                                adversary_available_action: List[str]) -> None:

        if game_type not in self.memory:
            self.memory[game_type] = dict()

        if adversary_id not in self.memory[game_type]:
            self.memory[game_type][adversary_id] = list()

        self.memory[game_type][adversary_id].append({
            'action_taken': action_taken,
            'available_actions': available_actions,
            'adversary_action_taken': action_taken_by_adversary,
            'adversary_available_action': adversary_available_action,
            'payoff_matrix': payoff_matrix
        })

# Classe apenas de exemplo
class RandomPlayer(Player):
    def get_action(self, game_type: str, 
                        adversary_id: str, 
                        available_action: List[str], 
                        adversary_available_action: List[str], 
                        payoff_matrix: Dict[str, Dict[str, Union[float, int]]]) -> str:

        return available_action[randint(0, len(available_action) - 1)]

if __name__ == '__main__':
    '''
    Matrix de payoff abaixo:

            C0       C1
        -----------------
    R0  | (1,1)  | (10,0)|
        -----------------
    R1  | (0,10) | (5,5) |
        ------------------
    
    Deverá ser representada como:

    '''
    payoff_matrix = {
        'R0': {
            'C0': 1,
            'C1': 10 
        },
        'R1': {
            'C0': 0,
            'C1': 5
        },
        'C0': {
            'R0': 1,
            'R1': 10
        },
        'C1': {
            'R0': 0,
            'R1': 5
        }
    }

    random_player_1 = RandomPlayer()
    random_player_2 = RandomPlayer()

    player_row_available_action = ['R0', 'R1']
    player_col_available_action = ['C0', 'C1']

    action_player_1 = random_player_1.get_action('test', None, player_row_available_action, player_col_available_action, payoff_matrix)
    action_player_2 = random_player_2.get_action('test', None, player_col_available_action, player_row_available_action, payoff_matrix)

    print(f'Payoff of player row: {payoff_matrix[action_player_1][action_player_2]}')
    print(f'Payoff of player col: {payoff_matrix[action_player_2][action_player_1]}')