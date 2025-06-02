import random
from random_game import SchnapsenRandom
from strategy_game import SchnapsenStrategy

# Create an instance of the Schnapsen Random class and simulate 1000 games
schnapsen_rand = SchnapsenRandom()
results = schnapsen_rand.simulate_games(1000)
print(f'Random Results{results}')

# Create an instance of the Schnapsen Strategy class and simulate 1000 games
schnapsen_strategy = SchnapsenStrategy()
results = schnapsen_strategy.simulate_games(1000)
print(f'Strategy Results{results}')