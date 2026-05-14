# Documentation technique

## 1. But du document

Ce document explique la logique technique suivie dans le projet afin qu'un autre membre de l'equipe puisse comprendre rapidement :

- comment le projet a ete structure
- comment les donnees sont preparees
- comment les modeles sont entraines et compares
- comment le meilleur modele est retenu
- comment l'application Streamlit a ete organisee

Le but est d'offrir une vue claire du raisonnement suivi pendant la mise en place du projet.

## 2. Vision generale du projet

Le projet repose sur quatre blocs complementaires :

1. preparation des donnees
2. entrainement et comparaison des modeles
3. sauvegarde des artefacts du projet
4. presentation des resultats dans une interface Streamlit

L'idee a ete de garder l'architecture de depart deja choisie , tout en renforcant sa proprete avec :

- `models/` comme emplacement unique des artefacts
- `logs/` pour la tracabilite
- `tests/` pour la verification basique

## 3. Dataset utilise

Le jeu de donnees retenu est `processed.cleveland.data` du dataset **Heart Disease UCI**.

Le fichier contient 14 colonnes :

- 13 variables explicatives
- 1 variable cible

Point important :

- la cible officielle du dataset n'est pas directement binaire
- elle prend les valeurs `0, 1, 2, 3, 4`
- `0` signifie absence
- `1 a 4` signifient presence

Dans ce projet, la cible est transformee en binaire :

- `0 -> 0`
- `1, 2, 3, 4 -> 1`

Ce choix rend le probleme conforme a la demande de classification binaire.

## 4. Structure des fichiers

### `src/preprocessing.py`

Ce fichier contient la logique de preparation des donnees :

- chargement du fichier brut
- attribution des noms de colonnes
- conversion des valeurs manquantes
- binarisation de la cible
- separation `X / y`
- division train/test
- construction du preprocesseur

### `src/models.py`

Ce fichier gere :

- la creation des 6 modeles imposes
- la creation des pipelines complets
- l'entrainement de tous les modeles
- la generation des resultats de comparaison
- la selection du meilleur modele
- la sauvegarde des artefacts

### `src/evaluation.py`

Ce fichier calcule :

- Accuracy
- Precision
- Recall
- F1-score
- AUC-ROC

Il gere aussi :

- la validation croisee
- l'evaluation finale sur le jeu de test

### `src/utils.py`

Ce fichier centralise :

- le chargement de `config.yaml`
- la resolution des chemins du projet
- la creation automatique des dossiers utiles
- la sauvegarde des artefacts
- la journalisation

### `streamlit_app/common.py`

Ce fichier sert de socle commun pour l'application Streamlit :

- authentification simple
- gestion de session
- bouton logout
- rendu de la barre laterale
- style global
- export CSV / Excel
- gestion des images de l'accueil

## 5. Strategie de preparation des donnees


### 5.1 Chargement

Le dataset est lu depuis :

- `data/raw/processed.cleveland.data`

Les colonnes sont ensuite nommees explicitement.

### 5.2 Valeurs manquantes

Le projet utilise une **imputation** plutot qu'une suppression.

Ce choix a ete retenu pour une raison simple :

- le dataset est petit
- supprimer des lignes reduirait encore l'information disponible

La logique choisie est la suivante :

- imputation par mediane pour les variables numeriques
- imputation par valeur la plus frequente pour les variables categorielles

### 5.3 Transformation avant apprentissage

Le preprocesseur applique :

- imputation
- standardisation sur les variables numeriques
- encodage `OneHotEncoder` sur les variables categorielles

Cette etape est integree dans les pipelines des modeles, ce qui garantit :

- une execution coherente
- une reutilisation propre
- l'absence de fuite d'information entre train et test

## 6. Modeles implementes

Les modeles demandes par le sujet sont bien ceux qui ont ete integres :

1. Logistic Regression
2. K-Nearest Neighbors
3. Support Vector Machine
4. Decision Tree
5. Random Forest
6. AdaBoost

Ils sont declares dans `config.yaml` et instancies dans `src/models.py`.

## 7. Methode de comparaison des modeles

La comparaison se fait en deux temps.

### 7.1 Validation croisee sur les donnees d'entrainement

La validation croisee sert a comparer les solutions dans un cadre plus robuste qu'un simple score unique.

Elle permet de :

- mieux estimer la stabilite des modeles
- reduire le risque de choisir un modele chanceux

### 7.2 Evaluation finale sur le jeu de test

Une fois les modeles compares, ils sont ensuite evalues sur le jeu de test.

Important :

- le jeu de test ne sert pas a choisir le meilleur modele
- il sert uniquement a valider la qualite finale

Ce point est important pour conserver une logique d'evaluation correcte.

## 8. Choix du meilleur modele

Le meilleur modele retenu pour l'application est choisi a partir de la validation croisee.

Le critere principal est l'indicateur :

- `roc_auc`

Ce choix a ete retenu car il donne une vue globale de la capacite du modele a separer les deux classes.

Le resultat final sauvegarde dans :

- `models/best_model.joblib`

correspond donc au modele juge le plus stable sur les essais croises.

## 9. Artefacts produits

Le dossier `models/` centralise les sorties importantes :

- `best_model.joblib`
- `logistic_regression.joblib`
- `knn.joblib`
- `svm.joblib`
- `decision_tree.joblib`
- `random_forest.joblib`
- `adaboost.joblib`
- `cv_results.csv`
- `test_results.csv`
- `registry.json`

Cette organisation evite toute confusion avec `streamlit_app/`.

### 9.1 Pourquoi les fichiers du dossier `models/` ne s'ouvrent pas comme des fichiers texte

Les fichiers comme :

