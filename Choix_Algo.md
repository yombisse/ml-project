# Choix des algorithmes

## 1. Objectif de cette partie

Cette section explique la logique retenue pour choisir, entraîner et comparer les algorithmes de classification du projet.  
L'idée n'était pas seulement d'obtenir un modèle qui fonctionne, mais de montrer une démarche de comparaison sérieuse, compréhensible et cohérente avec le sujet.

## 2. Pourquoi plusieurs algorithmes ont été testés

Le projet porte sur une **classification binaire** liée à la présence ou non d'une maladie cardiaque.  
Dans ce contexte, utiliser plusieurs algorithmes est important pour trois raisons :

- un seul modèle ne permet pas d'affirmer que la meilleure solution a été recherchée ;
- chaque algorithme apprend différemment ;
- certains modèles sont simples à interpréter, alors que d'autres sont souvent plus puissants.

La comparaison ne sert donc pas à “multiplier les essais au hasard”, mais à évaluer plusieurs familles d'approches sur les mêmes données, avec les mêmes règles de préparation et les mêmes métriques.

## 3. Algorithmes retenus

Les six algorithmes utilisés sont :

1. `Logistic Regression`
2. `K-Nearest Neighbors`
3. `Support Vector Machine`
4. `Decision Tree`
5. `Random Forest`
6. `AdaBoost`

Ces modèles ont été retenus parce qu'ils correspondent à ceux demandés dans le sujet et qu'ils couvrent des logiques d'apprentissage différentes.

## 4. Intérêt de chaque algorithme

### 4.1 Logistic Regression

La régression logistique sert de **modèle de référence**.

Elle est utile car :

- elle est simple ;
- elle est rapide à entraîner ;
- elle est adaptée à la classification binaire ;
- elle fournit une base de comparaison solide.

### 4.2 K-Nearest Neighbors

KNN classe un patient à partir de la proximité avec des patients similaires.

Ce modèle est intéressant car :

- il est intuitif ;
- il exploite directement la notion de similarité ;
- il permet de tester une approche différente des modèles linéaires.

Il est toutefois sensible à l'échelle des variables, d'où l'importance de la standardisation dans le pipeline.

### 4.3 Support Vector Machine

Le SVM cherche une frontière de séparation optimale entre les classes.

Il a été choisi car :

- il est souvent performant sur des jeux de données de petite ou moyenne taille ;
- il peut modéliser des séparations plus complexes ;
- il apporte une approche plus robuste que les modèles les plus simples.

### 4.4 Decision Tree

L'arbre de décision apprend sous forme de règles successives.

Il est pertinent car :

- il est facile à lire ;
- il est plus interprétable ;
- il permet de relier les prédictions à des seuils sur les variables.

### 4.5 Random Forest

Le Random Forest combine plusieurs arbres de décision.

Son intérêt est de :

- réduire l'instabilité d'un arbre unique ;
- limiter le surapprentissage ;
- fournir en pratique de bonnes performances globales.

### 4.6 AdaBoost

AdaBoost est une méthode d'ensemble qui améliore progressivement les prédictions en insistant sur les cas difficiles.

Il a été retenu pour :

- tester une autre famille de modèles d'ensemble ;
- comparer une logique adaptative à celle du Random Forest ;
- vérifier si une combinaison de petits modèles peut mieux généraliser.

## 5. Pourquoi cet ensemble de modèles est pertinent

Ces six algorithmes représentent plusieurs familles de classification :

- modèle linéaire : `Logistic Regression`
- modèle par voisinage : `KNN`
- modèle à marge : `SVM`
- modèle à règles : `Decision Tree`
- modèle d'ensemble par arbres : `Random Forest`
- modèle d'ensemble adaptatif : `AdaBoost`

Cette diversité rend la comparaison plus crédible, car elle oppose de vraies stratégies d'apprentissage différentes.

## 6. Comment les algorithmes sont gérés dans le projet

La logique des modèles est centralisée dans :

- `src/models.py`
- `config.yaml`

`config.yaml` définit les hyperparamètres et les noms des modèles.  
`src/models.py` lit cette configuration et instancie les modèles scikit-learn correspondants.

Autrement dit :

- `config.yaml` indique **quoi utiliser** ;
- `src/models.py` indique **comment le construire**.

## 7. Logique d'entraînement retenue

L'entraînement suit une chaîne claire :

1. chargement des données ;
2. préparation et prétraitement ;
3. séparation entraînement / test ;
4. construction des pipelines ;
5. validation croisée ;
6. entraînement des modèles ;
7. calcul des métriques ;
8. comparaison finale ;
9. sauvegarde du meilleur modèle.

Le projet ne repose donc pas sur une “IA qui choisit seule”, mais sur une procédure programmée, contrôlée et reproductible.

## 8. Pourquoi un pipeline a été utilisé

Chaque algorithme est intégré dans un pipeline contenant :

1. le préprocesseur ;
2. le classifieur.

Cela garantit que les mêmes transformations sont appliquées :

- pendant l'entraînement ;
- pendant l'évaluation ;
- pendant l'utilisation finale dans Streamlit.

Ce choix évite les incohérences entre apprentissage et prédiction.

## 9. Comment les modèles ont été comparés

La comparaison ne s'est pas faite uniquement sur l'accuracy.

Les métriques prises en compte sont :

- `Accuracy`
- `Precision`
- `Recall`
- `F1-score`
- `AUC-ROC`

Le critère principal de sélection du meilleur modèle est **`roc_auc`**, car il donne une vision plus complète de la capacité du modèle à séparer les deux classes.

La validation croisée a été utilisée pour rendre cette comparaison plus fiable et éviter de juger un modèle sur un seul découpage des données.

## 10. Comment le meilleur modèle est retenu

Le meilleur modèle est choisi à partir des résultats de validation croisée, puis sauvegardé pour être réutilisé.

Les sorties principales sont :

- `models/best_model.joblib`
- `models/cv_results.csv`
- `models/test_results.csv`
- `models/registry.json`

Cette organisation permet de conserver les résultats, de justifier le choix effectué et d'alimenter directement l'application Streamlit.

## 11. Point important sur les fichiers `.joblib`

Les fichiers comme :

- `best_model.joblib`
- `adaboost.joblib`
- `logistic_regression.joblib`

ne sont **pas des fichiers texte classiques**.  
Ce sont des **fichiers binaires** utilisés pour sauvegarder des objets Python déjà entraînés.

Il est donc normal qu'un éditeur affiche un message du type :

- fichier binaire ;
- encodage non pris en charge.

Cela ne signifie pas que le fichier est corrompu.  
Cela signifie simplement qu'il doit être chargé avec Python, par exemple via `joblib.load(...)`, et non lu comme un document texte.

## 12. Conclusion

Le choix des algorithmes dans ce projet repose sur une logique claire :

- respecter les exigences du sujet ;
- comparer plusieurs familles de modèles ;
- entraîner tous les modèles dans le même cadre méthodologique ;
- utiliser des métriques adaptées ;
- retenir le meilleur modèle sur une base objective.


