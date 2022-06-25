import re
from typing import List, Tuple, Union
from typing_extensions import Literal

from player import Player

class Game:
    def __init__(self, game_type: str, player_row_payoff_matrix: List[List[Union[float, int]]], player_col_payoff_matrix: List[List[Union[float, int]]]) -> None:
        self.type = game_type

        self.payoff_matrix = dict()
        for row in range(len(player_row_payoff_matrix)):
            self.payoff_matrix[f'R{row}'] = dict()
            for col in range(len(player_row_payoff_matrix[0])):
                self.payoff_matrix[f'C{col}'] = player_row_payoff_matrix[row][col]

                if f'C{col}' not in self.payoff_matrix:
                    self.payoff_matrix[f'C{col}'] = dict()
                
                self.payoff_matrix[f'C{col}'][f'R{row}'] = player_col_payoff_matrix[row][col]

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