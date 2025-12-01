#############################################################################
#
#   file: main.py
#   author: Michal Zatecka
#   date: 01.12.2025
#
#############################################################################

import argparse
import sys
from PySide6.QtWidgets import QApplication

from src.fuzzy import REFERENCE_RULES
from src.fuzzy_set import generate_random_rules
from src.genetic_algorithm import Population, Chromosome
from src.gui import ShowerWindow 


parser = argparse.ArgumentParser()
parser.add_argument(
    "-o", "--optimize", 
    action="store_true", required=False, 
    help="Run GA optimization and print best configuration"
)
parser.add_argument(
    "-l", "--load", 
    required=False, type=str, 
    help="Load file with rule configurations"
)
parser.add_argument(
    "-r", "--random", 
    required=False, action="store_true", 
    help="Use random rule configurations"
)


args = parser.parse_args()

if args.optimize:
    # just optimization - only in terminal
    population = Population(100)
    best = population.run(100, True)
    print(best[1].to_string())
elif args.load:
    # load rules config from given file and show gui
    rules = []
    try:
        with open(args.load, "r") as f:
            input_string = f.read().strip()
            c = Chromosome.from_string(input_string)
            rules = c.rules
    except FileNotFoundError:
        print(f"Error: File {args.load} does not exists")
    except ValueError:
        print(f"Error: invalid input")
    app = QApplication(sys.argv)
    win = ShowerWindow(rules)
    win.show()
    sys.exit(app.exec())
elif args.random:
    # use random rules configuration and show gui
    app = QApplication(sys.argv)
    win = ShowerWindow(generate_random_rules())
    win.show()
    sys.exit(app.exec())
else:
    # use reference rules configuration and show gui
    app = QApplication(sys.argv)
    win = ShowerWindow(REFERENCE_RULES)
    win.show()
    sys.exit(app.exec())