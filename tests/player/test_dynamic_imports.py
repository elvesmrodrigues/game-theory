import pytest
import src.player.dynamic_imports as di

from pathlib import Path


@pytest.fixture
def empty_file(tmp_path_factory: Path):

    temp_dir = tmp_path_factory.mktemp("temp_dir")

    temp_file = temp_dir / "empty_file.py"
    temp_file.write_text("")

    return temp_file


@pytest.fixture
def incorrect_text_file(tmp_path_factory: Path):

    temp_dir = tmp_path_factory.mktemp("temp_dir")

    temp_file = temp_dir / "incorrect_text.py"
    temp_file.write_text("clas Class:")

    return temp_file


class TestGetClassName:


    def test_empty_file(self, empty_file: Path):

        with pytest.raises(NameError):
            di._get_player_class_name(empty_file)


    def test_text_file(self, incorrect_text_file: Path):

        with pytest.raises(NameError):
            di._get_player_class_name(incorrect_text_file)