from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from streamlit_app.common import init_session, inject_global_styles, load_config, login_form, logger, render_login_shell


config = load_config()
st.set_page_config(
    page_title=config["streamlit"]["page_title"],
    page_icon=config["streamlit"]["page_icon"],
    layout=config["streamlit"]["layout"],
)

init_session()
inject_global_styles()
logger.info("Accueil page loaded.")

if st.session_state.get("authenticated", False):
    st.switch_page("pages/01_EDA.py")


@st.dialog("Connexion")
def open_login_dialog() -> None:
    st.markdown(
        """
        <div class="login-dialog-copy">
            <h3>Heart Disease Prediction</h3>
            <p>Connectez-vous pour acceder au tableau de bord, aux analyses et a l'outil de prediction.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    login_form()


render_login_shell()

left, center, right = st.columns([1, 1, 1])
with center:
    if st.button("Connexion", type="primary", use_container_width=True):
        open_login_dialog()

st.markdown(
    """
    <div class="section-card" style="margin-top: 0.8rem;">
        <h2>Accueil</h2>
        <p>
            Bienvenue dans l'application de demonstration. Cliquez sur le bouton ci-dessus
            pour ouvrir le formulaire de connexion et acceder directement a la premiere section.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
