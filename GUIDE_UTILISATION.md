# Guide d'utilisation

## 1. Objectif du guide

Ce guide permet de prendre en main rapidement le projet, de lancer les composants principaux, de verifier le bon fonctionnement du pipeline et de tester l'application Streamlit dans de bonnes conditions.

Il est volontairement pratique et organise pour qu'un membre du groupe, un enseignant ou un correcteur puisse suivre les etapes sans ambiguite.

## 2. Structure importante a connaitre

Les dossiers principaux utiles sont :

- `data/raw/` : dataset brut `processed.cleveland.data`
- `data/processed/` : donnees preparees
- `src/` : logique Python du projet
- `models/` : modeles et resultats sauvegardes
- `logs/` : journaux d'execution
- `tests/` : tests automatises
- `streamlit_app/` : application web Streamlit

## 3. Prerequis

Verifier les elements suivants :

- Python installe
- dependances installees depuis `requirements.txt`
- dataset present dans `data/raw/processed.cleveland.data`

## 4. Installation des dependances

Depuis la racine du projet :

```powershell
python -m pip install -r requirements.txt
```

## 5. Lancer l'entrainement complet

Cette etape genere :

- les modeles sauvegardes
- les resultats de comparaison
- les fichiers de journalisation

Commande :

```powershell
python run_training.py
```

Sorties attendues :

- `models/best_model.joblib`
- `models/logistic_regression.joblib`
- `models/knn.joblib`
- `models/svm.joblib`
- `models/decision_tree.joblib`
- `models/random_forest.joblib`
- `models/adaboost.joblib`
- `models/cv_results.csv`
- `models/test_results.csv`
- `models/registry.json`

## 6. Lancer les tests

Commande :

```powershell
python -m pytest tests -q
```

Les tests verifient notamment :

- le chargement du dataset
- la transformation correcte de la cible
- la construction du preprocesseur
- la presence des 6 modeles imposes
- le calcul des metriques principales

## 7. Lancer l'application Streamlit

Commande :

```powershell
streamlit run streamlit_app/app.py
```

Une fois l'application ouverte dans le navigateur, utiliser cet ordre :

1. page d'accueil
2. `Analyse Exploratoire`
3. `Comparaison des Modeles`
4. `Prediction Individuelle`
5. `Guide de l'Application`

## 8. Comment tester toutes les fonctionnalites

### 8.1 Verification du pipeline de donnees

Verifier que :

- le fichier `data/processed/heart_disease_cleaned.csv` est cree
- la colonne `target` contient seulement `0` et `1`
- les modeles sont sauvegardes dans `models/`

### 8.2 Verification de la comparaison des modeles

Dans la page `Comparaison des Modeles`, verifier que :

- les 6 algorithmes apparaissent
- les metriques suivantes sont presentes :
  - Accuracy
  - Precision
  - Recall
  - F1-score
  - AUC-ROC
- la validation croisee est affichee
- l'evaluation finale sur le jeu de test est visible

### 8.3 Verification de la prediction

Dans la page `Prediction Individuelle`, verifier que :

- le formulaire s'affiche completement
- chaque variable du patient peut etre renseignee
- la prediction s'affiche apres validation
- la probabilite est affichee si disponible
- le recapitulatif des donnees saisies apparait

### 8.4 Verification des journaux

Verifier la presence de :

- `logs/training.log`
- `logs/evaluation.log`
- `logs/app.log`

Ces journaux doivent contenir des informations sur l'entrainement, la comparaison et les executions importantes.

## 9. Ce qu'il faut expliquer pendant la presentation

Les points les plus importants a presenter sont :

- le dataset Heart Disease UCI
- la binarisation de la cible
- l'imputation des valeurs manquantes
- la comparaison des 6 modeles obligatoires
- le choix du meilleur modele a partir de la validation croisee
- l'utilisation de Streamlit pour la demonstration

## 10. Verification finale avant soutenance

Avant presentation, verifier cette checklist :

- `python run_training.py` fonctionne
- `python -m pytest tests -q` fonctionne
- `streamlit run streamlit_app/app.py` fonctionne
- les fichiers dans `models/` sont bien presents
- les logs sont bien generes
- la navigation Streamlit est fluide
- la prediction individuelle fonctionne

## 11. Remarque importante

L'application et les modeles ont une finalite academique.  
Les predictions affichees servent a illustrer un pipeline de machine learning et ne remplacent jamais une interpretation medicale professionnelle.
