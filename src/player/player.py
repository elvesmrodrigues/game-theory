from abc import ABC, abstractmethod

from typing import Dict, List, Optional, Tuple, Union


PayoffMatrixType = Dict[str, Dict[str, Union[float, int]]]
MemoryKey = Tuple[int, str, Tuple[str, ...]]
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
        available_actions: Tuple[str, ...],
        adversary_available_actions: Tuple[str, ...]
    ) -> str:
        ...


    def get_match_history(
        self, 
        game_id: int, 
        adversary_id: str, 
        available_actions: Tuple[str, ...]
    ) -> Optional[MatchHistoryType]:

        key: MemoryKey = (game_id, adversary_id, available_actions)

        return self.memory.get(key, None)


    def update_knowledge(
        self, 
        game_id: int,
        adversary_id: str,
        available_actions: Tuple[str, ...], 
        action: str, 
        adversary_action: str
    ) -> None:

        key: MemoryKey = (game_id, adversary_id, available_actions)
        
        if key not in self.memory:
            self.memory[key] = list()

        self.memory[key].append((action, adversary_action))

    
