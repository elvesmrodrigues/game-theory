from abc import ABC, abstractmethod

from typing import Dict, List, Optional, Tuple, Union


PayoffMatrixType = Dict[str, Dict[str, Union[float, int]]]
MemoryKey = Union[Tuple[int, str, str], Tuple[int, str]]
MatchHistoryType = List[Tuple[str, str]]

class Player(ABC):


    def __init__(self) -> None:
        '''
        memory format: 
        {
            (game_id, adversary_id, available_actions): [(action, adversary_action), ...]
        }
        '''
        self.name = ''        
        self.memory = dict()
    

    @abstractmethod
    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrixType,
        adversary_id: str,
        row_or_col: str
    ) -> str:
        ...


    def __create_key(
        self,
        game_symmetric: bool,
        game_id: int, 
        adversary_id: str, 
        row_or_col: str
    ) -> MemoryKey:

        if game_symmetric:
            return (game_id, adversary_id)

        return (game_id, adversary_id, row_or_col)



    def get_match_history(
        self, 
        game_symmetric: bool,
        game_id: int, 
        adversary_id: str, 
        row_or_col: str
    ) -> Optional[MatchHistoryType]:

        key = self.__create_key(
            game_symmetric, game_id, 
            adversary_id, row_or_col
        )

        return self.memory.get(key, None)


    def update_knowledge(
        self, 
        game_symmetric: bool,
        game_id: int,
        adversary_id: str,
        row_or_col: str,
        action: str, 
        adversary_action: str
    ) -> None:

        key = self.__create_key(
            game_symmetric, game_id, 
            adversary_id, row_or_col
        )
        
        if key not in self.memory:
            self.memory[key] = list()

        self.memory[key].append((action, adversary_action))

    
