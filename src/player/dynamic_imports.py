import re

from os import walk
from pathlib import Path
from importlib import import_module
from collections import Counter

from typing import List, Optional, Set, Type
from types import ModuleType

from .player import Player


def _get_player_class_name(path_to_file: Path) -> str:

    """
        Given a .py file, returns its class' name.

        It is assumed that the class inherits from Player, 
        i.e. the line with its declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    regex_pattern = re.compile(r"class\s*(?P<class_name>.+?)\s*\(Player\)")

    with path_to_file.open("r") as file:

        for line in file:
            regex_match = re.match(regex_pattern, line)

            if regex_match is not None:
                return regex_match.group("class_name")

        raise NameError(f"No class has been found in {path_to_file}.")


def import_class_from_from_file(
    filename: str, class_name: str, package: str
) -> Type:
    
    module: ModuleType = import_module(
        "." + filename.rstrip(".py"), package
    )
    class_: Type = getattr(module, class_name)

    return class_


def create_player_class_instance_from_file(
    path_to_file: Path, package: str
) -> Player:

    """
        Given a .py file, create an instance of its class.

        It is assumed that the class inherits from Player, 
        i.e. the line with its declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    filename: str = path_to_file.name
    class_name: str = _get_player_class_name(path_to_file)

    class_: Type[Player] = import_class_from_from_file(
        filename, class_name, package
    )
    return class_()


def are_strings_unique(list_strings: List[str]) -> bool:
    return len(list_strings) == len(set(list_strings))


def return_duplicate_strings(list_string: List[str]) -> List[str]:
    return [
        string 
        for string, count in Counter(list_string).items() 
        if count > 1
    ]


def _get_filenames(path_to_folder: Path) -> List[str]:

    (_, _, filenames) = next(walk(path_to_folder))

    if not are_strings_unique(filenames):
        duplicates = return_duplicate_strings(filenames)
        raise ValueError(f"Filenames are not unique. {duplicates} showed more than one.")

    filenames = [file for file in sorted(filenames)]

    return filenames


def create_player_class_instance_entire_folder(
    path_to_folder: Path = Path("players/"), 
    filenames_to_exclude: Set[str] = set(),
    package: str = "players"
) -> List[Player]:

    """
        Given a folder, return a list with an instance of all
        of its file's classes. If there are any files which do 
        not have a class, add its name to "filenames_to_exclude".

        It is assumed that the classes inherit from Player, 
        i.e. the line with their declaration should be like 
        "class <CLASS_NAME><some_spaces_maybe>(Player)<rest>".
    """

    filenames: Optional[List[str]] = None

    if path_to_folder.is_dir():
        filenames = _get_filenames(path_to_folder)

    if filenames is not None:

        instances: List[Player] = [
            create_player_class_instance_from_file(path_to_folder / file, package) 
            for file in filenames
            if file not in filenames_to_exclude
        ]

        classes_names: List[str] = [class_.name for class_ in instances]

        if not are_strings_unique(classes_names):
            duplicates = return_duplicate_strings(classes_names)
            raise ValueError(f"Classes' names are not unique. {duplicates} showed more than one.")
        
        return instances

    return []