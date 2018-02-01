<h1 align='center'> Projet RI Web </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Janvier 2017 <hr></i></p>

__Auteur__ : Eymard Houdeville<br>

## Index
1. [Description](#description)
2. [Initialisation et analyse des corpus](#init)
3. [Moteur de recherche booléen](#bool)
4. [Moteur de recherche vectoriel](#vect)
5. [Mesures de performance et de pertinence](#perf)

Pour lancer le projet il suffit de git clone le repo et de lancer l'un des scripts main en ligne de commande:

"""
python main_CACM.py
"""

L'ensemble des consignes du projet est disponible dans le document pdf "Projet_2017_2018".

## <a name="description"></a>1. Description

Le projet a pour objectif de construire un index inversé sur deux corpus de textes:
- CACM
- CS276

**Hypothèse**: On fait l'hypothèse que les deux corpus tiennent en mémoire.

Cet index inversé doit ensuite être utilisé pour implémenter différents types de modèles de recherche vus en cours:
- Des variantes du modèle vectoriel
- Le modèle booléen

L'arborescence du projet est la suivante:

- **Projet** Permet de lancer les différentes fonctions Main qui répondent aux différentes parties du projet
  - **main_CACM.py** : les réponses aux premières questions avec notamment une analyse du vocabulaire, du nombre de tokens ou de la loi de Zipf
  - **main_cs276.py** : l'analyse du second corpus de Stanford
  - **main_bool.py** : le script pour lancer le moteur de recherche booléen sur CACM
  - **main_vect.py** : le script pour lancer le moteur de recherche vectoriel sur CACM
  - **main_pertinence.py** : le script pour lancer le mesure de la performance du moteur vectoriel

-  **Lib** est le dossier "père" contenant :
    - **boolean_motor.py** Le moteur de recherche booléen
    - **vect_motor.py**  Le moteur de recherche vectoriel
    - **utils_CACM.py** Les fonctions utilisées pour l'indexation du corpus CACM
    - **utils_cs276.py** Les fonctions utilisées pour l'indexation du corpus CS 276 de Stanford
    - **utils_pertinence.py** Les fonctions utilisées pour la mesure de la pertinence des résultats des précédents moteurs


## <a name="init"></a>2. Initialisation et analyse des corpus

Nous reproduisons ici les courbes de Zipf que nous affichons en paramètrant la valeur PLOT_GRAPH à True dans nos classes d'analyse des corpus.

## <a name="bool"></a>3. Moteur de recherche booléen

Le moteur de recherche booléen prend des inputs sous la forme normale conjonctive : a|b&c.

## 4. <a name="vect"></a>Moteur de recherche vectoriel

Le moteur de recherche vectoriel utilise la mesure de similarité cosinus entre la requête et les documents.

## 4. <a name="pert"></a>Mesure de la performance et de la pertinence

Les valeurs suivantes ne sont pas présentes dans le fichier qrel.text pour juger de la pertinence de nos requêtes:
34,35,41,46,47,50,51,52,53,54,55,56. Dans ce cas là on indique que les fichiers pertinents pour cette requêtes étaient l'ensemble vide [].
