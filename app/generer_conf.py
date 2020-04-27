import os, shutil

from . import config, fichier_txt, parametres

def generer_config_files():
    print('generer_config_files')
    
    if not os.path.isdir(config.params['rep_modeles']):
        print('Le répertoire contenant les modèles de fichiers de conf est introuvable.')
        return

    # boucler sur les traitements
    print('nombre de traitements : {}'.format(len(config.params['traitements'])))
    nouv_valeurs = None
    for traitement in config.params['traitements']:
        un_traitement(traitement)

def un_traitement(data, valeurs_rempl = None):
    print('fonction un_traitement')
    chemin_modele = os.path.join(config.params['rep_modeles'], data['fic_modele'])
    print('chemin_modele : {}'.format(chemin_modele))
    chemin_cible = os.path.join(config.params['rep_cible'], data['fic_cible'])
    print('chemin_cible : {}'.format(chemin_cible))
    # shutil.copy(chemin_modele, chemin_cible)
    # lire le contenu du modèle



    # générer les x fichiers voulus (paramètre traitements.nombre)
    for i in range(1, data['nombre']+1):
        print('générer le fichier # {}'.format(i))

def data_conf(chemin):
    liste_data_conf = []
    contenu = fichier_txt.extraire_contenu(chemin)
    for ligne in contenu:
        bloc = ['', '', '', False]
        liste_data_conf.append(bloc)   
    return liste_data_conf

def extraire_balise(chaine):
    return ''

def generer_fichier_cible():
    pass