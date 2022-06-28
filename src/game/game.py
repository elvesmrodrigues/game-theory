from typing import List, Union

from src.player.player import Player


PayoffType = List[List[Union[float, int]]]


class Game:


    def __init__(self, 
        game_id: int,
        game_type: str, 
        player_row_payoff_matrix: PayoffType, 
        player_col_payoff_matrix: PayoffType
    ) -> None:
        
        self.id = game_id
        self.type = game_type
        self.payoff_matrix = dict()
        self.row_actions = list()
        self.col_actions = list()

        for row, (row_payoffs, col_payoffs) in enumerate(zip(player_row_payoff_matrix, player_col_payoff_matrix)):
            
            row_action = f'R{row}'
            self.row_actions.append(row_action)

            for col, (row_payoff, col_payoff) in enumerate(zip(row_payoffs, col_payoffs)):

                col_action = f'C{col}'
                self.col_actions.append(col_action)

                self.payoff_matrix[(row_action, col_action)] = row_payoff
                self.payoff_matrix[(col_action, row_action)] = col_payoff

        self.row_actions = tuple(self.row_actions)
        self.col_actions = tuple(self.col_actions)


    def play(self, player_row: Player, player_col: Player) -> None:

        row_action = player_row.get_action(
            self.type, self.payoff_matrix,
            player_col, self.row_actions, self.col_actions
        )

        col_action = player_col.get_action( 
            self.type, self.payoff_matrix,
            player_row, self.col_actions, self.row_actions
        )

        player_row.update_knowledge(
            self.id, player_col, self.row_actions, 
            row_action, col_action
        )

        player_col.update_knowledge(
            self.id, player_row, self.col_actions,
            col_action, row_action
        )


    
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

    #print(game.get_payoff('row', 1, 1))