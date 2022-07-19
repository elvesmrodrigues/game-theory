# Game-Theory Tournament

## Introduction

Repository created to run tournaments of known game-theory games, such as Prisoner's Dilemma, Hawk-Dove and Stag-Hunt. 

The main use case should be simple 2-player games in which each player has two actions, but it does support bigger payoff matrices.


## Getting Started

In this repository we use Python 3.7

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

Simply put, you can create files to represent different player strategies and define what game(s) they will play. 

The tournament can, then, be run by
```
python3 run_tournament.py
```

## Auto set up

If you don't want to clone the project and run it on your machine, you can run it with [replit](https://replit.com/), where everything is already set up for you:

- Go to [https://replit.com/@gametheory/tournament](https://replit.com/@gametheory/tournament)
- Click in the button **Fork Repl**
- Click on the tab **Shell**
- Run the tournament, by typing: `python3 run_tournament.py` 
    > Prefer to use the shell. The RUN button does not work because of an internal dependency conflict in the site modules.

### Player

In order to create a player strategy you need to create a .py file inheriting from the `Player` class (`src/player/player.py`) and to define your own `get_action(<params>)` method. All parameters you will receive are documented in the method definition. 

Some simple examples are provided inside `players/`. 
Implementations should be added inside this folder.

> **Our Tournament:** 
>- To avoid naming conflicts, name you implementation and your python_file something unique that easily identifies you.
>- You can, and probably should, create a strategy for each type of game we are gonna be playing. For instance, you can do so using if-statements or dictionaries mapping the game-type to a function.
>- You can assume, as can be seen in some examples, that cooperating will be action 0 and defecting will be action 1. Let's take this as a convention for our tournaments.

### Games

In this context, game refers to a .json file containing:
1. A unique identifier: integer
2. Game type: str
3. Payoff Matrix: lists of lists containing both player's payoffs. Each row represents an action from row-player and each column an action from col-player.

Some examples are provided inside `games/`. 
If you want to add more games, they should be added inside this folder.

> **Our Tournament:**
>- The two types of games we will be dealing with are PD (Prisoner's Dilemma) and SH (Stag-Hunt).
>- Payoff values might change from tournament to tournament,
so you can implement strategies according to payoff-ratios or payoff-value-ranges if you desire.

## Configuration file

If you want to change some parameters, like the type of tournament or remove some Player, you can change the `configuration.json` file.

### Player

1. **dir** -> folder with player-strategy implementations (there really isn't any reason to change this)
2. **files_to_ignore** -> player strategies which should not be dynamically imported. For instance, if you don't want "players/random_player.py" to take part in the tournament, you should add "random_player.py" to this list.

### Game

1. **dir** -> folder with payoff matrices, i.e., .json files (there really isn't any reason to change this)
2. **files_to_ignore** -> games which should be ignored. For instance, if you don't want "games/stag_hunt.json" to take part in the tournament, you should add "stag_hunt.json" to this list.

### Tournament
1. **min_number_of_rounds** -> minimum number of rounds of the tournament for one game. Each round is somewhat equivalent to the number of games a round-robin tournament would have.
2. **max_number_of_rounds** -> minimum number of rounds of the tournament for one game. Each round is somewhat equivalent to the number of games a round-robin tournament would have.
3. **matching_strategy** -> type of the tournament
    - "complete": round-robin 
        - each team face each other as row and as col player once for round
    - "random": randomized round-robin 
        - besides playing the same number of games per round, there is no restriction, i.e. teams can face each other many times in a row
        - if there are an odd number of players, a copy of another randomly selected player will be chosen to complete the round (this copy does not show up in the final ranking)
4. **time_to_take_action** -> maximum time your `get_action` implementation can take to make a choice. If time is exceeded, a random action shall be chosen.
4. **time_between_ranking_shows** -> sleep "time_between_ranking_shows" after refreshing the real-time ranking in the terminal 
6. **print_ranking_after_n_rounds** -> change if you want to print the ranking after every n rounds rather than after every round. 
7. **match_logs_dir** -> directory in which all matches' results will be saved
8. **ranking_filename** -> filename of the final ranking for a tournament (it can overwrite itself for different tournaments, so be careful)
9. **debug_mode** -> Boolean indicating whether logs should be shown on the screen or not.
