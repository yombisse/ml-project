from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from streamlit_app.common import (
    render_export_menu,
    require_authentication,
)
from src.constants import CLASS_LABELS
from src.models import run_training_pipeline
from src.utils import load_artifact, load_config, resolve_path


config = load_config()
best_model_path = resolve_path(f"{config['paths']['models']}/best_model.joblib")

require_authentication("Prediction")

st.title("Prediction du risque de maladie cardiaque")
st.caption("Renseignez les informations utiles et obtenez un resultat clair, telechargeable et facile a presenter.")

with st.expander("Aide rapide"):
    st.markdown(
        """
        - Choisissez simplement la valeur qui correspond le mieux au profil observe.
        - Si vous n'etes pas certain d'une valeur, utilisez les choix les plus proches.
        - Le resultat donne une estimation d'aide a la decision dans le cadre du projet.
        """
    )

if not best_model_path.exists():
    st.warning("Le modele n'est pas encore disponible.")
    if st.button("Preparer l'outil de prediction", type="primary"):
        with st.spinner("Preparation en cours..."):
            run_training_pipeline()
        st.success("L'outil de prediction est pret.")
        st.rerun()
    st.stop()

model = load_artifact(f"{config['paths']['models']}/best_model.joblib")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 29, 77, 54)
        sex = st.selectbox("Sexe", [0, 1], format_func=lambda x: "Femme" if x == 0 else "Homme")
        cp = st.selectbox(
            "Douleur thoracique",
            [1, 2, 3, 4],
            format_func=lambda x: {
                1: "Type 1",
                2: "Type 2",
                3: "Type 3",
                4: "Type 4",
            }[x],
        )
        trestbps = st.slider("Pression arterielle au repos", 90, 200, 130)
        chol = st.slider("Cholesterol", 100, 600, 245)

    with col2:
        fbs = st.selectbox("Glycemie elevee", [0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
        restecg = st.selectbox("Observation ECG", [0, 1, 2], format_func=lambda x: f"Niveau {x}")
        thalach = st.slider("Frequence cardiaque maximale", 70, 210, 150)
        exang = st.selectbox("Gene a l'effort", [0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
        oldpeak = st.slider("Variation a l'effort", 0.0, 6.5, 1.0, step=0.1)
        slope = st.selectbox("Evolution du signal", [1, 2, 3], format_func=lambda x: f"Niveau {x}")
        ca = st.selectbox("Nombre de vaisseaux visibles", [0, 1, 2, 3])
        thal = st.selectbox("Etat thal", [3, 6, 7], format_func=lambda x: {3: "Normal", 6: "Fixe", 7: "Reversible"}[x])

    submitted = st.form_submit_button("Afficher le resultat", type="primary")

if submitted:
    input_data = pd.DataFrame(
        [
            {
                "age": age,
                "sex": sex,
                "cp": cp,
                "trestbps": trestbps,
                "chol": chol,
                "fbs": fbs,
                "restecg": restecg,
                "thalach": thalach,
                "exang": exang,
                "oldpeak": oldpeak,
                "slope": slope,
                "ca": ca,
                "thal": thal,
            }
        ]
    )

    prediction = int(model.predict(input_data)[0])
    probability = float(model.predict_proba(input_data)[0][1]) if hasattr(model, "predict_proba") else None

    result_df = input_data.copy()
    result_df["resultat"] = CLASS_LABELS[prediction]
    if probability is not None:
        result_df["probabilite"] = round(probability, 4)
    st.session_state["last_prediction_df"] = result_df

    if prediction == 1:
        st.error(CLASS_LABELS[prediction])
    else:
        st.success(CLASS_LABELS[prediction])

    if probability is not None:
        st.progress(probability, text=f"Niveau estime : {probability:.1%}")
        if probability < 0.35:
            st.info("Le niveau estime est faible.")
        elif probability < 0.65:
            st.warning("Le niveau estime est moyen.")
        else:
            st.error("Le niveau estime est eleve.")

    st.caption("Ce resultat est fourni a titre d'illustration dans le cadre du projet.")
    st.dataframe(result_df, use_container_width=True)

if st.session_state.get("last_prediction_df") is not None:
    render_export_menu(st.session_state["last_prediction_df"], "prediction_resultat", "prediction")
