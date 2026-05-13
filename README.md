# 🏥 Prédiction des Maladies Cardiaques - Heart Disease Classification

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Streamlit App](https://img.shields.io/badge/streamlit-app-FF4B4B)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-F7931E)](https://scikit-learn.org)

## 📋 Vue d'ensemble du Projet

Ce projet académique de Machine Learning vise à prédire la présence de maladies cardiaques basé sur le dataset Heart Disease UCI. Le projet inclut une analyse exploratoire complète (EDA), le prétraitement des données, l'entraînement de multiples modèles de classification et une application web interactive.

### 🎯 Objectifs

- ✅ Analyse exploratoire des données (EDA)
- ✅ Prétraitement et nettoyage des données
- ✅ Entraînement de 6 modèles de classification
- ✅ Évaluation et comparaison des modèles
- ✅ Application web Streamlit pour prédictions en temps réel

---

## 📁 Architecture du Projet

```
ML-PROJECT/
├── data/
│   ├── raw/                          # Dataset brut (processed.cleveland.data)
│   └── processed/                    # Données nettoyées et prétraitées
│
├── notebooks/
│   └── analysis.ipynb                # Rapport académique complet
│
├── src/                              # Code réutilisable et modulaire
│   ├── __init__.py
│   ├── constants.py                  # Configurations et constantes
│   ├── preprocessing.py              # Nettoyage et préparation des données
│   ├── models.py                     # Implémentation des 6 modèles ML
│   ├── evaluation.py                 # Métriques et comparaison des modèles
│   └── utils.py                      # Visualisations et fonctions utiles
│
├── streamlit_app/
│   ├── app.py                        # Fichier principal Streamlit
│   ├── pages/
│   │   ├── 01_EDA.py                 # Visualisations exploratoires
│   │   ├── 02_Models_Comparison.py   # Comparaison des modèles
│   │   └── 03_Prediction.py          # Prédictions temps réel
│   └── models/                       # Modèles sauvegardés (.pkl)
│
├── requirements.txt                  # Dépendances Python
├── README.md                         # Ce fichier
├── .gitignore                        # Git configuration
├── setup.py                          # Installation du package
└── config.yaml                       # Configuration du projet
```

---

## 🚀 Installation et Configuration

### Prérequis

- **Python** : 3.9 ou supérieur
- **pip** : Gestionnaire de paquets Python
- **Git** (optionnel, pour le versioning)

### ⚙️ Étape 1 : Cloner/Naviguer vers le projet

```bash
cd ~/MesProjets/ml-project
```

### 📦 Étape 2 : Créer un Environnement Virtuel

#### **Sur Linux/macOS** :
```bash
python3 -m venv venv
source venv/bin/activate
```

#### **Sur Windows** :
```bash
python -m venv venv
venv\Scripts\activate
```

**✓ Vous verrez `(venv)` apparaître au début de votre ligne de terminal**

### 📥 Étape 3 : Installer les Dépendances

Assurez-vous que l'environnement virtuel est activé, puis :

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Cela installera :**
- numpy, pandas, scipy (manipulation de données)
- scikit-learn (modèles ML)
- matplotlib, seaborn, plotly (visualisations)
- streamlit (application web)
- jupyter, notebook (notebooks interactifs)

### ✅ Étape 4 : Vérifier l'Installation

```bash
# Vérifier que les principales bibliothèques sont installées
python -c "import pandas, sklearn, streamlit; print('✓ All libraries installed successfully!')"
```

---

## 📊 Utilisation du Projet

### Option 1 : Jupyter Notebook (Analyse)

```bash
# Activer l'environnement virtuel
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Lancer Jupyter
jupyter notebook

# Ouvrir: notebooks/analysis.ipynb
```

📌 Le notebook contient :
- Introduction et contexte
- Chargement du dataset
- Nettoyage des données
- Analyse exploratoire complète (distributions, corrélations, outliers)
- Sauvegarde des données prétraitées

### Option 2 : Application Streamlit (Prédictions)

```bash
# Activer l'environnement virtuel
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Lancer Streamlit
streamlit run streamlit_app/app.py
```

📌 L'application offre :
- **Page Accueil** : Vue d'ensemble du projet
- **Page EDA** : Visualisations exploratoires interactives
- **Page Comparaison Modèles** : Performance de 6 modèles
- **Page Prédiction** : Interface pour prédire en temps réel

---

## 🧪 Structure des Modules Python

### `src/preprocessing.py`
Nettoyage et préparation des données :
- Gestion des valeurs manquantes
- Normalisation/Standardisation
- Encodage des variables catégorielles
- Création des datasets train/test

### `src/models.py`
Implémentation de 6 modèles de classification :
1. Logistic Regression
2. Support Vector Machine (SVM)
3. Decision Tree
4. Random Forest
5. Gradient Boosting
6. K-Nearest Neighbors (KNN)

### `src/evaluation.py`
Métriques et évaluation :
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Confusion Matrix

### `src/utils.py`
Fonctions utilitaires :
- Visualisations (plots, heatmaps)
- Chargement/sauvegarde de modèles
- Configurations globales

### `src/constants.py`
Configurations du projet :
- Chemins des fichiers
- Paramètres des modèles
- Seuils et hyperparamètres

---

## 📈 Dataset

**Nom** : Heart Disease UCI Dataset  
**Source** : [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/heart+disease)  
**Fichier** : `processed.cleveland.data`

### Variables (13 features + 1 cible)

| Variable | Description | Type |
|----------|-------------|------|
| `age` | Âge du patient (années) | Numérique |
| `sex` | Sexe (0: Féminin, 1: Masculin) | Catégoriell |
| `cp` | Type de douleur thoracique | Catégoriquel |
| `trestbps` | Pression artérielle au repos (mmHg) | Numérique |
| `chol` | Cholestérol (mg/dl) | Numérique |
| `fbs` | Sucre à jeun > 120 mg/dl | Binaire |
| `restecg` | Résultats ECG au repos | Catégoriquel |
| `thalach` | Fréquence cardiaque maximale | Numérique |
| `exang` | Angine induite par l'exercice | Binaire |
| `oldpeak` | Dépression ST induite par l'exercice | Numérique |
| `slope` | Pente du segment ST | Catégoriquel |
| `ca` | Nombre de vaisseaux principaux | Numérique |
| `thal` | Thalassémie | Catégoriquel |
| **`target`** | **Maladie cardiaque (0: Absent, 1: Présent)** | **Binaire** |

---

## 🔧 Commandes Utiles

### Vérifier l'environnement virtuel
```bash
# Afficher le chemin de Python actif
which python  # Linux/macOS
where python  # Windows

# Lister les packages installés
pip list
```

### Réinstaller les dépendances
```bash
pip install -r requirements.txt --force-reinstall
```

### Créer un fichier requirements.txt à partir de l'env actuel
```bash
pip freeze > requirements.txt
```

### Déactiver l'environnement virtuel
```bash
deactivate
```

---

## 📚 Guide d'Utilisation Complet

### 1️⃣ Premier lancement (Setup complet)

```bash
# 1. Se placer dans le dossier
cd ~/MesProjets/ml-project

# 2. Créer et activer l'env virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 4. Lancer le notebook pour l'analyse
jupyter notebook notebooks/analysis.ipynb
```

### 2️⃣ Utiliser l'application Streamlit

```bash
# Avec l'env virtuel activé
streamlit run streamlit_app/app.py

# L'app sera accessible à http://localhost:8501
```

### 3️⃣ Entraîner les modèles

```python
# Dans un script Python ou Jupyter
from src.preprocessing import load_and_prepare_data
from src.models import train_all_models
from src.evaluation import evaluate_models

# Charger les données
X_train, X_test, y_train, y_test = load_and_prepare_data()

# Entraîner tous les modèles
models = train_all_models(X_train, y_train)

# Évaluer et comparer
results = evaluate_models(models, X_test, y_test)
print(results)
```

---

## 📊 Exemple de Sortie Attendue

### Performance des Modèles
```
Model                  | Accuracy | Precision | Recall | F1-Score | AUC
Logistic Regression   |  0.82    |   0.85    | 0.78   |  0.81    | 0.87
Random Forest         |  0.88    |   0.90    | 0.86   |  0.88    | 0.93
SVM                   |  0.84    |   0.87    | 0.81   |  0.84    | 0.89
Gradient Boosting     |  0.89    |   0.91    | 0.87   |  0.89    | 0.94
Decision Tree         |  0.81    |   0.83    | 0.79   |  0.81    | 0.85
KNN                   |  0.80    |   0.82    | 0.77   |  0.79    | 0.83
```

---

## 🐛 Dépannage

### Erreur : `No module named 'pandas'`
```bash
# Solution : Réinstaller les dépendances
source venv/bin/activate
pip install -r requirements.txt
```

### Erreur : `Port 8501 already in use`
```bash
# Solution : Spécifier un port différent
streamlit run streamlit_app/app.py --server.port 8502
```

### Erreur : `FileNotFoundError` pour les données
```bash
# Solution : Télécharger le dataset dans data/raw/
# Chemin attendu: data/raw/processed.cleveland.data
```

---

## 📖 Ressources Supplémentaires

- [Scikit-learn Documentation](https://scikit-learn.org)
- [Pandas Documentation](https://pandas.pydata.org)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Jupyter Notebook Guide](https://jupyter.org)
- [UCI Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+disease)

---

## 📝 Notes Académiques

Ce projet respecte les normes académiques :
- ✅ Code modulaire et réutilisable
- ✅ Documentation complète
- ✅ Séparation des responsabilités (SoC)
- ✅ Validation croisée et métriques appropriées
- ✅ Interface utilisateur professionnelle

---

## 👤 Auteur

**Projet IFOAD Machine Learning**  
Date : 13 mai 2026

---

## 📜 Licence

Ce projet est fourni à titre académique à des fins d'enseignement.

---

## ✨ Améliorations Futures

- [ ] Ajouter des modèles d'ensemble (Voting, Stacking)
- [ ] Implémenter l'optimisation des hyperparamètres (GridSearch, RandomSearch)
- [ ] Ajouter la prédiction par batch (fichier CSV)
- [ ] Créer une API REST (FastAPI)
- [ ] Déployer sur cloud (Heroku, AWS, Azure)
- [ ] Ajouter des tests unitaires (pytest)
- [ ] Implémenter le monitoring des modèles

---
