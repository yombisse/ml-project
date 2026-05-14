"""Evaluation helpers for classification models."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate

from src.utils import load_config, setup_logger


def _extract_score_vector(model: Any, features: pd.DataFrame) -> np.ndarray:
    """Extract a probability-like score for ROC-AUC."""
    if hasattr(model, "predict_proba"):
        return model.predict_proba(features)[:, 1]
    if hasattr(model, "decision_function"):
        return model.decision_function(features)
    return model.predict(features)


def compute_classification_metrics(model: Any, features: pd.DataFrame, target: pd.Series) -> dict[str, float]:
    """Compute the five required evaluation metrics on a dataset split."""
    predictions = model.predict(features)
    scores = _extract_score_vector(model, features)

    return {
        "accuracy": accuracy_score(target, predictions),
        "precision": precision_score(target, predictions, zero_division=0),
        "recall": recall_score(target, predictions, zero_division=0),
        "f1_score": f1_score(target, predictions, zero_division=0),
        "roc_auc": roc_auc_score(target, scores),
    }


def cross_validate_models(
    models: dict[str, Any],
    features: pd.DataFrame,
    target: pd.Series,
    config: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Run stratified cross-validation and summarize mean/std metrics."""
    loaded_config = config or load_config()
    splitter = StratifiedKFold(
        n_splits=loaded_config["evaluation"]["cv_folds"],
        shuffle=True,
        random_state=loaded_config["data"]["random_state"],
    )
    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc",
    }

    rows: list[dict[str, float | str]] = []
    for model_name, model in models.items():
        scores = cross_validate(model, features, target, cv=splitter, scoring=scoring, n_jobs=None)
        rows.append(
            {
                "model": model_name,
                "cv_accuracy_mean": scores["test_accuracy"].mean(),
                "cv_accuracy_std": scores["test_accuracy"].std(),
                "cv_precision_mean": scores["test_precision"].mean(),
                "cv_recall_mean": scores["test_recall"].mean(),
                "cv_f1_mean": scores["test_f1"].mean(),
                "cv_roc_auc_mean": scores["test_roc_auc"].mean(),
            }
        )

    return pd.DataFrame(rows).sort_values(by="cv_roc_auc_mean", ascending=False).reset_index(drop=True)


def compare_test_metrics(
    fitted_models: dict[str, Any],
    X_test: pd.DataFrame,
    y_test: pd.Series,
    config: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Evaluate fitted models on the held-out test set."""
    loaded_config = config or load_config()
    logger = setup_logger("evaluation", loaded_config)
    rows: list[dict[str, float | str]] = []
    for model_name, model in fitted_models.items():
        metrics = compute_classification_metrics(model, X_test, y_test)
        logger.info("Test metrics for %s: %s", model_name, metrics)
        rows.append({"model": model_name, **metrics})
    return pd.DataFrame(rows).sort_values(by="roc_auc", ascending=False).reset_index(drop=True)
