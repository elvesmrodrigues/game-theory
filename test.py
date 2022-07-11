from nis import match
from random import shuffle, choice
from typing import List

def get_random_matching(players: List[str]) -> list:
    # player always cooperate, or another choosed by the user
    ghost_player = players[0]
    if len(players) % 2:
        players.append(ghost_player)

    shuffle(players)

    matching = list()
    for i in range(len(players) - 1):
        matching.append((players[i], players[i + 1]))

    return matching 

if __name__ == '__main__':
    x = [f'player_{n}' for n in range(5)]

    matching = get_random_matching(x)   
    print(matching)