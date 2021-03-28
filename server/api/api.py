import sys, os
import logging
import json
from typing import List
import inspect
import flask
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import cross_origin
from pathlib import Path
from server import models as m
from server.api import helper as h


logging.basicConfig(level=logging.DEBUG, filename='api.log', encoding='utf-8')

app = flask.Flask(__name__)

outputPath = str(Path(__file__).parent)

AllModels = m.AllModels.items()

def Setup(port: int):
    logging.info('starting application on port: ' + str(port))
    success = False
    attempts = 0
    while success == False and attempts < 5:
        try:
            app.run(port=port)
            success = True
        except OSError as ose:
            logging.error(ose)
            logging.error('Failed to launch api. Retry attempt ' + str(attempts+1))
            __shutdown_server__()
        except:
            raise RuntimeError('Failed to launch api')
        finally:
            attempts += 1
    

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(500)
def invalid_request(e):
    return e, 500

@app.route('/api/models', methods=['GET'])
@cross_origin()
def getAllModels():
    logging.info('retrieving all models')

    j = list({ 
        'id': key, 
        'value': item.ModelSchema.Description,
        'parameters': item.ModelSchema.ToJson()
        } 
        for key, item in AllModels)

    logging.info('models found: ' + str(j))

    return jsonify(j)
    

@app.route('/api/models/<path:modelName>', methods=['GET'])
@cross_origin()
def getModelDefinition(modelName):
    return __runModel__(modelName, request.query_string.decode(), False)

@app.route('/api/models3d/<path:modelName>', methods=['GET'])
@cross_origin()
def getModelDefinition3d(modelName):
    return __runModel__(modelName, request.query_string.decode(), True)

@app.route('/ping', methods=['GET'])
def ping():
    return 'Server is running...'

@app.route('/shutdown', methods=['GET'])
def shutdown():
    __shutdown_server__()
    return 'Server shutting down...'

def __runModel__(modelName: str, queryString: str, is3d: bool):
    try:
        parameters = h.ParseQueryString(queryString)

        model = dict(AllModels)[modelName]()
        
        if model is None:
            raise ModuleNotFoundError(name=modelName)
        
        graphJson = model.Run(is3d, 'Api', parameters)

        return json.dumps(graphJson)
    except Exception as e:
        return 'failed to run: ' + modelName + '\r\n\t [Trace]: \r\n\t' + str(e), 500

def __shutdown_server__():
    logging.info('attempting to shutdown server')
    try:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is not None:
            func()

    except RuntimeError as e:
        logging.error(e)


if __name__ == '__main__':
    Setup(1400)

    

