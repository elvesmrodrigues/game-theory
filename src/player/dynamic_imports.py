import re

from pathlib import Path



def get_player_class_name(path_to_file: Path) -> str:

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


if __name__ == "__main__":

    test_path = Path("./test_class.py")

    print(f"Function: {get_player_class_name(test_path)}\nExpected: TestClass")