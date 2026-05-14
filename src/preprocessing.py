"""Data loading and preprocessing utilities for the Heart Disease dataset."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.constants import CATEGORICAL_FEATURES, DATASET_COLUMNS, NUMERIC_FEATURES
from src.utils import load_config, resolve_path


def load_raw_dataset(config: dict[str, Any] | None = None) -> pd.DataFrame:
    """Load the raw Cleveland file and assign the expected columns."""
    loaded_config = config or load_config()
    raw_path = resolve_path(loaded_config["data"]["raw_path"])
    columns = loaded_config["data"].get("columns", DATASET_COLUMNS)
    dataframe = pd.read_csv(raw_path, header=None, names=columns, na_values="?")
    return dataframe


def prepare_dataset(
    dataframe: pd.DataFrame | None = None,
    config: dict[str, Any] | None = None,
    save_processed: bool = True,
) -> pd.DataFrame:
    """Clean the dataset and convert the multiclass target into a binary target."""
    loaded_config = config or load_config()
    df = dataframe.copy() if dataframe is not None else load_raw_dataset(loaded_config)

    df["target"] = (df["target"].astype(float) > 0).astype(int)
    for column in NUMERIC_FEATURES + ["ca", "thal"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if save_processed:
        processed_path = resolve_path(loaded_config["data"]["processed_path"])
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(processed_path, index=False)

    return df


def get_feature_target_split(
    dataframe: pd.DataFrame,
    target_column: str = "target",
) -> tuple[pd.DataFrame, pd.Series]:
    """Split a dataframe into features and target."""
    features = dataframe.drop(columns=[target_column])
    target = dataframe[target_column]
    return features, target


def build_preprocessor(config: dict[str, Any] | None = None) -> ColumnTransformer:
    """Build the shared preprocessing transformer with imputation and encoding."""
    loaded_config = config or load_config()
    preprocessing_config = loaded_config["preprocessing"]
    numeric_features = preprocessing_config.get("numeric_features", NUMERIC_FEATURES)
    categorical_features = preprocessing_config.get("categorical_features", CATEGORICAL_FEATURES)

    numeric_steps = [
        ("imputer", SimpleImputer(strategy=preprocessing_config["missing_strategy_numeric"])),
    ]
    if preprocessing_config.get("scaling", True):
        numeric_steps.append(("scaler", StandardScaler()))

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy=preprocessing_config["missing_strategy_categorical"])),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", Pipeline(steps=numeric_steps), numeric_features),
            ("categorical", categorical_transformer, categorical_features),
        ]
    )


def split_dataset(
    dataframe: pd.DataFrame | None = None,
    config: dict[str, Any] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Prepare the cleaned dataframe and produce a stratified train/test split."""
    loaded_config = config or load_config()
    df = prepare_dataset(dataframe=dataframe, config=loaded_config, save_processed=True)
    features, target = get_feature_target_split(df, loaded_config["data"]["target"])

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=loaded_config["data"]["test_size"],
        random_state=loaded_config["data"]["random_state"],
        stratify=target,
    )
    return X_train, X_test, y_train, y_test


def load_processed_dataset(config: dict[str, Any] | None = None) -> pd.DataFrame:
    """Load the processed dataset if it exists, otherwise build it."""
    loaded_config = config or load_config()
    processed_path = resolve_path(loaded_config["data"]["processed_path"])
    if not processed_path.exists():
        return prepare_dataset(config=loaded_config, save_processed=True)
    return pd.read_csv(processed_path)
