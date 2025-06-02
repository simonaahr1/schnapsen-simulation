# Schnapsen
Simulation of the Game Schnapsen

## Requirements

- Python 3.7 or later
- No external libraries required (only standard library is used)
- pip install -r requirements.txt

## Project Overview
This project simulates the traditional card game Schnapsen, focusing on two versions:
1. A random strategy version where players' actions are determined randomly.
2. A strategy version where players follow a more sophisticated set of rules, aiming to play the highest possible card in matching suits to maximize scoring.

## Files
- `random_game.py`: The `SchnapsenRandom` class simulates the game with random moves.
- `strategy_game.py`: Contains the `SchnapsenStrategy` class that implements more strategic gameplay.

## Run the Simulation
- Make sure all files are in the same folder, then run:
python main.py


## Simulation Results

### Random Strategy
The `SchnapsenRandom` class simulated 1000 games where players made decisions randomly. The results were as follows:
- Player 1 wins: 526
- Player 2 wins: 467
- Draws: 7

### Enhanced Strategy
The `Schnapsen` class incorporated strategies such as playing the highest card in the same suit when possible. The simulation of 1000 games yielded:
- Player 1 wins: 481
- Player 2 wins: 515
- Draws: 4

## Key Differences
The strategic version shows a more balanced game dynamic than the random version. We even can see that with the strategy game there are slightly more wins for the second player which presents that the second player is having more advantage 
## Usage
To run a simulation, execute the main.py Python script which will run both simulations:
- python main.py

## Customizing or Extending Strategies

- To implement new strategies, modify or add classes to `strategy_game.py`.
- You can change the number of games simulated by editing the number in `main.py`.

## License

MIT License

## Acknowledgments

This simulation is inspired by the rules of the classic card game Schnapsen.