- `best_model.joblib`
- `adaboost.joblib`
- `logistic_regression.joblib`

ne sont pas des fichiers texte classiques.

Ce sont des **fichiers binaires** crees pour sauvegarder des objets Python deja entraines.

Il est donc normal que l'editeur affiche un message du type :

- fichier binaire
- encodage non pris en charge

Cela ne signifie pas que le fichier est corrompu.  
Cela signifie simplement qu'il ne doit pas etre lu comme un document texte.

### 9.2 Bonne methode pour consulter le contenu d'un modele sauvegarde

La bonne methode consiste a charger le fichier avec `joblib`, puis a afficher son type ou sa structure.

Exemple correct depuis la racine du projet :

```powershell
python
```

Puis dans l'interpreteur Python :

```python
import joblib

modele = joblib.load("models/adaboost.joblib")
print(type(modele))
print(modele)
```

Exemple de resultat attendu :

```python
<class 'sklearn.pipeline.Pipeline'>
```

Cela montre que le fichier contient ici un **pipeline scikit-learn complet**, c'est-a-dire :

- le pretraitement
- puis le classifieur

### 9.3 Pourquoi `joblib.load("adaboost.joblib")` ne marchait pas

La commande :

```python
modele = joblib.load("adaboost.joblib")
```

ne fonctionne pas si le fichier n'est pas dans le dossier courant.

Dans ce projet, les modeles sont sauvegardes dans :

- `models/`

Il faut donc utiliser le chemin correct :

```python
modele = joblib.load("models/adaboost.joblib")
```

### 9.4 Comment inspecter precisement ce qu'un modele contient

Une fois le modele charge, on peut afficher ses differentes parties.

Exemple :

```python
import joblib

modele = joblib.load("models/adaboost.joblib")

print(type(modele))
print(modele.named_steps.keys())
print(modele.named_steps["preprocessor"])
print(modele.named_steps["classifier"])
```

Cela permet de voir :

- les etapes du pipeline
- le bloc de pretraitement
- l'algorithme de classification utilise

### 9.5 Exemple d'inspection du meilleur modele

Pour consulter le modele retenu par l'application :

```python
import joblib

best_model = joblib.load("models/best_model.joblib")
print(type(best_model))
print(best_model)
```

### 9.6 Comment lire les fichiers de resultats non binaires

Tous les fichiers du dossier `models/` ne sont pas binaires.

Les fichiers suivants peuvent etre ouverts directement :

- `cv_results.csv`
- `test_results.csv`
- `registry.json`

Exemples :

```python
import pandas as pd

cv = pd.read_csv("models/cv_results.csv")
test = pd.read_csv("models/test_results.csv")

print(cv.head())
print(test.head())
```

Et pour le fichier JSON :

```python
import json

with open("models/registry.json", "r", encoding="utf-8") as f:
    registry = json.load(f)

print(registry)
```

### 9.7 Conclusion pratique

Pour resumer :

- un fichier `.joblib` ne se lit pas dans l'editeur comme un fichier texte
- il faut le charger avec `joblib.load(...)`
- ta methode etait donc la bonne
- l'important est simplement d'utiliser le bon chemin, par exemple `models/adaboost.joblib`

## 10. Journalisation

Le projet genere plusieurs journaux dans `logs/` :

- `app.log`
- `training.log`
- `evaluation.log`
- `streamlit.log`

Le but est de garder une trace de :

- l'entrainement
- l'evaluation
- les connexions et chargements d'interface

Cela facilite le suivi des executions et le debogage.

## 11. Logique de l'application Streamlit

L'application a ete revue pour etre plus convaincante visuellement et plus simple a utiliser.

### 11.1 Authentification

Une authentification simple par email et mot de passe a ete ajoutee.

Objectifs :

- eviter une saisie peu professionnelle dans le terminal
- donner un vrai point d'entree a l'application
- ajouter un bouton de deconnexion

Le mecanisme repose sur `st.session_state`.

### 11.2 Accueil visuel

La page d'accueil utilise :

- une zone visuelle avec les images de `assets/images`
- un formulaire de connexion

### 11.3 Pages utilisateur

Les pages ont ete revues avec un vocabulaire plus simple :

- `01_EDA.py` : vue d'ensemble des donnees
- `02_Models_Comparison.py` : resultats globaux
- `03_Prediction.py` : estimation individuelle
- `04_Guide_Application.py` : aide rapide



## 12. Exports

Des boutons d'export ont ete ajoutes pour rendre l'application plus utile :

- export CSV
- export Excel

Ils sont disponibles :

- pour les donnees preparees
- pour les resultats globaux
- pour la prediction individuelle

## 13. Tests

Le dossier `tests/` contient des tests simples mais utiles.

Ils verifient notamment :

- le chargement du dataset
- la binarisation de la cible
- la construction du preprocesseur
- la presence des 6 modeles
- la production des metriques attendues

Commande d'execution :

```powershell
python -m pytest tests -q
```



## 14. Points forts de la solution finale

Les points forts du projet sont :

- architecture de depart respectee
- pipeline clair et reusable
- imputation adaptee a un petit dataset
- 6 modeles conformes au sujet
- choix du meilleur modele base sur la validation croisee
- artefacts centralises
- logs et tests presents
- application plus professionnelle et plus demonstrative

## 17. Limites assumees

Le projet reste un projet academique.  
Certaines limites sont donc normales :

- authentification simple et non securisee pour la production
- dataset de petite taille
- absence de deploiement cloud
- interface orientee demonstration plus que produit medical reel

## 18. Conclusion

Le projet a ete mene avec une logique de progression propre :

- partir d'une base simple
- la rendre plus rigoureuse
- conserver la lisibilite
- produire un resultat presentable techniquement et visuellement

