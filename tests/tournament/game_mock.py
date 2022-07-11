from src.game.game import GameFactoryFromJson, GameDict

def get_mock_game():
    game_dict: GameDict = {
        "id": 0, 
        "type": "PD",
        "payoff_matrix": [
            [[1,1], [1,1]],
            [[1,1], [1,1]]
        ]
    }

    return GameFactoryFromJson().create_game(game_dict)
