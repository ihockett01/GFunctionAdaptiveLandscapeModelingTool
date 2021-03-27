# import sys, os
# import logging
# import json
# import inspect
# import argparse
# from pathlib import Path
# from .. import models as m
# from . import helper as h
# from typing import List

# parser = argparse.ArgumentParser(description='Execute a given g-function model to create an adaptive landscape graph')
# parser.add_argument(
#     'model_name', 
#     type=str, 
#     choices=['DrugResistance', 'Evolvability', 'OnePrey', 'TwoPrey'],
#     help='The name of the model to use')
# parser.add_argument('-3d', '--is3d', type=bool, default=False, help='Whether to generate a 3d model')
# parser.add_argument('-a', '--animate', type=bool, default=False, help='Animate the graph when initially displaying')

# logging.basicConfig(level=logging.DEBUG)
# outputPath = str(Path(__file__).parent)

# AllModels = m.BaseModelsSchema.AllModels.items()
# argumentList = parser.parse_known_args()

# print(argumentList)