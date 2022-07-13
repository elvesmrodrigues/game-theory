import json
from pathlib import Path

from src.player.dynamic_imports import create_player_class_instance_entire_folder
from src.game.game import create_game_class_instance_entire_folder
from src.tournament.tournament import Tournament

CONFIG = "./configuration.json"


def get_config(config_filename):

    config = None

    with open(config_filename, "r") as file:
        config = json.load(file)

    return config


def run_tournament(players, games, config):

    tournament = Tournament(
        players = players,
        games = games,
        action_timeout = config["Tournament"]["time_to_take_action"],
        log_path = config["Tournament"]["match_logs_dir"]
    )

    tournament.round_robin(
        matching_strategy = config["Tournament"]["matching_strategy"], 
        num_tournaments = config["Tournament"]["number_of_rounds"]
    )

    tournament.save_result(
        output_file = config["Tournament"]["ranking_filename"]
    )

    tournament.save_match_logs()


def main():

    config = get_config(CONFIG)

    if config is None:
        return

    players = create_player_class_instance_entire_folder(
        path_to_folder = Path(config["Player"]["dir"])
    )

    games = create_game_class_instance_entire_folder(
        path = config["Games"]["dir"]
    )

    run_tournament(players, games, config)


if __name__ == "__main__":
    main()