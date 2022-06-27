import pytest
import src.player.dynamic_imports as di

from pathlib import Path
from typing import Callable, List


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
        