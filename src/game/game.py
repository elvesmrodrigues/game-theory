import re
from typing import List, Tuple, Union
from typing_extensions import Literal

from player import Player

class Game:
    def __init__(self, game_type: str, player_row_payoff_matrix: List[List[Union[float, int]]], player_col_payoff_matrix: List[List[Union[float, int]]]) -> None:
        self.type = game_type

        self.player_row_payoff_matrix = player_row_payoff_matrix
        self.player_col_payoff_matrix = player_col_payoff_matrix

        num_row_player_action = len(player_row_payoff_matrix)
        num_col_player_action = len(player_row_payoff_matrix[0])

        self.player_row_available_actions = list(range(num_row_player_action))
        self.player_col_available_actions = list(range(num_col_player_action))

    def get_payoff(self, player: Literal['row', 'col'], player_row_action: int, player_col_action: int) -> Union[float, int]:
        if player == 'row':
            return self.player_row_payoff_matrix[player_row_action][player_col_action]
        return self.player_col_payoff_matrix[player_row_action][player_col_action]

    def play(self, player_row: Player, player_col: Player) -> Tuple[Union[float, int], Union[float, int]]:
        player_row_action = player_row.get_action(self.type, 
                                                self.player_row_available_actions, 
                                                self.player_col_available_actions, 
                                                self.player_row_payoff_matrix, 
                                                self.player_col_payoff_matrix)

        player_col_action = player_col.get_action(self.type, 
                                                self.player_col_available_actions,
                                                self.player_row_available_actions,
                                                self.player_col_payoff_matrix,
                                                self.player_row_payoff_matrix)

    
if __name__ == '__main__':
    player_row_payoff_matrix = [
        [1, 2],
        [4, 7]
    ]
    
    player_col_payoff_matrix = [
        [4, 8],
        [9, 0]
    ]

    game = Game('test', player_row_payoff_matrix, player_col_payoff_matrix)

    print(game.get_payoff('row', 1, 1))