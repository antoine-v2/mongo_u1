# module de gestion de fichiers texte
from . import config


def extraire_contenu(chemin_fic):
    contenu = []
    try:
        with open(chemin_fic, 'r') as fic_src:
            contenu_brut = fic_src.read()
            contenu = contenu_brut.split('\n')
    except FileNotFoundError:
        config.logger.debug('!! fichier_txt.extraire_contenu()    fichier introuvable.')
    return contenu

# créer un fichier
def initialiser_fichier(chemin_fic):
    try:
        with open(chemin_fic, 'w'):    
            pass
    except FileNotFoundError:
        config.logger.debug('!! fichier_txt.extraire_contenu()    fichier introuvable.')

# écrire des données dans un fichier texte
def alimenter_fichier(chemin_fic, donnees):
    try:
        with open(chemin_fic, 'w') as fic:  
            for elem in donnees:
                fic.write(elem)
    except FileNotFoundError:
        config.logger.debug('!! fichier_txt.extraire_contenu()    fichier introuvable.')

def alimenter_fichier_chaine(chemin_fic, chaine):
    try:
        # with open(chemin_fic, 'w') as fic:
        with open(chemin_fic, 'a') as fic:
            fic.write(chaine + '\n')
    except FileNotFoundError:
        config.logger.debug('!! fichier_txt.extraire_contenu()    fichier introuvable.')

# écrire une chaîne dans le fichier de retour
def ecrire_retour(chaine):
    alimenter_fichier_chaine(config.chemin_fic_retour, chaine)