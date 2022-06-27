from typing import List


class CreateList:

    def __init__(self, elements: List) -> None:
        self.list_: List = elements

    def get_list(self) -> List:
        return self.list_