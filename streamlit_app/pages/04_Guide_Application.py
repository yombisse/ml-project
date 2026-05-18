from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from streamlit_app.common import inject_global_styles, require_authentication


# Inject CSS immediately at page load
inject_global_styles()

require_authentication("Guide")

# Back button
if st.button("← Retour à l'accueil"):
    st.switch_page("pages/00_Accueil.py")

st.title("Guide rapide")
st.caption("Cette page explique comment utiliser l'application de facon simple et fluide.")

step1, step2, step3 = st.columns(3)
step1.info("1. Consultez la vue d'ensemble pour voir le profil general des donnees.")
step2.info("2. Ouvrez les resultats globaux pour comparer les solutions.")
step3.info("3. Utilisez l'estimation individuelle pour tester un profil patient.")

st.subheader("Conseils d'utilisation")
st.markdown(
    """
    - Commencez par la page d'accueil pour vous orienter.
    - Passez ensuite a la vue d'ensemble pour comprendre les principales tendances.
    - Consultez les resultats globaux avant d'utiliser l'estimation individuelle.
    - Utilisez les boutons de telechargement pour conserver les resultats.
    """
)

st.subheader("Bonnes pratiques")
st.markdown(
    """
    - Verifiez les informations saisies avant de valider.
    - Comparez plusieurs profils si vous souhaitez observer les differences.
    - Gardez en tete qu'il s'agit d'un outil de demonstration academique.
    """
)
