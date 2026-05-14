"""Simple entry point to train models and generate project artifacts."""

from src.models import run_training_pipeline


if __name__ == "__main__":
    result = run_training_pipeline()
    print(f"Meilleur modele retenu: {result['best_model_name']}")
