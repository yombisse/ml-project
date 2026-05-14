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
    render_export_menu,
    require_authentication,
)
from src.preprocessing import load_processed_dataset


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_processed_dataset()


require_authentication("Analyse")

st.title("Vue d'ensemble des donnees")
st.caption("Cette page aide a visualiser rapidement le profil general des patients du jeu de donnees.")

df = get_data()

header_left, header_right = st.columns((1.2, 0.8))
with header_left:
    st.markdown(
        """
        <div class="section-card">
            <h3>Ce que vous pouvez voir ici</h3>
            <p>
                Les graphiques ci-dessous montrent l'age des patients, la repartition generale
                et quelques facteurs importants observables dans le jeu de donnees.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_right:
    render_export_menu(df, "heart_disease_processed", "donnees")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Nombre de patients", len(df))
metric_2.metric("Informations suivies", df.shape[1] - 1)
metric_3.metric("Situation rassurante", int((df["target"] == 0).sum()))
metric_4.metric("Vigilance recommandee", int((df["target"] == 1).sum()))

left, right = st.columns((1.2, 1))
with left:
    age_fig = px.histogram(
        df,
        x="age",
        color=df["target"].map({0: "Situation rassurante", 1: "Vigilance recommandee"}),
        nbins=20,
        barmode="overlay",
        color_discrete_sequence=["#6cae75", "#d95f02"],
        title="Age des patients",
    )
    st.plotly_chart(age_fig, use_container_width=True)

with right:
    target_fig = px.pie(
        df,
        names=df["target"].map({0: "Situation rassurante", 1: "Vigilance recommandee"}),
        title="Repartition generale",
        color_discrete_sequence=["#6cae75", "#d95f02"],
    )
    st.plotly_chart(target_fig, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    sex_fig = px.histogram(
        df,
        x=df["sex"].map({0: "Femme", 1: "Homme"}),
        color=df["target"].map({0: "Situation rassurante", 1: "Vigilance recommandee"}),
        barmode="group",
        title="Repartition selon le sexe",
        labels={"x": "Sexe", "color": "Observation"},
    )
    st.plotly_chart(sex_fig, use_container_width=True)

with row2_col2:
    cp_fig = px.histogram(
        df,
        x="cp",
        color=df["target"].map({0: "Situation rassurante", 1: "Vigilance recommandee"}),
        barmode="group",
        title="Type de douleur thoracique observe",
        labels={"cp": "Categorie", "color": "Observation"},
    )
    st.plotly_chart(cp_fig, use_container_width=True)

summary = (
    df.groupby("target")[["trestbps", "chol", "thalach"]]
    .mean()
    .rename(index={0: "Situation rassurante", 1: "Vigilance recommandee"})
    .round(2)
)
st.subheader("Moyennes observees")
st.dataframe(summary, use_container_width=True)

row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    fbs_fig = px.histogram(
        df,
        x=df["fbs"].map({0: "Glycemie normale", 1: "Glycemie elevee"}),
        color=df["target"].map({0: "Situation rassurante", 1: "Vigilance recommandee"}),
        barmode="group",
        title="Glycemie a jeun",
    )
    st.plotly_chart(fbs_fig, use_container_width=True)

with row3_col2:
    exang_fig = px.histogram(
        df,
        x=df["exang"].map({0: "Sans gene a l'effort", 1: "Gene a l'effort"}),
        color=df["target"].map({0: "Situation rassurante", 1: "Vigilance recommandee"}),
        barmode="group",
        title="Ressenti a l'effort",
    )
    st.plotly_chart(exang_fig, use_container_width=True)
