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

  `python main_CACM.py
  `


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
  - **main_cs276.py** : l'analyse du second corpus de Stanford et la création d'un index inversé sur ce dernier avec le paradigme map reduce
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


  >Réponse obtenue dans un terminal lors d'un test:

  >QUESTION 1: Nombre de tokens dans CACM: 153338

  >QUESTION 2: Taille du vocabulaire : 8190

  >QUESTION 3
  Valeur de b estimée:  0.4876
  Valeur de k estimée: 24

  >QUESTION 4: Si on a 1 million de tokens, on peut estimer la taille du vocabulaire a 20436

  >QUESTION 5: Chargement des graphs


![alt text](CACM.png)

Pour le corpus CS 276 on obtient les résultats suivants:

  >QUESTION 1: Nombre de tokens dans CS276: 25 626 660

  >QUESTION 2:
  >Taille du vocabulaire : 335 917

  >Valeur de b estim2e:  0.7180

  >Valeur de k estimée: 1

  >QUESTION 4: Si on a 1 million de tokens, on peut estimer la taille du vocabulaire a 32718

## <a name="bool"></a>3. Moteur de recherche booléen

Le moteur de recherche booléen prend des inputs sous la forme normale conjonctive : a|b&c.

On trouvera ce moteur de recherches sous main_bool.py.

On donne un exemple de recherche effectuée dans le terminal avec l'algorithme booléen:

>#########  Recherche Booleenne dans le corpus CACM ###############

>Que cherchez-vous ? (format attendu sous la forme normale conjonctive: a|b&c)"square&root"


>############ RELEVANT WORK FOUND IN CACM in 0.00109 sec ######################

>A Note on Range Transformations for Square Root and Logarithm

>Starting Approximations for Square Root Calculation on IBM System/360

>The Logarithmic Error and Newton's Method for the Square Root

>Optimal Starting Approximations for Generating

>Jump Searching: A Fast Sequential Search Technique


## 4. <a name="vect"></a>Moteur de recherche vectoriel

Le moteur de recherche vectoriel utilise la mesure de similarité cosinus entre la requête et les documents.

Les méthodes implémentées pour mesurer la similarité sont les suivantes:
- tf_idf
- tf_idf normalisé (appelé ntf_idf ici)
- Fréquence normalisée (maxfreq)

On donne un exemple de recherche effectuée dans le terminal avec l'algorithme vectoriel:

>Initialisation et analyse du corpus...merci de patienter

>Indexation en 2.4 sec

>Quelle methode souhaitez-vous utiliser pour la recherche vectorielle ? (tf_idf,ntf_idf,maxfreq)"tf_idf"

>Que cherchez-vous ? (une liste de mots)"optimization of square root computation on a computer"

>############ TOP 10 RELEVANT WORK FOUND IN CACM in 0.5 sec ######################

>A Proposal for Input-Output Conventions in ALGOL

>The Secant Method for Simultaneous Nonlinear Equations

>Some Experiments in Algebraic Manipulation by Computer

>A Note on Starting the Newton-Raphson Method

>Method for Hyphenating at the End of a Printed Line

>Algorithms SCALE1, SCALE2, and SCALE3 for Determination

>Monitors: An Operating System Structuring Concept

>Applications of Differential Equations in General Problem Solving

>Increasing the Efficiency of Quicksort

>Ancient Babylonian Algorithms


# Evaluation sur le corpus CACM avec tf_idf

L'évaluation de la pertinence des résultats du moteur vectoriel se fait dans main_pertinence.py

On récupère à chaque fois les 10 premiers documents renvoyés par l'algo.

La durée moyenne d'une requête est de l'ordre de 0.50 seconde.

Ce script déclenchera une chaine d'évaluations du type:

>################ Corpus analysis #################

>Corpus analyzed and indexed in 1.350 secs

>################# Queries ####################

>Calcul en cours de 1/64

>Calcul en cours de 2/64

>Calcul en cours de 3/64

>...

Pour l'évaluation de la pertinence de nos résultats, on tient compte:
- Du temps (l'initialisation du corpus CACM prend généralement 1 sec,les recherches y sont quasiment instantanées)
- De la précision
- Du rappel

La courbe rappel précision obtenue en moyenne sur les recherches données en exemple est la suivante (chaque point est une moyenne sur un seuil particulier)

Graphique lorsque l'on regarde uniquement les 10 premiers articles renvoyés (on a donc au max 9 seuils) par le module :

![alt text](pc10.png)

Au contraire lorsque l'on regarde *tous* les résultats (3203 seuils):

![alt text](pc.png)

NOTA BENE: Les valeurs suivantes ne sont pas présentes dans le fichier qrel.text pour juger de la pertinence de nos requêtes:
34,35,41,46,47,50,51,52,53,54,55,56. Dans ce cas là on indique que les fichiers pertinents pour cette requêtes étaient l'ensemble vide [].
