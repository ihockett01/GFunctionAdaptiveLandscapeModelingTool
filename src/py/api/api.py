import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'models'))

import flask
from flask import request, jsonify, send_from_directory

from pathlib import Path

app = flask.Flask(__name__)
app.config["DEBUG"] = True

outputPath = str(Path(__file__).parent)

@app.route('/', methods=['GET'])
def home():
    return 'API for PACC G-Function Modelling'


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/models/run/{modelName}?p={parameters}', methods=['GET'])
def runModel(modelName, parameters):
    #TODO: Find Model
    #TODO: Instantiate Model
    #TODO: Run Model

    return ''

app.run()
    #TODO: Add in all required parameters

    # missingParams = checkParams(['pop1', 'pop2', 'strat1', 'strat2'], request.args)
    
    # if missingParams:
    #     return 'Missing parameters: ' + ','.join(missingParams), 400

    # pop1 = int(request.args['pop1'])
    # pop2 = int(request.args['pop2'])
    # strat1 = int(request.args['strat1'])
    # strat2 = int(request.args['strat2'])

    # drugResistance = dr.Model(pop1, pop2, strat1, strat2, outputPath)
    # filename = drugResistance.run()
    # return filename
    # return send_from_directory()

    # return jsonify({'pop1': request.args['pop1'], 'pop2': request.args['pop2']})

# @app.route('/api/models/Evolvability3D', methods=['GET'])
# def evolvability3D():
#     #TODO: Add in all required parameters
    
#     missingParams = checkParams(['pop1', 'pop2'], request.args)
    
#     if missingParams:
#         return 'Missing parameters: ' + ','.join(missingParams), 400

#     return jsonify({'pop1': request.args['pop1'], 'pop2': request.args['pop2']})

# @app.route('/api/models/OnePrey', methods=['GET'])
# def onePrey():
#     #TODO: Add in all required parameters
    
#     missingParams = checkParams(['pop1', 'pop2'], request.args)
    
#     if missingParams:
#         return 'Missing parameters: ' + ','.join(missingParams), 400

#     return jsonify({'pop1': request.args['pop1'], 'pop2': request.args['pop2']})

# @app.route('/api/models/TwoPrey', methods=['GET'])
# def twoPrey():
#     #TODO: Add in all required parameters
    
#     missingParams = checkParams(['pop1', 'pop2', 'pop3'], request.args)
    
#     if missingParams:
#         return 'Missing parameters: ' + ','.join(missingParams), 400

#     return jsonify({'pop1': request.args['pop1'], 'pop2': request.args['pop2']})

# def checkParams(expected, actual):
#     missingParams = []
#     for a in expected:
#         if not a in actual:
#             missingParams.append(a)

#     return missingParams

