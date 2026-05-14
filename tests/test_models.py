from src.models import build_model_pipelines, get_estimators


def test_get_estimators_contains_six_required_models():
    estimators = get_estimators()
    assert len(estimators) == 6
    assert "adaboost" in estimators


def test_build_model_pipelines_wrap_estimators():
    pipelines = build_model_pipelines()
    assert "svm" in pipelines
    assert hasattr(pipelines["svm"], "predict")
