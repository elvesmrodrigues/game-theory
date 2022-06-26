import re

from os import walk
from pathlib import Path

from typing import List, Optional, Set, Type
from types import ModuleType

from . import Player


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
        Given a .py file, create an instance of its class.

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


def _are_filenames_unique(filenames: List[str]):
    return len(filenames) == len(set(filenames))


def _get_filenames(path_to_folder: Path) -> List[Path]:

    (_, _, filenames) = next(walk(path_to_folder))

    if not _are_filenames_unique(filenames):
        raise RuntimeError("Some of the provided files have the same name.")

    filenames = [Path(file) for file in sorted(filenames)]

    return filenames


def create_class_instance_entire_folder(
    path_to_folder: Path = Path("src/player/"), 
    filenames_to_exclude: Set[Path] = {
        Path("__init__.py"),
        Path("player.py"),
        Path("dynamic_imports.py")
    }
) -> List[Player]:

    """
        Given a folder, return a list with an instance of all
        of its file's classes. If there are any files which do 
        not have a class, add its name to "filenames_to_exclude".

        It is assumed that the classes inherit from Player, 
        i.e. the line with their declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    filenames: Optional[List[Path]] = None

    if path_to_folder.is_dir():
        filenames = _get_filenames(path_to_folder)

    if filenames is not None:
        return [
            create_class_instance_from_file(path_to_folder / file) 
            for file in filenames
            if file not in filenames_to_exclude
        ]
        
    return []


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


    test_and_random_class: List[Player] = create_class_instance_entire_folder(
        PATH_PLAYERS
    )

    print(
        test_and_random_class[0].get_action(
            game_type = "",
            adversary_id = "",
            available_actions = ["R0", "R1"],
            adversary_available_actions = [],
            payoff_matrix = dict()
        )
    )

    test_and_random_class[1].get_action(
        game_type = "",
        adversary_id = "",
        available_actions = [],
        adversary_available_actions = [],
        payoff_matrix = dict()
    )