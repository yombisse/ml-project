"""Model registry, training and artifact persistence."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any

import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from src.evaluation import compare_test_metrics, cross_validate_models
from src.preprocessing import build_preprocessor, load_processed_dataset, split_dataset
from src.utils import ensure_project_directories, load_config, save_artifact, save_json, setup_logger


os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")


def get_estimators(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Instantiate the six required classification estimators."""
    loaded_config = config or load_config()
    models_config = loaded_config["models"]

    return {
        "logistic_regression": LogisticRegression(**models_config["logistic_regression"]["hyperparameters"]),
        "knn": KNeighborsClassifier(**models_config["knn"]["hyperparameters"]),
        "svm": SVC(**models_config["svm"]["hyperparameters"]),
        "decision_tree": DecisionTreeClassifier(**models_config["decision_tree"]["hyperparameters"]),
        "random_forest": RandomForestClassifier(**models_config["random_forest"]["hyperparameters"]),
        "adaboost": AdaBoostClassifier(**models_config["adaboost"]["hyperparameters"]),
    }


def build_model_pipelines(config: dict[str, Any] | None = None) -> dict[str, Pipeline]:
    """Build a preprocessing + model pipeline for each estimator."""
    loaded_config = config or load_config()
    preprocessor = build_preprocessor(loaded_config)
    estimators = get_estimators(loaded_config)

    return {
        name: Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", estimator),
            ]
        )
        for name, estimator in estimators.items()
    }


def train_all_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    config: dict[str, Any] | None = None,
) -> dict[str, Pipeline]:
    """Fit all model pipelines on the training data."""
    loaded_config = config or load_config()
    logger = setup_logger("training", loaded_config)
    models = build_model_pipelines(loaded_config)

    for name, model in models.items():
        logger.info("Training model: %s", name)
        model.fit(X_train, y_train)
        logger.info("Training completed: %s", name)
    return models


def run_training_pipeline(config_path: str | None = None) -> dict[str, Any]:
    """Execute the end-to-end training, evaluation and artifact saving workflow."""
    config = load_config(config_path)
    ensure_project_directories(config)
    logger = setup_logger("pipeline", config)

    X_train, X_test, y_train, y_test = split_dataset(config=config)
    cv_models = build_model_pipelines(config)
    cv_results = cross_validate_models(cv_models, X_train, y_train, config)

    fitted_models = train_all_models(X_train, y_train, config)
    test_results = compare_test_metrics(fitted_models, X_test, y_test, config)
    best_model_name = cv_results.iloc[0]["model"]
    best_model = fitted_models[best_model_name]

    models_dir = config["paths"]["models"]
    save_artifact(best_model, f"{models_dir}/best_model.joblib")
    for model_name, model in fitted_models.items():
        save_artifact(model, f"{models_dir}/{model_name}.joblib")

    cv_results.to_csv(f"{models_dir}/cv_results.csv", index=False)
    test_results.to_csv(f"{models_dir}/test_results.csv", index=False)
    registry = {
        "generated_at": datetime.utcnow().isoformat(),
        "best_model": best_model_name,
        "cv_results_file": f"{models_dir}/cv_results.csv",
        "test_results_file": f"{models_dir}/test_results.csv",
        "processed_dataset": config["data"]["processed_path"],
    }
    save_json(registry, f"{models_dir}/registry.json")

    logger.info("Best model selected: %s", best_model_name)
    logger.info("CV results saved to %s/cv_results.csv", models_dir)
    logger.info("Test results saved to %s/test_results.csv", models_dir)
    logger.info("Training pipeline completed successfully.")

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "cv_results": cv_results,
        "test_results": test_results,
        "best_model_name": best_model_name,
        "best_model": best_model,
        "processed_data": load_processed_dataset(config),
    }
