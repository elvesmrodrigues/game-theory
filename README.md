# Game-Theory Tournament

## Introduction

Repository created to run tournaments of known game-theory games, such as Prisoner's Dilemma, Hawk-Dove and Stag-Hunt. 

The main use case should be simples 2-player games in which each player has two actions, but it does support bigger payoff matrices.


## Getting Started

In this repository we used Python 3.7

Creating virtual environment
```
python3 -m venv env
```

Using created environment

```
source env/bin/activate
```

Installing requirements
```
python3 -m install -r requirements.txt
```

## How to use

Simply put, you can create files to represents different player strategies and define what game(s) they will play. 

The tournament can, then, be run by
```
python3 run_tournament.py
```

### Player

In order to create a player strategy you need to create a .py file inheriting from the `Player` class (`src/player/player.py`) and define your own `get_action(<params>)` method. All parameters you will receive are documented in the method definition. 

Some simple examples are provided inside `src/player/`. 

> **Our Tournament:** 
>- To avoid naming conflicts, name you implementation an your python_file something unique that easily identifies you.
>- You can, and probably should, create an strategy for each type of game we are gonna be playing. For instance, you can do so using if-statements or dictionaries mapping the game-type to a function.

### Games

In this context, game refers to a .json file containing:
1. A unique identifier: integer
2. Game type: str
3. Payoff Matrix: lists of lists containing both player's payoffs. Each row represents an action from row-player and each column an action from col-player.

Some examples are provided inside `games/`. 

> **Our Tournament:**
>- Those should be the main types of games (Prisoner's Dilemma, Hawk-Dove and Stag-Hunt) we will be dealing with.
>- Payoff values might change from tournament to tournament,
so you can implement strategies according to payoff-ratios or payoff-value-ranges if you desire.
