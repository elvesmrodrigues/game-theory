import re

from pathlib import Path

from typing import List, Type
from types import ModuleType

from player import Player


PATH_PLAYERS = Path("src/player/")


def _get_player_class_name(path_to_file: Path) -> str:

    """
        Given a .py file, returns its class' name.

        It is assumed that the class inherits from Player, 
        i.e. the line with its declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    regex_pattern = re.compile(r"class (?P<class_name>.+?)\s*\(")

    with path_to_file.open("r") as file:

        for line in file:
            regex_match = re.match(regex_pattern, line)

            if regex_match is not None:
                return regex_match.group("class_name")

        raise NameError("No class has been found.")


def create_class_instance_from_file(path_to_file: Path) -> Player:

    """
        Given a .py file, import its class that inherits from Player.

        It is assumed that the class inherits from Player, 
        i.e. the line with its declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    filename: str = path_to_file.name
    class_name: str = _get_player_class_name(path_to_file)

    module: ModuleType = __import__(filename.strip(".py"))
    class_: Type[Player] = getattr(module, class_name)
    instance: Player = class_()

    return instance


if __name__ == "__main__":

    test_path: Path = PATH_PLAYERS / Path("./test_class.py")

    print(f"Function: {_get_player_class_name(test_path)}\nExpected: TestClass")

    test_class_instance: Player = create_class_instance_from_file(test_path)
    
    test_class_instance.get_action(
        game_type = "",
        adversary_id = "",
        available_actions = [],
        adversary_available_actions = [],
        payoff_matrix = dict()
    )