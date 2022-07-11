from abc import ABC, abstractmethod

from typing import Dict, List, Optional, Tuple, Union
from typing_extensions import Literal

Number = Union[int, float]
PayoffMatrix = Tuple[Tuple[Tuple[Number, ...], ...], ...]
MatchHistoryKey = Tuple[int, str]
MatchHistory = Dict[str, List[Tuple[int, int]]]


class Player(ABC):


    def __init__(self) -> None:
        '''
            It initializes Player Class.
                - Your implementation should inherit from this.
                - You should define a self.name variable (id) to uniquely 
                  identify it. Just copy this __init__ method inside your
                  descendant-class and hardcode it there.
        ''' 
        self.name = "Insert your implementation's name here"
        self.match_history = dict()

        # Do not change this value
        self.robot = False 
    
    @abstractmethod
    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:
        ...
        """
        This is the only function you are required to implement.
        
        --------------------------
        Parameters:

            game_type: str

                Type of the game. 
                (Possible types yet to be defined.)

            payoff_matrix: tuple[tuple[tuple[number, ...], ...], ...]

                Matrix with both your and your adversary's payoff.

                    Consider, for example, the payoff_matrix below:

                                       Col
                                    0      1                    
                                ( 
                        Row  0    ((1,2), (3,4)),
                             1    ((5,6), (7,8))
                                )

                    If you were the row player, you would receive
                    exactly the matrix above. 
                    
                    If, on the other hand, you were the col player 
                    you would receive:

                                      Row
                                    0      1                    
                                ( 
                        Col  0    ((2,1), (6,5)),
                             1    ((4,3), (8,7))
                                )

                    Simply put, you can implement the function as though
                    you were always the row player. Your actions will
                    always be the the "row", your adversary's will always
                    be the "col", and you payoff will always be the first one.

                        Your payoff:
                            payoff_matrix[action][adversary_action][0]

                        Your adversary's payoff:
                            payoff_matrix[action][adversary_action][1]

            adversary_id: str

                Your opponent's name.

            match_history: Optional[dict[str, list[tuple[int, int]]]]

                Dictionary of lists containing the match history between you and 
                your adversary. If there are no matches, its value will be None.

                The possible keys for the dict are: ["all", "row", "col"].

                Each position of the list is a tuple like 
                (your_action, your_adversary_action).

                    If, for example, you want to get the action your adversary
                    played last match, you would just do "match_history[0][1]".

                Symmetric game:
                    There is no distinction between being the row or 
                    col player, so all keys take you to the same match history.

                Asymmetric game:
                    In this case you might want act differently if you are
                    the row or col player. 
                    
                    For instance, if you are the row player, the last time
                    you played you adversary is somewhat ambiguous. It 
                    might refer to the literally last time you played him/her
                    or it might refer to the last time you played against
                    him/her while you were the row player.

                    You can distinguish between these two cases with the keys.
                        "all": will get the entire match_history regardless of 
                                who was the row player and who was the col player. 
                        "row": will only get the matches you were the row player.
                        "col": will only get the matches you were the col player.

                    The information about whether you are the row or col player
                    will be provided (see row_or_col parameter).

            rol_or_col: Literal

                "rol" if you are the row player and "col" otherwise.
                
                Only really useful for asymmetric games (see match_history
                parameter).
            
        --------------------------
        Return:
            action: int
                The action you want to take.
                    On the 2x2 example above, strategy 1 strictly
                    dominates strategy 0. Thus you would just 
                    return the integer 1.
        """


    def __create_key(
        self,
        game_id: int, 
        adversary_id: str
    ) -> MatchHistoryKey:

        """
        It creates the key to the dictionary.
        You should not use or change this function.
        """

        return (game_id, adversary_id)


    def get_match_history(
        self, 
        game_id: int, 
        adversary_id: str
    ) -> Optional[MatchHistory]:

        """
        It returns match_history dictionary at desired position.
        If dictionary said position does not exist, it returns None.
        You should not use or change this function.
        """

        key = self.__create_key(game_id, adversary_id)

        return self.match_history.get(key, None)


    def __create_match_history(
        self, 
        key: MatchHistoryKey, 
        game_symmetric: bool
    ) -> None:
        
        """
        It creates match_history dictionary.
        You should not use or change this function.
        """

        self.match_history[key] = {
            "all": list(), 
            "row": list(),
            "col": list()
        }

        if game_symmetric:
            self.match_history[key]["row"] = self.match_history[key]["all"]
            self.match_history[key]["col"] = self.match_history[key]["all"]


    def __update_match_history(
        self,
        key: MatchHistoryKey,
        game_symmetric: bool,
        row_or_col: str,
        action: int,
        adversary_action: int
    ) -> None:

        """
        It updates match_history dictionary.
        You should not use or change this function.
        """
        actions: Tuple[int, int] = (action, adversary_action)
        
        self.match_history[key]["all"].append(actions)

        if not game_symmetric:
            self.match_history[key][row_or_col].append(actions)


    def update_match_history(
        self, 
        game_symmetric: bool,
        game_id: int,
        adversary_id: str,
        row_or_col: str,
        action: int, 
        adversary_action: int
    ) -> None:

        """
        It creates (if necessary) and updates match_history dictionary.
        You should not use or change this function.
        """

        key = self.__create_key(game_id, adversary_id)
        
        if key not in self.match_history:
            self.__create_match_history(key, game_symmetric)
        
        self.__update_match_history(
            key, game_symmetric, row_or_col, 
            action, adversary_action
        )

    
