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
        min_num_rounds = config["Tournament"]["min_number_of_rounds"],
        max_num_rounds = config["Tournament"]["max_number_of_rounds"],
        time_between_ranking_shows=config["Tournament"]["time_between_ranking_shows"],
        print_after = config["Tournament"]["print_ranking_after_n_rounds"]
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
        path_to_folder = Path(config["Player"]["dir"]),
        filenames_to_exclude = set(config["Player"]["files_to_ignore"])
    )

    games = create_game_class_instance_entire_folder(
        path_to_folder = Path(config["Games"]["dir"]),
        filenames_to_exclude = set(config["Games"]["files_to_ignore"])
    )

    run_tournament(players, games, config)


if __name__ == "__main__":
    main()