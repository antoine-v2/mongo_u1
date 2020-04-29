import os

from . import config, fichier_txt, parametres

def generer_config_files():
    print('generer_config_files')
    if not os.path.isdir(config.params['rep_modeles']):
        print('Le répertoire contenant les modèles de fichiers de conf est introuvable.')
        return
    print('nombre de traitements : {}'.format(len(config.params['traitements'])))
    for traitement in config.params['traitements']:
        un_traitement(traitement)

def un_traitement(data, valeurs_rempl = None):
    print('fonction un_traitement')
    chemin_modele = os.path.join(config.params['rep_modeles'], data['fic_modele'])
    print('chemin_modele : {}'.format(chemin_modele))
    fic_cible = data['fic_cible']
    balise_fic_cible = extraire_balise(fic_cible)
    valeur_balise = int(balise_fic_cible)
    balise_fic_cible = '{{' + balise_fic_cible + '}}'
    # lire le contenu du modèle et générer les "data conf", à partir desquelles on pourra générer le(s) fichier(s)
    data_conf = generer_data_conf(chemin_modele, data)
    # générer les x fichiers voulus (paramètre traitements.nombre)
    for i in range(1, data['nombre']+1):
        print('générer le fichier # {}'.format(i))
        if balise_fic_cible == '':
            chemin_cible = os.path.join(config.params['rep_cible'], data['fic_cible'])
        else:
            fic_cible_tmp = fic_cible.replace(balise_fic_cible, str(valeur_balise))
            valeur_balise += 1
            chemin_cible = os.path.join(config.params['rep_cible'], fic_cible_tmp)
        print('chemin_cible : {}'.format(chemin_cible))
        generer_fichier_cible(chemin_cible, data_conf)

def generer_data_conf(chemin, data):
    liste_data_conf = []
    contenu = fichier_txt.extraire_contenu(chemin)
    for ligne in contenu:
        # créer un bloc par ligne dans le fichier modèle ; tel que traité, cela implique d'avoir une balise maximum par ligne.
        # extraire la balise qui est éventuellement présente dans la ligne du modèle.
        balise = extraire_balise(ligne)
        if balise == '':
            # la ligne dans le fichier de modèle ne contient pas de balise
            bloc = [ligne]
        else:
            # récupérer dans les paramètres, la valeur à donner à cette balise pour le premier fichier à générer.
            valeur_cible_brute = data['balises'][balise]
            # déterminer si cette valeur doit être incrémentée d'un fichier à l'autre (un nombre entier entre double accolades est à incrémenter)
            balise_valeur_cible = extraire_balise(valeur_cible_brute)
            if balise_valeur_cible == '':
                # la ligne contient une balise, dont la valeur sera fixe : la remplacer ici directement
                bloc = [ligne.replace('{{' + balise + '}}', valeur_cible_brute)]
            else:
                prochaine_valeur_cible = int(balise_valeur_cible)
                balise_valeur_cible = '{{' + balise_valeur_cible + '}}'
                bloc = [ligne, '{{' + balise + '}}', valeur_cible_brute, balise_valeur_cible, prochaine_valeur_cible]
        # print('bloc : {}'.format(bloc))
        liste_data_conf.append(bloc)
    return liste_data_conf

def extraire_balise(chaine):
    retour = ''
    debut_balise = chaine.find('{{')
    if debut_balise != -1:
        fin_balise = chaine.find('}}', debut_balise)
        if fin_balise != -1:
            retour = chaine[debut_balise+2:fin_balise]
    return retour

def generer_fichier_cible(chemin_cible, data_conf):
    contenu_fic = []
    premiere_ligne = True
    for elem in data_conf:
        # chaque elem est un "bloc" de type liste ; si plus d'un élément, remplacer une balise par une valeur à incrémenter
        ligne = elem[0]
        if len(elem) == 5:
            valeur_intermediaire = elem[2].replace(elem[3], str(elem[4]))
            elem[4] += 1
            ligne = ligne.replace(elem[1], valeur_intermediaire)
        if premiere_ligne:
            premiere_ligne = False
        else:
            ligne = '\n' + ligne
        contenu_fic.append(ligne)
    fichier_txt.alimenter_fichier(chemin_cible, contenu_fic)