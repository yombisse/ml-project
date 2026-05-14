# Choix des algorithmes

## 1. But du document

Ce document explique simplement :

- pourquoi ces algorithmes ont ete choisis
- comment ils sont implementes dans le projet
- comment l'entrainement est effectue
- comment le systeme sait quoi faire a chaque etape
- quelle logique a ete suivie pour comparer les resultats

L'objectif est de rendre la partie "modeles de machine learning" facile a comprendre, meme pour quelqu'un qui ne connait pas encore tous les details du code.

## 2. Pourquoi plusieurs algorithmes ont ete utilises

Le sujet du projet ne demande pas un seul modele, mais une **comparaison de plusieurs algorithmes de classification**.

L'idee derriere cela est simple :

- un seul modele ne suffit pas pour dire qu'on a cherche la meilleure solution
- chaque algorithme a sa propre maniere d'apprendre
- certains modeles sont simples et interpretables
- d'autres sont plus puissants mais plus complexes

Le but n'est donc pas seulement de "faire tourner de l'IA", mais de **comparer des approches differentes** sur le meme jeu de donnees.

## 3. Les algorithmes retenus dans le projet

Les modeles utilises sont :

1. Logistic Regression
2. K-Nearest Neighbors
3. Support Vector Machine
4. Decision Tree
5. Random Forest
6. AdaBoost

Ces algorithmes ont ete gardes parce qu'ils sont exactement ceux demandes dans le sujet.

## 4. Logique derriere le choix de chaque algorithme

### 4.1 Logistic Regression

Ce modele est souvent utilise comme base de reference en classification binaire.

Pourquoi il est utile :

- il est simple
- il est rapide
- il fonctionne bien sur beaucoup de petits jeux de donnees
- il donne une bonne base de comparaison

Dans ce projet, il sert de modele de reference serieux.

### 4.2 K-Nearest Neighbors

Ce modele compare un patient a des patients proches dans les donnees.

Pourquoi il est interessant :

- il est intuitif
- il repose sur la notion de similarite
- il reagit bien lorsque les donnees sont bien preparees

Mais il est sensible a l'echelle des variables.  
C'est pour cela que la standardisation a ete integree dans le pipeline.

### 4.3 Support Vector Machine

Le SVM cherche une separation optimale entre les classes.

Pourquoi il est utile :

- il peut etre tres performant sur des datasets de petite ou moyenne taille
- il gere bien les separations complexes

Dans ce projet, il permet de tester une approche plus mathematique et plus puissante que les modeles les plus simples.

### 4.4 Decision Tree

L'arbre de decision prend des decisions par regles successives.

Pourquoi il est interessant :

- il est facile a comprendre
- il est interpretable
- il apprend des regles simples du type : "si telle variable depasse tel seuil"

Il est utile pour comparer un modele interpretable avec des modeles plus performants mais moins lisibles.

### 4.5 Random Forest

Le Random Forest est un ensemble de plusieurs arbres.

Pourquoi il est utile :

- il est souvent plus stable qu'un arbre unique
- il reduit le risque de surapprentissage
- il donne souvent de bons resultats en pratique

Dans ce projet, il sert a representer les methodes d'ensemble robustes.

### 4.6 AdaBoost

AdaBoost est aussi une methode d'ensemble, mais avec une logique differente.

Pourquoi il est interessant :

- il construit plusieurs petits modeles successifs
- il insiste progressivement sur les cas difficiles
- il peut donner de tres bons resultats sur certains problemes

Dans ce projet, il permet de tester une autre logique d'amelioration progressive des predictions.

## 5. Pourquoi ces 6 modeles forment un bon ensemble de comparaison

Les 6 modeles ne sont pas la par hasard.  
Ils couvrent plusieurs grandes familles d'approches :

- modele lineaire : Logistic Regression
- modele par voisinage : KNN
- modele a marge : SVM
- modele a regles : Decision Tree
- modele d'ensemble par arbres : Random Forest
- modele d'ensemble adaptatif : AdaBoost

