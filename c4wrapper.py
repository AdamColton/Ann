import Evolver
import c4Ai
from config import C4wrapper as config

if __name__ == '__main__' : Evolver.Queen(c4Ai.C4AI, config.display, config.cores, config.genomes, config.genomeInitialScore)