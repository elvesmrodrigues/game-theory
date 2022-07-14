import json
import logging
import os
from unicodedata import name
import uuid
import time
from pathlib import Path
from copy import deepcopy
import argparse
from random import randint, shuffle, choice
from typing import Dict, List, Tuple, Union

import pandas as pd
from pandas import DataFrame
from func_timeout import func_timeout
from func_timeout.exceptions import FunctionTimedOut
from src.game.game import Game, create_game_class_instance_entire_folder
from src.player.dynamic_imports import \
    create_player_class_instance_entire_folder
from src.player.player import Player
from typing_extensions import Literal, TypedDict

Number = Union[int, float]
PayoffMatrix = Tuple[Tuple[Tuple[Number, ...], ...], ...]
MatchHistory = Dict[str, List[Tuple[int, int]]]

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s')

Number = Union[float, int]
PayoffMatrix = List[List[List[Number]]]

class PlayLog(TypedDict):
    tournament: int 
    player_row: str 
    player_col: str 
    player_row_action: int 
    player_col_action: int 
    player_row_payoff: Number
    player_col_payoff: Number 

class MatchLog(TypedDict):
    game_id: str 
    game_type: str 
    payoff_matrix: PayoffMatrix
    players: List[Player]
    tournament_type: str 
    num_tournaments: int
    plays: List[PlayLog]

