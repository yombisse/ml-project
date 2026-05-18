from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.constants import CLASS_LABELS
from src.utils import load_artifact, load_config, resolve_path
from src.models import run_training_pipeline
from streamlit_app.common import inject_global_styles, require_authentication
from streamlit_app.ui_components import (
    numeric_slider_input,
    section_title,
    result_card,
    confidence_badge,
    form_section_title,
    info_box,
    divider,
)

st.set_page_config(
    page_title="Prédiction Maladie Cardiaque",
    layout="wide"
)

# Inject CSS immediately at page load
inject_global_styles()

require_authentication("Prédiction")

# Back button
if st.button("← Retour à l'accueil"):
    st.switch_page("pages/00_Accueil.py")

st.title("Système de Prédiction de Maladie Cardiaque")

config = load_config()
model_path = resolve_path(f"{config['paths']['models']}/best_model.joblib")

if not model_path.exists():
    st.warning("Modèle non disponible.")
    if st.button("Entraîner le modèle"):
        run_training_pipeline()
        st.success("Modèle entraîné avec succès.")
        st.rerun()
    st.stop()

model = load_artifact(model_path)


# Main form
section_title("Formulaire de Prédiction", icon="heart-pulse")

with st.form("formulaire_prediction"):
    
    # Section 1: Données Générales
    form_section_title("Données Générales", icon="user-md")
    col1, col2 = st.columns(2)
    
    with col1:
        age = numeric_slider_input(
            "âge : Âge de l'individu en années.", 

            key="patient_age",
            min_value=29,
            max_value=77,
            step=1,
            default=54,
            unit="ans"
        )
    
    with col2:
        sexe = st.selectbox(
            "sexe : Sexe de l'individu (1 = homme ; 0 = femme)",

            [0, 1],
            format_func=lambda x: "Femme" if x == 0 else "Homme",
            key="patient_sexe"
        )
    
    douleur_poitrine = st.selectbox(
        "cp : Type de douleur thoracique (0 à 3, représentant différents types de douleurs)",

        [0, 1, 2, 3],
        format_func=lambda x: {
            0: "Angine typique",
            1: "Angine atypique",
            2: "Douleur non-angineuse",
            3: "Asymptomatique"
        }[x],
        key="patient_cp"
    )
    
    divider()
    
    # Section 2: Évaluation Cardiaque
    form_section_title("Évaluation Cardiaque", icon="heartbeat")
    col1, col2 = st.columns(2)
    
    with col1:
        pression_repos = numeric_slider_input(
            "trestbps : Pression artérielle au repos (mm Hg, à l'admission)",

            key="patient_trestbps",
            min_value=90,
            max_value=200,
            step=1,
            default=120,
            unit="mm Hg"
        )
    
    with col2:
        frequence_max = numeric_slider_input(
            "thalach : Fréquence cardiaque maximale atteinte (bpm)",
            key="patient_thalach",

            min_value=70,
            max_value=210,
            step=1,
            default=150,
            unit="bpm"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        angine_effort = st.selectbox(
            "exang : Angine induite par l'exercice (1 = oui ; 0 = non)",

            [0, 1],
            format_func=lambda x: "Oui" if x == 1 else "Non",
            key="patient_exang"
        )
    
    with col2:
        electrocardiogramme = st.selectbox(
            "restecg : Résultats électrocardiographiques au repos (0, 1, 2)",

            [0, 1, 2],
            format_func=lambda x: {
                0: "Normal",
                1: "Anomalie ST-T",
                2: "Hypertrophie ventriculaire gauche"
            }[x],
            key="patient_restecg"
        )
    
    divider()
    
    # Section 3: Paramètres Sanguins
    form_section_title("Paramètres Sanguins", icon="droplet")
    col1, col2 = st.columns(2)
    
    with col1:
        cholesterol = numeric_slider_input(
            "chol : Cholestérol sérique (mg/dl)",

            key="patient_chol",
            min_value=100,
            max_value=600,
            step=5,
            default=200,
            unit="mg/dl"
        )
    
    with col2:
        glycemie = st.selectbox(
            "fbs : Glycémie à jeun > 120 mg/dl (1 = vrai ; 0 = faux)",

            [0, 1],
            format_func=lambda x: "Vrai" if x == 1 else "Faux",
            key="patient_fbs"
        )
    
    divider()
    
    # Section 4: Analyses Supplémentaires
    form_section_title("Analyses Supplémentaires", icon="flask")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        depression_st = numeric_slider_input(
            "oldpeak : Dépression du segment ST induite par l'exercice (vs repos)",

            key="patient_oldpeak",
            min_value=0.0,
            max_value=6.5,
            step=0.1,
            default=1.0,
            unit=""
        )
    
    with col2:
        pente_st = st.selectbox(
            "slope : Pente du segment ST au pic de l'exercice (0, 1, 2)",

            [0, 1, 2],
            format_func=lambda x: {
                0: "Descendante",
                1: "Plate",
                2: "Montante"
            }[x],
            key="patient_slope"
        )
    
    with col3:
        vaisseaux = st.selectbox(
            "ca : Nombre de gros vaisseaux (0-3) colorés par fluoroscopie",

            [0, 1, 2, 3],
            key="patient_ca"
        )
    
    thalassemie = st.selectbox(
        "thal : Trouble sanguin (3 = normal ; 6 = défaut fixé ; 7 = défaut réversible)",

        [3, 6, 7],
        format_func=lambda x: {
            3: "Normal",
            6: "Défaut fixé",
            7: "Défaut réversible"
        }[x],
        key="patient_thal"
    )
    
    divider()
    
    envoyer = st.form_submit_button("🏥 Analyser le Patient", use_container_width=True)


if envoyer:
    
    # Prepare data
    data = pd.DataFrame([{
        "age": age,
        "sex": sexe,
        "cp": douleur_poitrine,
        "trestbps": pression_repos,
        "chol": cholesterol,
        "fbs": glycemie,
        "restecg": electrocardiogramme,
        "thalach": frequence_max,
        "exang": angine_effort,
        "oldpeak": depression_st,
        "slope": pente_st,
        "ca": vaisseaux,
        "thal": thalassemie
    }])
    
    # Make predictions
    prediction = model.predict(data)[0]
    prob = None
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(data)[0][1]
    
    # Determine risk level
    if prob is not None:
        if prob >= 0.65:
            risk_level = "high"
            risk_title = "Risque Élevé de Maladie Cardiaque"
            icon_class = "heart-crack"
            description = f"La probabilité de maladie cardiaque est de {prob:.1%}, ce qui indique un risque significatif."
            recommendation = """
            <strong>Recommandations urgentes :</strong>
            <ul>
                <li>Consultation cardiologique recommandée dans les prochains jours</li>
                <li>Envisager une évaluation diagnostique complète (ECG, tests d'effort, échocardiographie)</li>
                <li>Mise en place d'un traitement préventif ou thérapeutique selon les résultats</li>
            </ul>
            """
        elif prob >= 0.35:
            risk_level = "medium"
            risk_title = "Risque Modéré de Maladie Cardiaque"
            icon_class = "heart-pulse"
            description = f"La probabilité de maladie cardiaque est de {prob:.1%}, ce qui indique un risque modéré."
            recommendation = """
            <strong>Recommandations prudentielles :</strong>
            <ul>
                <li>Suivi médical régulier avec votre médecin généraliste</li>
                <li>Examens de contrôle recommandés dans 3-6 mois</li>
                <li>Amélioration du mode de vie (alimentation, exercice, stress)</li>
                <li>Considérer une consultation cardiologique si facteurs de risque additionnels</li>
            </ul>
            """
        else:
            risk_level = "low"
            risk_title = "Risque Faible de Maladie Cardiaque"
            icon_class = "heart"
            description = f"La probabilité de maladie cardiaque est de {prob:.1%}, ce qui indique un risque faible."
            recommendation = """
            <strong>Recommandations préventives :</strong>
            <ul>
                <li>Continuer un mode de vie sain et équilibré</li>
                <li>Maintenir une activité physique régulière</li>
                <li>Suivi médical annuel recommandé</li>
                <li>Contrôle régulier de la tension artérielle et du cholestérol</li>
            </ul>
            """
    else:
        risk_level = "medium"
        risk_title = "Évaluation Non Disponible"
        icon_class = "question-circle"
        description = "Le modèle n'a pas pu calculer la probabilité de risque."
        recommendation = "<strong>Veuillez consulter un professionnel de santé pour une évaluation complète.</strong>"
    
    # Display result
    st.markdown("")
    section_title("Résultat de l'Analyse", icon="stethoscope")
    
    result_card(
        title=risk_title,
        description=description,
        recommendation=recommendation,
        risk_level=risk_level,
        icon=icon_class
    )
    
    if prob is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            confidence_badge(risk_level, prob)
        with col2:
            st.metric("Probabilité", f"{prob:.1%}")
        with col3:
            st.metric("Confiance du Modèle", f"{max(prob, 1-prob):.1%}")
    
    divider()
    
    # Medical disclaimer
    info_box(
        title="Avis de Non-Responsabilité Médical",
        icon="exclamation-triangle",
        message="""
        Ce résultat est généré par un modèle de machine learning à titre informatif uniquement.
        <strong>Il ne remplace en aucun cas un diagnostic médical professionnel.</strong>
        Consultez toujours un cardiologue ou votre médecin généraliste pour une évaluation clinique complète
        et des conseils médicaux personnalisés.
        """
    )
