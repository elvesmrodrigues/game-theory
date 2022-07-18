from enum import Enum
from typing import Optional
from typing_extensions import Literal
from src.player.player import Player, MatchHistory, PayoffMatrix

from collections import Counter

class Action(Enum):
    COOPERATE: int = 0
    DEFECT: int = 1


class ComplexExampleIf(Player):

    """
        An example a little more complicated than the rest, utilizing 
        different strategies through the use of dictionaries.
    """

    def __init__(self) -> None:
        super().__init__()

        self.name = "Complex Example Dict"

        self.strategy_mapping = {
            "PD": self.__pd_strategy,
            "SH": self.__sh_strategy
        }


    def __pd_strategy(
        self,
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:

        if match_history is None:
            return Action.COOPERATE.value

        # decide strategy looking at the past five actions from your adversary
            # five matches are taken from all the games against adversary
            # .. regardless of whether we are playing as row or as col
        last_adv_actions = [adv_action for _, adv_action in match_history["all"][-5:]]

        if last_adv_actions == []:
            return Action.COOPERATE.value
        
        # similar to a tit_for_tat strategy, replicate the most played strategy by your adversary
        count = Counter(last_adv_actions)
        return max(count, key=count.get)


    def __sh_strategy(
        self,
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:

        # use grim trigger considering only matches played when you
        # ...  were playing the same position (row or col) you are now
        desired_col: str = row_or_col

        if match_history is None or match_history[desired_col] == []:
            return Action.COOPERATE.value
        
        previous_action, adversary_previous_action = match_history[desired_col][-1]

        defected = (previous_action == Action.DEFECT.value)
        adv_defected = (adversary_previous_action == Action.DEFECT.value)

        if defected or adv_defected:
            return Action.DEFECT.value
        
        return Action.COOPERATE.value


    def get_action(
        self, 
        game_type: str, 
        payoff_matrix: PayoffMatrix,
        adversary_id: str,
        match_history: Optional[MatchHistory],
        row_or_col: Literal['row', 'col']
    ) -> int:

        strategy_method = self.strategy_mapping.get(game_type, None)

        if strategy_method is None:
            return Action.COOPERATE.value
        
        return strategy_method(
            payoff_matrix, adversary_id, match_history, row_or_col
        )
        
