import sys, os, logging
from server.api import api

def run():
    logging.info('Running application from cli')
    port = 1400

    try:
        port = int(sys.argv[1:][0])
    except:
        print('nope')
        # nope

    api.Setup(port)

if __name__ == 'main':
    run()

run()