Cela rend la comparaison plus riche, car on ne compare pas six variantes presque identiques, mais six manieres differentes d'apprendre.

## 6. Ou les algorithmes sont implementes dans le projet

La logique des modeles est centralisee dans :

- `src/models.py`
- `config.yaml`

### Role de `config.yaml`

`config.yaml` contient :

- les noms des modeles
- leurs hyperparametres
- les chemins utiles
- les parametres d'evaluation

Cela permet d'eviter de mettre toutes les valeurs "en dur" dans le code.

### Role de `src/models.py`

Ce fichier lit la configuration et cree les modeles scikit-learn correspondants.

Autrement dit :

- `config.yaml` dit **quoi utiliser**
- `src/models.py` dit **comment le construire**

## 7. Comment le systeme sait quel algorithme creer

Dans `src/models.py`, une fonction cree un dictionnaire de modeles.

La logique ressemble a ceci :

1. charger la configuration
2. lire les hyperparametres de chaque modele
3. instancier chaque algorithme scikit-learn
4. stocker chaque modele dans une structure commune

Exemple de logique :

- `logistic_regression` devient un objet `LogisticRegression(...)`
- `knn` devient un objet `KNeighborsClassifier(...)`
- `svm` devient un objet `SVC(...)`

Ainsi, le systeme ne "devine" pas les algorithmes tout seul.  
Il suit la logique definie explicitement dans le projet.

## 8. Comment l'IA "sait" comment faire l'entrainement

Ici, il faut bien comprendre une chose :

Le projet n'utilise pas une IA qui invente sa propre methode toute seule.  
Le systeme suit un **pipeline programme a l'avance**.

Autrement dit :

- nous definissons les etapes
- le code execute ces etapes automatiquement

La logique est la suivante :

1. charger les donnees
2. nettoyer les donnees
3. preparer les variables
4. diviser les donnees en train/test
5. construire les pipelines
6. entrainer les modeles
7. calculer les scores
8. comparer les resultats
9. choisir le meilleur modele
10. sauvegarder les artefacts

Donc l'IA n'improvise pas.  
Elle apprend en suivant la structure qu'on lui a imposee.

## 9. Pourquoi un pipeline a ete utilise

Le pipeline est un element tres important du projet.

Il permet d'enchainer automatiquement :

- le pretraitement
- puis le modele

Dans ce projet, chaque algorithme est encapsule dans un pipeline qui contient :

1. le preprocesseur
2. le classifieur

Exemple logique :

```text
donnees brutes
-> imputation
-> encodage / standardisation
-> modele
-> prediction
```

Ce choix est important car il garantit que les memes transformations sont appliquees :

- pendant l'entrainement
- pendant l'evaluation
- pendant la prediction finale dans Streamlit

## 10. Comment les donnees sont preparees avant l'entrainement

Avant qu'un algorithme puisse apprendre, les donnees doivent etre preparees.

Dans ce projet :

- les valeurs manquantes sont gerees par imputation
- les variables numeriques sont standardisees
- les variables categorielles sont encodees
- la cible est binarisee

Pourquoi cela est important :

- certains modeles ne supportent pas les valeurs manquantes
- certains modeles ont besoin de variables mises a l'echelle
- les categories doivent etre converties dans un format exploitable

## 11. Pourquoi tous les modeles ne sont pas traites "a la main" un par un

Plutot que de coder 6 scripts differents, le projet suit une logique modulaire :

- une fonction cree tous les modeles
- une autre construit tous les pipelines
- une autre les entraine
- une autre les evalue

Avantages :

- moins de repetition
- code plus propre
- plus facile a maintenir
- plus simple a expliquer

## 12. Comment l'entrainement est effectue concretement

L'entrainement suit une logique tres claire.

### 12.1 Separation des donnees

Le dataset est separe en deux parties :

