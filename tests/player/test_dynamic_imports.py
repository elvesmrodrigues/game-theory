import pytest

import src.player.dynamic_imports as di

from pathlib import Path
from typing import Callable, List, Type


@pytest.fixture(scope="function")
def empty_file(tmp_path: Path):
    
    temp_file: Path = tmp_path / "empty_file.py"
    temp_file.write_text("")

    return temp_file


@pytest.fixture(scope="function")
def incorrect_text_file(tmp_path: Path):

    temp_file: Path = tmp_path / "incorrect_text.py"
    temp_file.write_text("clas Class:")

    return temp_file


@pytest.fixture(scope="function")
def correct_text_file(tmp_path: Path) -> Callable[[str, str], Path]:

    def correct_text_file_class_name(filename: str, file_class_name: str) -> Path:

        tmp_file: Path = tmp_path / filename
        tmp_file.write_text(f"class {file_class_name}(Player):")

        return tmp_file
    
    return correct_text_file_class_name
    

class TestGetClassName:


    def test_empty_file(self, empty_file: Path):

        with pytest.raises(NameError):
            di._get_player_class_name(empty_file)


    def test_text_file(self, incorrect_text_file: Path):

        with pytest.raises(NameError):
            di._get_player_class_name(incorrect_text_file)


    def test_text_file(self, correct_text_file: Callable[[str], Path]):

        file_class_names: List[str] = ["Nome", "Nome     ", "  Nome "]
        filenames: List[str] = [f"file{i}" for i, value in enumerate(file_class_names)]

        expected_class_name: str = "Nome"
        
        for class_name, filename in zip(file_class_names, filenames):

            file = correct_text_file(filename, class_name)
            assert di._get_player_class_name(file) == expected_class_name


class TestCreateInstance:


    def test_returns_one(self):

        filename: str = "returns_one.py"
        package: str = "tests.player.create_instance"
        class_name: str = "ReturnsOne"

        class_: Type = di.import_class_from_from_file(
            filename, class_name, package
        )
        instance = class_()

        assert instance.returns_one() == 1 


    def test_create_list(self):

        filename: str = "create_list.py"
        package: str = "tests.player.create_instance"
        class_name: str = "CreateList"

        class_: Type = di.import_class_from_from_file(
            filename, class_name, package
        )

        elements = [1, "2", tuple()]
        instance = class_(elements)

        assert instance.get_list() == elements


class TestFilenames:


    def test_filenames_create_instance(self):
        
        filenames = di._get_filenames(Path("tests/player/create_instance/"))
        expected_filenames = [Path("create_list.py"), Path("returns_one.py")]

        assert filenames == expected_filenames


class TestCreatePlayerInstance:


    def test_incorrect_class(self):

        with pytest.raises(NameError):
            di.create_player_class_instance_entire_folder(
                Path("tests/player/players_mock"),
                filenames_to_exclude = set(),
                package = "tests.player.players_mock"
            )


    def test_create_player_instance(self):

        instances: List = di.create_player_class_instance_entire_folder(
            Path("tests/player/players_mock"),
            filenames_to_exclude = {Path("empty_template.py")},
            package = "tests.player.players_mock"
        )

        assert len(instances) == 2

        assert instances[0].function() == 1
        assert instances[1].function() == 2