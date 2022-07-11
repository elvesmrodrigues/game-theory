import unittest

from typing import List, Tuple
from typing_extensions import TypedDict
from src.game.game import Game

from src.player.player import Player
from src.tournament.tournament import Tournament

from tests.tournament.game_mock import get_mock_game
from tests.tournament.player_mock import PlayerMock

class TestTournament(unittest.TestCase):
    def setUp(self) -> None:
        self.games: List[Game] = [get_mock_game()]
        self.players: List[Player] = [PlayerMock(0), PlayerMock(1)]
        self.robot_player: Player = PlayerMock(0, '[ROBOT]')

        self.tournament = Tournament(self.players, self.games, self.robot_player)

    def test_create_complete_matching(self):
        expected_matching: List[Tuple[Player, Player]] = [
            (self.players[0], self.players[1]),
            (self.players[1], self.players[0])
        ]

        self.assertEqual(expected_matching, self.tournament.create_complete_matchings())

    def test_create_random_matching(self):
        possible_matchings: List[Tuple[Player, Player]] = [
            (self.players[0], self.players[1]),
            (self.players[1], self.players[0])
        ]

        matchings: List[Tuple[Player, Player]] = self.tournament.create_random_matchings()

        self.assertEqual(len(matchings), 1)
        self.assertIn(matchings[0], possible_matchings)

    def test_complete_matching_score(self):
        self.tournament.round_robin(matching_strategy='complete')
        
        player_1_name: str = self.players[0].name
        player_2_name: str = self.players[1].name

        game_id: int = self.games[0].id

        player_1_scores = self.tournament.scores[player_1_name][game_id]
        player_2_scores = self.tournament.scores[player_2_name][game_id]

        self.assertEqual(sum(player_1_scores), 2)
        self.assertEqual(sum(player_2_scores), 2)

    def test_number_player_rounds_complete_matching(self):
        self.tournament.round_robin(matching_strategy='complete')

        player_1_name: str = self.players[0].name
        player_2_name: str = self.players[1].name

        game_id: int = self.games[0].id

        player_1_scores = self.tournament.scores[player_1_name][game_id]
        player_2_scores = self.tournament.scores[player_2_name][game_id]

        self.assertEqual(len(player_1_scores), 2)
        self.assertEqual(len(player_2_scores), 2)

        self.setUp()

        self.tournament.round_robin(matching_strategy='complete', num_tournaments=2)

        player_1_scores = self.tournament.scores[player_1_name][game_id]
        player_2_scores = self.tournament.scores[player_2_name][game_id]

        self.assertEqual(len(player_1_scores), 4)
        self.assertEqual(len(player_2_scores), 4)

        self.setUp()

        self.tournament.round_robin(matching_strategy='complete', num_tournaments=100)

        player_1_scores = self.tournament.scores[player_1_name][game_id]
        player_2_scores = self.tournament.scores[player_2_name][game_id]

        self.assertEqual(len(player_1_scores), 200)
        self.assertEqual(len(player_2_scores), 200)

    def test_number_player_rounds_complete_matching(self):
        self.tournament.round_robin(matching_strategy='random')

        player_1_name: str = self.players[0].name
        player_2_name: str = self.players[1].name

        game_id: int = self.games[0].id

        player_1_scores = self.tournament.scores[player_1_name][game_id]
        player_2_scores = self.tournament.scores[player_2_name][game_id]

        self.assertEqual(len(player_1_scores), 1)
        self.assertEqual(len(player_2_scores), 1)

        self.setUp()

        self.tournament.round_robin(matching_strategy='random', num_tournaments=2)

        player_1_scores = self.tournament.scores[player_1_name][game_id]
        player_2_scores = self.tournament.scores[player_2_name][game_id]

        self.assertEqual(len(player_1_scores), 2)
        self.assertEqual(len(player_2_scores), 2)

        self.setUp()

        self.tournament.round_robin(matching_strategy='random', num_tournaments=100)

        player_1_scores = self.tournament.scores[player_1_name][game_id]
        player_2_scores = self.tournament.scores[player_2_name][game_id]

        self.assertEqual(len(player_1_scores), 100)
        self.assertEqual(len(player_2_scores), 100)

    def test_random_matching_score(self):
        self.tournament.round_robin(matching_strategy='random')
        
        player_1_name: str = self.players[0].name
        player_2_name: str = self.players[1].name

        game_id: int = self.games[0].id

        player_1_scores = self.tournament.scores[player_1_name][game_id]
        player_2_scores = self.tournament.scores[player_2_name][game_id]

        self.assertEqual(sum(player_1_scores), 1)
        self.assertEqual(sum(player_2_scores), 1)