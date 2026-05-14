import pandas as pd

from src.evaluation import compare_test_metrics
from src.models import train_all_models
from src.preprocessing import split_dataset


def test_compare_test_metrics_returns_required_columns():
    X_train, X_test, y_train, y_test = split_dataset()
    fitted_models = train_all_models(X_train, y_train)
    results = compare_test_metrics(fitted_models, X_test, y_test)

    expected = {"model", "accuracy", "precision", "recall", "f1_score", "roc_auc"}
    assert expected.issubset(set(results.columns))
    assert isinstance(results, pd.DataFrame)
