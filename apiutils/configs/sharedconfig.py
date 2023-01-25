# Contains the shared config in a python file
# Done so that the file is read once and cached for other scripts to use
import os
import json

def load_shared_config():
    # read the json file and convert to dictionary
    shared_config = json.loads( open( os.path.join( os.path.abspath(os.path.split(__file__)[0]), '..', '..',  'shared-linked', 'config.json') ).read() )
    return shared_config

SHARED_CONFIG = load_shared_config()