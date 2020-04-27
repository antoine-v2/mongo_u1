# imports de modules natifs ou tiers
import logging, os, sys
from datetime import datetime

# imports de modules persos
from app import config, generer_conf, parametres


def bandeau_demarrage():
    print('\n================================================================================================')
    print('========================= ' + config.appli_nom + ' - v' + config.appli_version + ' - ' + config.appli_date + ' ========================')
    print('================================================================================================')

def initialiser_log():
    nom_fic_log = 'log_{}.txt'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    chemin_fic_log = os.path.join(config.log_path, nom_fic_log)
    formatter = logging.Formatter("%(asctime)s %(module)s %(funcName)s %(message)s")
    handler = logging.FileHandler(chemin_fic_log, mode="a", encoding="utf-8")
    handler.setFormatter(formatter)
    config.logger = logging.getLogger("outil MongoDB")
    config.logger.setLevel(logging.DEBUG)
    config.logger.addHandler(handler)
    config.logger.debug("{} ; log initialisé.".format(config.appli_nom))

# initialiser l'application    
def ini_appli(liste_args):
    
    if (len(liste_args) != 2):
        info_args()
        return False

    if getattr(sys, 'frozen', False):
        # exécutable
        config.forme = 'exe'
        config.root_path = os.path.join('..', '..')
    else:
        # code python
        config.forme = 'python'
        config.root_path = '.'
    print('config.root_path : {}'.format(config.root_path))

    config.log_path = os.path.join(config.root_path, 'log')
    print('config.log_path : {}'.format(config.log_path))
    initialiser_log()

    if not os.path.isfile(liste_args[1]):
        config.logger.critical("fichier de paramètres introuvable")
        return False
    config.chemin_fic_param = liste_args[1]

    parametres.lire_fic_param()
    return True

def info_args():
    print('aide sur le script :')
    print('arguments attendus :')
    print('    1 : chemin du fichier de paramètres')
    print('\n---------------- utilisation du script à l\'état de script Python (fichier .py) :')
    print('    python .\\main.py ..\\param.json')

def main(liste_args):
    bandeau_demarrage()
    print('exécution : {}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    if ini_appli(liste_args) :
        generer_conf.generer_config_files()

if __name__ == "__main__":
    main(sys.argv)