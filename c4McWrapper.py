import Evolver
import c4McAi
from config import C4wrapper as config

# Connect 4 Monte Carlo Artificial Intelligence using Genetic Evolution of Neural Nets
# Status: Does not work

if __name__ == '__main__' : Evolver.Queen(c4McAi.C4MCAI, config.display, 0, config.genomes)