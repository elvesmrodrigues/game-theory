from typing import List, Tuple 

from src.player.player import Player
from src.game.game import Game 
from src.game.game import GameFactoryFromJson
from src.player.dynamic_imports import create_player_class_instance_entire_folder

class Tournament:
    def __init__(self, players: List[Player]) -> None:
        self.players = players
        self.scores = dict()

    def __create_matchings(self) -> List[Tuple[Player, Player]]:
        matching: List[Tuple[Player, Player]] = list()
        for player_row in self.players:
            for player_col in self.players:
                if player_row.name == player_col.name:
                    continue
                matching.append((player_row, player_col))
        return matching

    def round_robin(self, games: List[Game]):
        matchings = self.__create_matchings()

        for game in games:
            for player_row, player_col in matchings:
                player_row_action = player_row.get_action(game.type, 
                                        game.payoff_row, 
                                        player_col.name, 
                                        player_row.get_match_history(game.id, player_col.name),
                                        'row')

                player_col_action = player_col.get_action(game.type,
                                        game.payoff_col,
                                        player_row.name,
                                        player_col.get_match_history(game.id, player_row.name),
                                        'col')

                player_row.update_match_history(game.symmetric, game.id, player_col.name, 'row', player_row_action, player_col_action)
                player_col.update_match_history(game.symmetric, game.id, player_row.name, 'col', player_col_action, player_row_action)

                payoff_player_row = game.payoff_row[player_row_action][player_col_action][0]
                payoff_player_col = game.payoff_col[player_col_action][player_row_action][0]

                if player_row.name not in self.scores:
                    self.scores[player_row.name] = dict()

                if game.type not in self.scores[player_row.name]:
                    self.scores[player_row.name][game.type] = list()

                if player_col.name not in self.scores:
                    self.scores[player_col.name] = dict()

                if game.type not in self.scores[player_col.name]:
                    self.scores[player_col.name][game.type] = list()

                self.scores[player_row.name][game.type].append(payoff_player_row)
                self.scores[player_col.name][game.type].append(payoff_player_col)

                print(f'{player_row.name} [{payoff_player_row}] x {player_col.name} [{payoff_player_col}]')
            

        print('-' * 15)

        print(f'Final results:')
        for player in self.scores:
            print(player)
            for game in self.scores[player]:
                print(f'\t{game}')
                total_points = sum(self.scores[player][game])
                mean_points = total_points / len(self.scores[player][game])
                print(f'\t\t Total points: {total_points}')
                print(f'\t\t Mean points: {mean_points}')
            print('\n')
        # print(self.scores)
        print('-' * 15)

if __name__ == '__main__':
    players = create_player_class_instance_entire_folder()
    game = GameFactoryFromJson("src/game/game_test_sym.json").create_game() 
    games = [game]

    tournament = Tournament(players)
    tournament.round_robin(games)

    # print(players)