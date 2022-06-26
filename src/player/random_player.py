from player import Player

from typing import Dict, Tuple, Union
from random import randint


class RandomPlayer(Player):


    def get_action(self, game_type: str, 
                        adversary_id: str, 
                        available_actions: Tuple[str], 
                        adversary_available_actions: Tuple[str], 
                        payoff_matrix: Dict[str, Dict[str, Union[float, int]]]) -> str:

        return available_actions[randint(0, len(available_actions) - 1)]


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

    player_row_available_action = ('R0', 'R1')
    player_col_available_action = ('C0', 'C1')

    action_player_1 = random_player_1.get_action('test', None, player_row_available_action, player_col_available_action, payoff_matrix)
    action_player_2 = random_player_2.get_action('test', None, player_col_available_action, player_row_available_action, payoff_matrix)

    print(f'Payoff of player row: {payoff_matrix[action_player_1][action_player_2]}')
    print(f'Payoff of player col: {payoff_matrix[action_player_2][action_player_1]}')

    random_player_1.update_knowledge('test', None, payoff_matrix, '', None, None, None)

    print(random_player_1.memory)