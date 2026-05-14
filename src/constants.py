"""Project constants for the Heart Disease classification workflow."""

DATASET_COLUMNS = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "target",
]

NUMERIC_FEATURES = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CATEGORICAL_FEATURES = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]

CLASS_LABELS = {
    0: "Risque faible detecte",
    1: "Vigilance recommandee",
}

MODEL_DISPLAY_NAMES = {
    "logistic_regression": "Logistic Regression",
    "knn": "K-Nearest Neighbors",
    "svm": "Support Vector Machine",
    "decision_tree": "Decision Tree",
    "random_forest": "Random Forest",
    "adaboost": "AdaBoost",
}

PATIENT_FRIENDLY_METRICS = {
    "accuracy": "Exactitude globale",
    "precision": "Fiabilite des alertes",
    "recall": "Detection des cas a risque",
    "f1_score": "Equilibre global",
    "roc_auc": "Qualite generale",
}
