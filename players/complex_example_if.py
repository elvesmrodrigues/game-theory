from enum import Enum
from typing import Optional
from typing_extensions import Literal
from src.player.player import Player, MatchHistory, PayoffMatrix


class Action(Enum):
    COOPERATE: int = 0
    DEFECT: int = 1


class ComplexExampleIf(Player):

    """
        An example a little more complicated than the rest, utilizing 
        different strategies through the use of if statements.
    """

    def __init__(self) -> None:
        super().__init__()

        self.name = "Complex Example If Statement"


    def __pd_strategy(
        self,
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:

        # if you get way too much for defecting, defect
            # payoff_matrix[0][0] is the payoff tuple (row, col) 
            # ... if row plays COOPERATE and col players COOPERATE
            # similarly payoff_matrix[0][0] is the payoff tuple (row, col) 
            # ... if row plays DEFECT and col players COOPERATE
        # since we can assume we are the row player, we take the first position
        if 10*payoff_matrix[0][0][0] <= payoff_matrix[1][0][0]:
            return Action.DEFECT.value

        return Action.COOPERATE.value


    def __sh_strategy(
        self,
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:

        return Action.COOPERATE.value


    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:


        if game_type == "PD":
            return self.__pd_strategy(
                payoff_matrix, adversary_id, match_history, row_or_col
            )

            
        if game_type == "SH":
            return self.__sh_strategy(
                payoff_matrix, adversary_id, match_history, row_or_col
            )

        return Action.COOPERATE.value

        