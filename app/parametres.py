import json

from . import config

def lire_fic_param():
    with open(config.chemin_fic_param) as f:
        config.params = json.loads(f.read())