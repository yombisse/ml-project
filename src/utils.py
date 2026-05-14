"""Shared utility helpers for configuration, artifacts and logging."""

from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import joblib
import yaml


ROOT_DIR = Path(__file__).resolve().parents[1]


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load the YAML configuration file."""
    path = Path(config_path) if config_path else ROOT_DIR / "config.yaml"
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def resolve_path(relative_path: str | Path) -> Path:
    """Resolve a project-relative path from the repository root."""
    return ROOT_DIR / Path(relative_path)


def ensure_project_directories(config: dict[str, Any]) -> None:
    """Create the main working directories referenced by the configuration."""
    for key in ("models", "logs"):
        resolve_path(config["paths"][key]).mkdir(parents=True, exist_ok=True)
    resolve_path("data/processed").mkdir(parents=True, exist_ok=True)


def setup_logger(name: str, config: dict[str, Any] | None = None) -> logging.Logger:
    """Return a rotating file logger configured from config.yaml."""
    loaded_config = config or load_config()
    ensure_project_directories(loaded_config)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_files = loaded_config["logging"].get("files", {})
    configured_file = log_files.get(name, loaded_config["logging"]["file"])
    log_file = resolve_path(configured_file)
    handler = RotatingFileHandler(
        log_file,
        maxBytes=loaded_config["logging"]["max_file_size"],
        backupCount=loaded_config["logging"]["backup_count"],
        encoding="utf-8",
    )
    formatter = logging.Formatter(loaded_config["logging"]["format"])
    handler.setFormatter(formatter)

    logger.setLevel(getattr(logging, loaded_config["logging"]["level"].upper(), logging.INFO))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def save_artifact(obj: Any, relative_path: str | Path) -> Path:
    """Persist an artifact with joblib and return its absolute path."""
    path = resolve_path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, path)
    return path


def load_artifact(relative_path: str | Path) -> Any:
    """Load an artifact stored with joblib."""
    return joblib.load(resolve_path(relative_path))


def save_json(data: dict[str, Any], relative_path: str | Path) -> Path:
    """Persist metadata as formatted JSON."""
    path = resolve_path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
    return path
