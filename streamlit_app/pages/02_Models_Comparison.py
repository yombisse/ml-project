from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from streamlit_app.common import (
    inject_global_styles,
    render_export_menu,
    require_authentication,
)
from src.constants import MODEL_DISPLAY_NAMES, PATIENT_FRIENDLY_METRICS
from src.models import run_training_pipeline
from src.utils import load_config, resolve_path


config = load_config()
models_dir = resolve_path(config["paths"]["models"])
cv_results_path = models_dir / "cv_results.csv"
test_results_path = models_dir / "test_results.csv"


@st.cache_data
def load_results() -> tuple[pd.DataFrame, pd.DataFrame]:
    cv_df = pd.read_csv(cv_results_path)
    test_df = pd.read_csv(test_results_path)
    return cv_df, test_df


def beautify_models(dataframe: pd.DataFrame) -> pd.DataFrame:
    df = dataframe.copy()
    df["model"] = df["model"].map(MODEL_DISPLAY_NAMES).fillna(df["model"])
    return df


# Inject CSS immediately at page load
inject_global_styles()

require_authentication("Comparaison")

# Back button
if st.button("← Retour à l'accueil"):
    st.switch_page("pages/00_Accueil.py")

st.title("Resultats globaux")
st.caption("Cette page aide a voir quelle solution offre les resultats les plus solides sur ce jeu de donnees.")

if not cv_results_path.exists() or not test_results_path.exists():
    st.warning("Les resultats ne sont pas encore disponibles.")
    if st.button("Generer les resultats", type="primary"):
        with st.spinner("Preparation des resultats en cours..."):
            run_training_pipeline()
        st.success("Les resultats sont maintenant disponibles.")
        st.rerun()
    st.stop()

cv_df, test_df = load_results()
cv_df = beautify_models(cv_df)
test_df = beautify_models(test_df)

best_model = cv_df.iloc[0]["model"]
top1, top2, top3 = st.columns(3)
top1.metric("Solution recommandee", best_model)
top2.metric("Meilleure qualite globale", f"{test_df.iloc[0]['roc_auc']:.3f}")
top3.metric("Meilleur equilibre global", f"{test_df['f1_score'].max():.3f}")

export_col1, export_col2 = st.columns(2)
with export_col1:
    render_export_menu(test_df, "resultats_modeles", "resultats")
with export_col2:
    st.empty()

tab1, tab2, tab3 = st.tabs(["Classement general", "Resultats detailles", "Lecture simple"])

with tab1:
    st.subheader("Classement general")
    st.dataframe(cv_df.round(3), use_container_width=True)

    cv_bar = px.bar(
        cv_df,
        x="model",
        y="cv_roc_auc_mean",
        color="cv_f1_mean",
        title="Comparaison generale des solutions",
        labels={"model": "Solution", "cv_roc_auc_mean": "Qualite moyenne"},
        color_continuous_scale="Tealgrn",
    )
    st.plotly_chart(cv_bar, use_container_width=True)

with tab2:
    st.subheader("Resultats detailles")
    st.dataframe(test_df.round(3), use_container_width=True)

    test_long = test_df.melt(
        id_vars="model",
        value_vars=["accuracy", "precision", "recall", "f1_score", "roc_auc"],
        var_name="metric",
        value_name="score",
    )
    test_long["metric"] = test_long["metric"].map(PATIENT_FRIENDLY_METRICS).fillna(test_long["metric"])

    line_fig = px.line(
        test_long,
        x="metric",
        y="score",
        color="model",
        markers=True,
        title="Evolution des scores par solution",
    )
    st.plotly_chart(line_fig, use_container_width=True)

with tab3:
    st.success(f"La solution la plus stable pour cette application est : {best_model}.")
    st.markdown(
        """
        **Comment lire cette page**

        - `Exactitude globale` : montre la part de bonnes reponses.
        - `Fiabilite des alertes` : indique si les alertes positives sont souvent justes.
        - `Detection des cas a risque` : montre la capacite a reperer les cas a surveiller.
        - `Equilibre global` : resume l'ensemble.
        - `Qualite generale` : donne une vue d'ensemble de la performance.
        """
    )
    st.info(
        "Pour cette application, nous retenons la solution la plus stable sur l'ensemble des essais, "
        "puis nous verifions ensuite son comportement sur les donnees de controle."
    )
