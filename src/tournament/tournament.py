import logging
import uuid
from random import randint
from typing import Dict, List, Tuple, Union

import pandas as pd
from func_timeout import func_timeout
from func_timeout.exceptions import FunctionTimedOut
from src.game.game import Game, GameFactoryFromJson
from src.player.dynamic_imports import \
    create_player_class_instance_entire_folder
from src.player.player import Player
from typing_extensions import Literal

Number = Union[int, float]
PayoffMatrix = Tuple[Tuple[Tuple[Number, ...], ...], ...]
MatchHistory = Dict[str, List[Tuple[int, int]]]

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s')


# TODO: Ao invés dos logs serem salvos em json, salvá-los em CSV. Para importar mais fácil para planilha
class Tournament:
    def __init__(self, players: List[Player], games: List[Game], action_timeout: float = 1.0) -> None:
        self.id: str = str(uuid.uuid4())

        self.players: List[players] = players
        self.games: List[Game] = games
        self.action_timeout: float = action_timeout

        self.scores: Dict[int, Dict[int, List[Number]]] = dict()
        self.logs: Dict[int, Dict[int, List[Number]]] = dict()

    def __create_matchings(self) -> List[Tuple[Player, Player]]:
        '''    
        This method creates round matching between all players.


        --------------------------
        Return:

            Returns the round matching between all players.
        '''

        matching: List[Tuple[Player, Player]] = list()

        for player_row in self.players:
            for player_col in self.players:
                if player_row.name == player_col.name:
                    continue
                matching.append((player_row, player_col))

        return matching

    def __update_player_score(self, game_id: int, player: Player, payoff: Number):
        '''
        Updates the player's score according to new rounds.

        --------------------------
        Parameters:

            game_id: int 

                ID of the game being played in the round.

            player: Player

                Player who is having his score updated.

            payoff: Number

                Payoff ot the player in the round.

        --------------------------
        Return:

            None.

        '''

        if player.name not in self.scores:
            self.scores[player.name] = dict()

        if game_id not in self.scores[player.name]:
            self.scores[player.name][game_id] = list()

        self.scores[player.name][game_id].append(payoff)

    def __get_player_action_safely(self, game_type: str, 
                                        player: Player, 
                                        payoff_matrix: PayoffMatrix, 
                                        adversary_id: str, 
                                        match_history: MatchHistory, 
                                        row_or_col: Literal['row', 'col']) -> int:
        '''
        This method gets a player's action safely. That is, considering that it may raise an exception or take longer than it should.

        --------------------------
        Parameters:

            game_type: str

                Type of the game. 
                (Possible types yet to be defined.)

            payoff_matrix: tuple[tuple[tuple[number, ...], ...], ...]

                Payoff matrix of the player.

            adversary_id: str

                The opponent's name.

            match_history: Optional[dict[str, list[tuple[int, int]]]]

                Dictionary of lists containing the match history between the and 
                the adversary. If there are no matches, its value will be None.

            rol_or_col: Literal

                "rol" if you are the row player and "col" otherwise.
            
        --------------------------
        Return:
            action: int
                The action that the wants to take.          

        '''

        action = None
        try:
            args = (game_type, payoff_matrix, adversary_id, match_history, row_or_col)
            action = func_timeout(timeout=self.action_timeout, func=player.get_action, args=args)
        except FunctionTimedOut:
            action = randint(0, len(payoff_matrix)-1) 

            logging.error(f'The action to be played by {player.name} was not returned in' \
                            f' {self.action_timeout} seconds and was terminated. The random' \
                            f' action {action} was taken.')

        except Exception as e:
            action = randint(0, len(payoff_matrix)-1) 
            logging.error(f'The action of player {player.name} generated the following exception' + \
                          f'and the random action {action} was taken: {e}')

        return action

    def save_result(self, output_file: str = None):
        '''
        Method responsible for presenting the players' performance. If the csv_filename parameter is 
        given a valid string (other than None), saves the results in a csv named csv_filename.
        
        --------------------------
        Parameters:
            output_file: str

                Name of the file to be generated with the match results.
        
        --------------------------
        Return:

            None.
        '''
        if output_file is None:
            output_file = f'tournament.xlsx'

        data = list()

        for player in self.scores:
            for game in self.scores[player]:
                total_score = sum(self.scores[player][game])
                num_plays = len(self.scores[player][game])
                mean_score = round(total_score / num_plays, 2)
                
                data.append((player, game, total_score, mean_score, num_plays))

        df = pd.DataFrame(data, columns=['Player', 'Game', 'Total payoff', 'Mean payoff', 'No. of plays']) 

        with pd.ExcelWriter(output_file) as writer:
            for game in self.games:
                df_aux = df.loc[df['Game'] == game.type]

                df_aux = df_aux.drop('Game', axis=1)
                df_aux.sort_values(by='Mean payoff', ascending=False, inplace=True)

                df_aux.to_excel(writer, sheet_name=game.type, index=False)

    def round_robin(self, num_tournaments: int = 1):
        '''

        This method runs k double round-robin tournaments between players in each game in the list `games`.

        --------------------------
        Parameters:
            games: List[Game]

                List of games that the player will play.

            num_tournaments: int

                Number of tournaments that the players will play against each other each game.

        --------------------------
        Return:

            None.
        
        '''

        matchings = self.__create_matchings()

        for game in self.games:
            for tournament in range(num_tournaments):
                for player_row, player_col in matchings:
                    player_row_action = self.__get_player_action_safely(game.type, 
                                                                        player_row, 
                                                                        game.payoff_row, 
                                                                        player_col.name, 
                                                                        player_row.get_match_history(game.id, player_col.name), 
                                                                        'row')

                    player_col_action = self.__get_player_action_safely(game.type, 
                                                                        player_col,
                                                                        game.payoff_col,
                                                                        player_row.name,
                                                                        player_col.get_match_history(game.id, player_row.name), 
                                                                        'col')

                    player_row.update_match_history(game.symmetric, 
                                                    game.id, 
                                                    player_col.name, 
                                                    'row', 
                                                    player_row_action, 
                                                    player_col_action)

                    player_col.update_match_history(game.symmetric, 
                                                    game.id, 
                                                    player_row.name, 
                                                    'col', 
                                                    player_col_action, 
                                                    player_row_action)

                    payoff_player_row = game.payoff_row[player_row_action][player_col_action][0]
                    payoff_player_col = game.payoff_col[player_col_action][player_row_action][0]

                    self.__update_player_score(game.type, player_row, payoff_player_row)
                    self.__update_player_score(game.type, player_col, payoff_player_col)


if __name__ == '__main__':
    players = create_player_class_instance_entire_folder()
    game = GameFactoryFromJson("src/game/game_test_sym.json").create_game() 
    game2 = GameFactoryFromJson("src/game/game_test_asym.json").create_game() 
    games = [game, game2]

    tournament = Tournament(players, games)
    tournament.round_robin()

    tournament.save_result()