class Tournament:
    def __init__(self, players: List[Player], 
                    games: List[Game],
                    action_timeout: float = 1.0, 
                    log_path: str = 'logs/') -> None:

        self.id: str = str(uuid.uuid4())

        self.players: List[players] = players

        # used to create random matchings in each turn. If the number of players is odd, add the robot player 
        self.robot_players: List[players] = self.__create_robot_players(players)

        self.games: List[Game] = games
        self.action_timeout: float = action_timeout

        self.scores: Dict[int, Dict[int, List[Number]]] = dict()
    
        self.match_logs: Dict[str, MatchLog] = dict()
        self.log_path: str = log_path if log_path[-1] == '/' else log_path + '/'


    def __create_robot_players(self, players: List[Player]) -> List[Player]:

        players_copies = deepcopy(players)

        for player in players_copies:
            player.name = f"[ROBOT] {player.name}"
            player.robot = True

        return players_copies


    def __create_match_log(self, game: Game, tournament_type: str, num_tournaments: int, tournament: int, 
                                player_row: Player, player_col: Player, player_row_action: int, player_col_action: int):
        
        if game.id not in self.match_logs:
            self.match_logs[game.id] = {
                'game_id': game.id,
                'game_type': game.type,
                'payoff_matrix': game.payoff_matrix,
                'players': [player.name for player in self.players],
                'tournament_type': tournament_type,
                'num_tournaments': num_tournaments,
                'plays': list()
            }
        
        player_row_payoff: Number = game.payoff_row[player_row_action][player_col_action][0]
        player_col_payoff: Number = game.payoff_col[player_col_action][player_row_action][0]
        

        play_log: PlayLog = {
            'tournament': tournament,
            'player_row': player_row.name,
            'player_col': player_col.name,
            'player_row_action': player_row_action,
            'player_col_action': player_col_action,
            'player_row_payoff': player_row_payoff,
            'player_col_payoff': player_col_payoff
        }

        self.match_logs[game.id]['plays'].append(play_log)

    def save_match_logs(self):
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        for match_log in self.match_logs.values():
            game_id = match_log['game_id']
            game_type = match_log['game_type']

            filename = f'{self.log_path}{game_type}_{game_id}_{self.id}.json'

            with open(filename, 'w') as f:
                f.write(json.dumps(match_log, indent=4))
        
    def create_complete_matchings(self) -> List[Tuple[Player, Player]]:
        '''    
        This method creates round matching between all players.

        If the method receives players A, B and C, it creates matchings 
        [(A, B), (A, C), (B, A), (B, C), (C, A) and (C, B)].  

        --------------------------
        Return:

            Returns the round matching between all players.
        '''

        return [
            (player_row, player_col)
            for player_row in self.players
            for player_col in self.players
            if player_row.name != player_col.name
        ]
    
    def create_random_matchings(self) -> List[Tuple[Player, Player]]:
        '''
        This method creates round matching between the players randomly.

        If the number of players is odd, a robot player will be inserted into the match, 
        and then random matches will be created between them in each round.

        If the method receives A, B, C, it can create in round 1 the matchings 
        [(A,B), (B,C), (C, Robot)] and in another round create the matchings [(Robot, A), (C, A), (A,B)]. 

        --------------------------
        Return:

            Returns the round matching between all players.
        '''
        
        shuffle(self.players)

        matching: List[Tuple[Player, Player]] = [
            (player_row, player_col) 
            for player_row, player_col in zip(self.players[::2], self.players[1::2])
        ]

        if len(self.players)%2 == 1:
            last_player = self.players[-1]
            robot = choice(self.robot_players)

            while robot.name == f"[ROBOT] {last_player.name}":
                robot = choice(self.robot_players)

            match_to_append = [last_player,robot]
            shuffle(match_to_append)

            matching.append(tuple(match_to_append))

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

        # Robot payoffs are not considered
        if player.robot:
            return

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
            if not os.path.exists('out/'):
                os.makedirs('out/')

            output_file = f'out/tournament_{self.id}.csv'
            
        df = self.get_ranking()
        df['Tournament ID'] = self.id
        df.to_csv(output_file, index=False)
        
    def get_ranking(self) -> DataFrame:
        data = list()
        for player in self.scores:
            total_payoff = 0
            number_of_plays = 0
            for game in self.scores[player]:
                total_payoff += sum(self.scores[player][game])
                number_of_plays += len(self.scores[player][game])

            data.append((player, total_payoff, round(total_payoff / number_of_plays, 2) , number_of_plays))

        df = pd.DataFrame(data, columns=['Player', 'Total payoff', 'Mean payoff', 'No. of plays']) 
        df.sort_values(by='Total payoff', ascending=False, inplace=True)

        return df 

    def __clean_terminal(self):
        clean_command: str = 'cls' if os.name == 'nt' else 'clear'
        os.system(clean_command) 

    def show_ranking(self, num_rounds: int, total_rounds: int, time_between_ranking_shows: float):
        self.__clean_terminal()

        df: DataFrame = self.get_ranking()

        output: str = df.to_string(index=False)
        max_columns_chars: int = output.find('\n') + 1
        
        print(f'Round {num_rounds} of {total_rounds}\n'.center(max_columns_chars))
        print(output)

        time.sleep(time_between_ranking_shows)

    def round_robin(self, matching_strategy: Literal['complete', 'random'], 
                        num_tournaments: int = 1, 
                        time_between_ranking_shows: float = .5):
        '''

        This method runs k double round-robin tournaments between players in each game in the list `games`.

        --------------------------
        Parameters:
            games: List[Game]

                List of games that the player will play.

            num_tournaments: int

                Number of tournaments that the players will play against each other each game.

            time_between_ranking_shows: float

                The ranking of the players will be displayed every time_between_ranking_shows seconds, 
                if time_between_ranking_shows is different from None.

        --------------------------
        Return:

            None.
        
        '''

        tournament_type = f'round-robin [{matching_strategy}]'
        matchings = self.create_complete_matchings()   

        rounds_count = 0
        current = time.time()

        num_rounds = len(self.games) * num_tournaments

        for game in self.games:
            for tournament in range(1, num_tournaments + 1):

                if matching_strategy == 'complete':
                    matchings = self.create_random_matchings()

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

                    player_row_payoff = game.payoff_row[player_row_action][player_col_action][0]
                    player_col_payoff = game.payoff_col[player_col_action][player_row_action][0]

                    self.__update_player_score(game.id, player_row, player_row_payoff)
                    self.__update_player_score(game.id, player_col, player_col_payoff)

                    self.__create_match_log(game, tournament_type, num_tournaments, tournament, player_row, 
                                            player_col, player_row_action, player_col_action)

                rounds_count += 1
                time_elapsed = time.time() - current

                if num_tournaments < 100:
                    self.show_ranking(rounds_count, num_rounds, time_between_ranking_shows)   
                elif time_elapsed > time_between_ranking_shows:
                    self.show_ranking(rounds_count, num_rounds, 0)
                    current = time.time()

        self.show_ranking(rounds_count, num_rounds, 0)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='List the content of a folder')
    
    arg_parser.add_argument('-pf',
                            '--player_folder',
                            default='src/player/',
                            help='Folder where the players\' strategies are implemented.')

    arg_parser.add_argument('-gf',
                            '--game_folder',
                            default='games/',
                            help='Folder where the games\' json is.')

    arg_parser.add_argument('-nt',
                        '--num_tournaments',
                        type=int,
                        default=1,
                        help='Number of tournaments..')

    arg_parser.add_argument('-ms',
                    '--matching_strategy',
                    default='complete',
                    choices=['complete', 'random'],
                    help='Matching strategy.')

    arg_parser.add_argument('-o',
                    '--output',
                    help='Name of the XLS file to save the match results.')

    arg_parser.add_argument('-lp',
                    '--log_path',
                    default='logs',
                    help='Folder where the logs of the matches will be recorded.')

    arg_parser.add_argument('-tbrs',
                    '--time_between_ranking_shows',
                    default=.5,
                    help='Folder where the logs of the matches will be recorded.')

    args: argparse.Namespace = arg_parser.parse_args()

    player_folder: Path = Path(args.player_folder) 
    game_folder: str = args.game_folder

    num_tournaments: int = args.num_tournaments
    matching_strategy: str = args.matching_strategy

    output_file: str = args.output
    log_path: str = args.log_path

    players: List[Player] = create_player_class_instance_entire_folder(player_folder)
    games: List[Game] = create_game_class_instance_entire_folder(game_folder)

    time_between_ranking_shows: float = args.time_between_ranking_shows

    tournament: Tournament = Tournament(players, games, log_path=log_path)
    tournament.round_robin(matching_strategy, num_tournaments, time_between_ranking_shows)

    tournament.save_result(output_file)
    tournament.save_match_logs()