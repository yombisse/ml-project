# Heart Disease Prediction

Projet académique de classification supervisée basé sur le dataset **Heart Disease UCI**.  
L’objectif est de comparer plusieurs algorithmes de machine learning pour prédire la présence d’une maladie cardiaque, puis de présenter les résultats dans une application **Streamlit** claire et interactive.

## Objectifs

- préparer et nettoyer le dataset `processed.cleveland.data`
- transformer la cible en problème binaire
- entraîner 6 modèles de classification
- comparer les performances avec :
  - Accuracy
  - Precision
  - Recall
  - F1-score
  - AUC-ROC
- proposer une interface Streamlit avec :
  - authentification simple
  - visualisation des données
  - comparaison des modèles
  - prédiction individuelle
  - export des résultats

## Algorithmes utilisés

Les algorithmes imposés par le sujet et implémentés dans le projet sont :

1. Logistic Regression
2. K-Nearest Neighbors
3. Support Vector Machine
4. Decision Tree
5. Random Forest
6. AdaBoost

## Structure du projet

```text
ml-project/
├── assets/
│   └── images/                         # Images utilisées dans l'accueil Streamlit
├── data/
│   ├── raw/
│   │   └── processed.cleveland.data   # Dataset brut principal
│   └── processed/                     # Données nettoyées
├── logs/                              # Journaux d'entraînement et d'application
├── models/                            # Modèles sauvegardés et résultats exportés
├── notebooks/
│   └── analysis.ipynb
├── src/
│   ├── constants.py
│   ├── evaluation.py
│   ├── models.py
│   ├── preprocessing.py
│   └── utils.py
├── streamlit_app/
│   ├── app.py
│   ├── common.py
│   └── pages/
│       ├── 00_Accueil.py
│       ├── 01_EDA.py
│       ├── 02_Models_Comparison.py
│       ├── 03_Prediction.py
│       └── 04_Guide_Application.py
├── tests/
│   ├── test_evaluation.py
│   ├── test_models.py
│   └── test_preprocessing.py
├── Choix_Algo.md
├── config.yaml
├── DOCUMENTATION_TECHNIQUE.md
├── GUIDE_UTILISATION.md
├── plan_implementation.md
├── projet.md
├── README.md
├── requirements.txt
└── run_training.py
```

## Dataset

- Source : [UCI Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease)
- Fichier exploité : `data/raw/processed.cleveland.data`
- Nombre de colonnes : 14
- Nombre de variables explicatives : 13
- Variable cible : `target`

### Point important sur la cible

Dans le dataset original, la cible prend les valeurs `0, 1, 2, 3, 4`.

- `0` : absence de maladie
- `1 à 4` : présence de maladie

Dans ce projet, la cible est convertie en **binaire** :

- `0 -> 0`
- `1, 2, 3, 4 -> 1`

## Prétraitement

Le pipeline de préparation des données comprend :

- chargement du dataset
- détection des valeurs manquantes
- imputation :
  - médiane pour les variables numériques
  - valeur la plus fréquente pour les variables catégorielles
- standardisation des variables numériques
- encodage des variables catégorielles avec `OneHotEncoder`
- séparation `train / test`

Le prétraitement est intégré directement dans les pipelines scikit-learn pour éviter les fuites de données.

## Entraînement et évaluation

Le projet suit cette logique :

1. préparation des données
2. séparation du dataset en jeu d’entraînement et jeu de test
3. validation croisée sur les données d’entraînement
4. entraînement final des modèles
5. évaluation sur le jeu de test
6. sélection du meilleur modèle
7. sauvegarde des artefacts dans `models/`

### Fichiers générés dans `models/`

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

## Application Streamlit

L’application inclut :

- une page d’accueil avec carousel d’images
- un bouton de connexion avec formulaire pop-up
- une authentification simple email / mot de passe
- une sidebar privée après connexion
- une page de visualisation des données
- une page de comparaison des modèles
- une page de prédiction individuelle
- une page guide
- des exports CSV / Excel

## Installation

### 1. Créer un environnement virtuel

Sous Windows :

```bash
python -m venv .venv
.venv\Scripts\activate
```

Sous Linux / macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancer le projet

### Entraîner les modèles

```bash
python run_training.py
```

### Exécuter les tests

```bash
python -m pytest tests -q
```

### Lancer l’application Streamlit

```bash
streamlit run streamlit_app/app.py
```

## Identifiants de démonstration

- Email : `IFOAD@gmail.com`
- Mot de passe : `Heart123`

## Fichiers de documentation

- [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)
- [DOCUMENTATION_TECHNIQUE.md](DOCUMENTATION_TECHNIQUE.md)
- [Choix_Algo.md](Choix_Algo.md)
- [plan_implementation.md](plan_implementation.md)

## Vérifications déjà réalisées

- entraînement du pipeline : OK
- génération des artefacts : OK
- tests unitaires basiques : OK
- interface Streamlit fonctionnelle : OK

## Remarque

Ce projet a une finalité **académique**.  
Les résultats et prédictions fournis par l’application servent à démontrer une démarche de machine learning et ne remplacent pas une interprétation médicale professionnelle.