- jeu d'entrainement
- jeu de test

Le jeu d'entrainement sert a apprendre.  
Le jeu de test sert a verifier la qualite finale.

### 12.2 Validation croisee

Avant de retenir un modele, on fait une validation croisee sur les donnees d'entrainement.

Cela signifie qu'on coupe les donnees plusieurs fois pour tester la stabilite du modele.

Pourquoi c'est utile :

- cela donne une evaluation plus fiable
- cela evite de juger un modele sur un seul decoupage

### 12.3 Entrainement final

Une fois la comparaison faite, chaque modele est entraine sur le jeu d'entrainement complet.

Ensuite :

- on calcule les metriques sur le jeu de test
- on compare les scores
- on retient le meilleur modele selon la logique choisie

## 13. Comment le meilleur modele est choisi

Le meilleur modele n'est pas choisi au hasard.

La logique retenue est :

- comparaison principale sur la validation croisee
- critere principal : `roc_auc`

Pourquoi ce choix :

- l'AUC-ROC donne une vision globale de la capacite de separation
- elle est tres utile quand on veut comparer plusieurs modeles de classification

Une fois ce meilleur modele identifie :

- il est sauvegarde dans `models/best_model.joblib`

## 14. Pourquoi on ne choisit pas le meilleur modele uniquement avec l'accuracy

L'accuracy est utile, mais elle ne suffit pas toujours.

Dans ce projet, on tient compte de plusieurs metriques :

- Accuracy
- Precision
- Recall
- F1-score
- AUC-ROC

La logique est la suivante :

- `Accuracy` mesure la performance globale
- `Precision` mesure la fiabilite des alertes positives
- `Recall` mesure la capacite a retrouver les cas a risque
- `F1-score` equilibre precision et recall
- `AUC-ROC` mesure la qualite generale de separation

Cela permet une comparaison plus serieuse et plus juste.

## 15. Comment les resultats sont sauvegardes

Apres l'entrainement :

- chaque modele est sauvegarde dans `models/`
- les resultats de validation croisee sont exportes dans `cv_results.csv`
- les resultats finaux sont exportes dans `test_results.csv`
- un fichier `registry.json` garde une trace du meilleur modele retenu

Cela permet :

- de ne pas re-entrainer a chaque fois
- de reutiliser le meilleur modele dans Streamlit
- de presenter facilement les resultats

## 16. Lien entre les modeles et Streamlit

L'application Streamlit n'entraine pas les modeles a la main a chaque page.

Elle utilise les artefacts deja crees dans `models/`.

Par exemple :

- la page de comparaison lit les fichiers de resultats
- la page de prediction charge `best_model.joblib`

Cela rend l'application :

- plus rapide
- plus propre
- plus stable

## 17. Ce qu'il faut retenir 

1. on a choisi les 6 algorithmes imposes par le sujet
2. on les a organises dans un systeme commun
3. chaque modele passe par le meme pretraitement
4. on compare tous les modeles avec les memes metriques
5. on utilise la validation croisee pour une comparaison plus fiable
6. on choisit le meilleur modele selon une logique claire
7. on sauvegarde les resultats pour les reutiliser dans l'application

## 18. Conclusion

Le choix des algorithmes dans ce projet repose sur une logique serieuse :

- respecter les exigences du sujet
- comparer plusieurs familles de modeles
- utiliser une methode d'entrainement propre
- garantir une evaluation juste
- rendre le tout reutilisable dans une application

Ce n'est donc pas simplement "tester des modeles".  
C'est construire une chaine coherente de comparaison, de selection et d'utilisation pratique.

## Open tabs:
 - DOCUMENTATION_TECHNIQUE.md: DOCUMENTATION_TECHNIQUE.md
 - test_evaluation.py: tests/test_evaluation.py
 - __init__.py: tests/__init__.py
 - test_preprocessing.py: tests/test_preprocessing.py
 - test_models.py: tests/test_models.py


