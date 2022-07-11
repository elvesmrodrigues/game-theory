from typing import Any, List, Tuple, Union
from typing_extensions import TypedDict

from src.game.game import nested_list_to_nested_tuple, transpose_list_of_lists, GameFactoryFromJson

Number = Union[float, int]
PayoffMatrix = Tuple[Tuple[Tuple[Number, ...], ...], ...]

class GameDict(TypedDict):
    id: int 
    type: str 
    payoff_matrix: PayoffMatrix

class TestNestedListToNestedTuple:

    def test_empty_list(
        self) -> None:
        
        empty_list: List[Any] = [] 
        res: Tuple[Any] = nested_list_to_nested_tuple(empty_list)

        assert type(res) is tuple
        assert len(res) == 0

    def test_list_with_values(self) -> None:
        numbers: List[Number] = [1, 2, 3, 5]
        res: Tuple[Number] = nested_list_to_nested_tuple(numbers)

        assert len(res) == len(numbers)

        assert numbers[0] == res[0]
        assert numbers[1] == res[1]
        assert numbers[2] == res[2]
        assert numbers[3] == res[3]

    def test_2x2_payoff_matrix(self) -> None:
        payoff_matrix: List[List[Number]] = [
                                    [[4,4], [0,5]],
                                    [[5,0], [1,1]]
                                ]

        res: Tuple[Tuple[Number]] = nested_list_to_nested_tuple(payoff_matrix)
        expected_response: Tuple[Tuple[Number]] = (
            ((4,4),(0,5)),
            ((5,0),(1,1))
        )

        assert res == expected_response

class TestTransposeListOfList:
    def test_empty_list(self) -> None:
        empty_list: List[Any] = []
        res: List[Any] = transpose_list_of_lists(empty_list)

        assert empty_list == res 

    def test_transpose_2x2_payoff_matrix(self) -> None:
        payoff_matrix: List[List[Number]] = [
                            [[4,4], [0,5]],
                            [[5,0], [1,1]]
                        ]
                
        expected_response: List[List[Number]] = [
                            [[4, 4], [5, 0]], 
                            [[0, 5], [1, 1]]
                        ]

        assert transpose_list_of_lists(payoff_matrix) == expected_response

class TestGameFactoryFromJson:
    def test_create_game(self) -> None:
        game_dict: GameDict = {
                        "id": 0, 
                        "type": "PD",
                        "payoff_matrix": [
                            [[4,4], [0,5]],
                            [[5,0], [1,1]]
                        ]
                    }        

        game = GameFactoryFromJson().create_game(game_dict) 
        
        payoff_matrix: PayoffMatrix = (
                    ((4, 4), (0, 5)), 
                    ((5, 0), (1, 1))
                )

        assert game.id == game_dict['id']
        assert game.type == game_dict['type']
        assert game.symmetric
        assert game.payoff_matrix == game_dict["payoff_matrix"]
        assert game.payoff_row == payoff_matrix
        assert game.payoff_col == payoff_matrix
        