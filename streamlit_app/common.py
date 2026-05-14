from __future__ import annotations

import base64
import io
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils import load_config, resolve_path, setup_logger


config = load_config()
logger = setup_logger("streamlit", config)


def get_image_paths() -> list[Path]:
    images_dir = resolve_path(config["streamlit"].get("assets_images_path", "assets/images"))
    if not images_dir.exists():
        return []
    return sorted([path for path in images_dir.iterdir() if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}])


def image_to_data_uri(path: Path) -> str:
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def init_session() -> None:
    query_params = st.query_params
    persisted_auth = query_params.get("auth", "0") == "1"
    persisted_user = query_params.get("user", "")

    st.session_state.setdefault("authenticated", persisted_auth)
    st.session_state.setdefault("user_email", persisted_user)
    st.session_state.setdefault("last_prediction_df", None)
    st.session_state.setdefault("show_login_form", False)


def persist_auth_in_url() -> None:
    if st.session_state.get("authenticated", False) and st.session_state.get("user_email"):
        st.query_params["auth"] = "1"
        st.query_params["user"] = st.session_state["user_email"]


def authenticate_user(email: str, password: str) -> bool:
    demo_user = config["auth"]["demo_user"]
    return email.strip().lower() == demo_user["email"].lower() and password == demo_user["password"]


def login_form() -> None:
    init_session()
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter", type="primary")

    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.caption("Compte de demonstration")
        st.code(f"Email : {config['auth']['demo_user']['email']}\nMot de passe : {config['auth']['demo_user']['password']}")
    with info_col2:
        st.caption("Acces")
        st.write("Une fois connecte, vous pourrez naviguer librement dans toute l'application.")

    if submit:
        if authenticate_user(email, password):
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = email.strip()
            st.session_state["show_login_form"] = False
            persist_auth_in_url()
            logger.info("Successful login for %s", email.strip())
            st.success("Connexion reussie.")
            st.switch_page("pages/01_EDA.py")
        else:
            st.error("Email ou mot de passe incorrect.")
            logger.warning("Failed login attempt for %s", email.strip())


def require_authentication(page_title: str) -> None:
    init_session()
    if not st.session_state.get("authenticated", False):
        st.switch_page("pages/00_Accueil.py")
    persist_auth_in_url()
    render_sidebar(page_title)


def logout() -> None:
    logger.info("User logged out: %s", st.session_state.get("user_email", "unknown"))
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = ""
    st.session_state["last_prediction_df"] = None
    st.session_state["show_login_form"] = False
    st.query_params.clear()
    st.switch_page("pages/00_Accueil.py")


def render_sidebar(current_page: str) -> None:
    with st.sidebar:
        st.markdown("## Heart Prediction")
        st.write(f"Connecte en tant que : **{st.session_state.get('user_email', 'Utilisateur')}**")
        st.caption(f"Page en cours : {current_page}")
        st.markdown("---")
        st.page_link("pages/01_EDA.py", label="Vue d'ensemble")
        st.page_link("pages/02_Models_Comparison.py", label="Resultats globaux")
        st.page_link("pages/03_Prediction.py", label="Estimation individuelle")
        st.page_link("pages/04_Guide_Application.py", label="Guide")
        st.markdown("---")
        if st.button("Se deconnecter", use_container_width=True):
            logout()


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(31, 119, 180, 0.06), transparent 25%),
                radial-gradient(circle at bottom right, rgba(16, 150, 72, 0.07), transparent 28%),
                linear-gradient(180deg, #fbfdfc 0%, #f5f8fb 100%);
        }
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.9rem 1.2rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.86);
            border: 1px solid rgba(17, 51, 43, 0.08);
            margin-bottom: 1rem;
            backdrop-filter: blur(8px);
        }
        .brand {
            font-size: 1.05rem;
            font-weight: 700;
            color: #11332b;
        }
        .nav-links {
            color: #35544c;
            font-size: 0.92rem;
        }
        .login-shell {
            position: relative;
            min-height: 78vh;
            border-radius: 26px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.18);
            box-shadow: 0 20px 40px rgba(17, 51, 43, 0.12);
        }
        .carousel-layer {
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center;
            opacity: 0;
            animation: fadeSlide 25s infinite;
        }
        .carousel-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(9,27,24,0.68), rgba(15,47,76,0.50));
        }
        .overlay-content {
            position: relative;
            z-index: 2;
            display: flex;
            align-items: center;
            min-height: 78vh;
            padding: 1.4rem;
        }
        .welcome-panel {
            color: white;
            padding: 2rem;
            max-width: 48rem;
        }
        .welcome-panel h1 {
            font-size: 2.5rem;
            line-height: 1.1;
            margin-bottom: 0.8rem;
        }
        .welcome-panel p {
            font-size: 1.02rem;
            color: rgba(255,255,255,0.86);
            max-width: 40rem;
        }
        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 1rem;
        }
        .pill {
            padding: 0.55rem 0.9rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.18);
            color: white;
            font-size: 0.9rem;
        }
        .login-card h1 {
            color: #11332b;
            margin-bottom: 0.3rem;
        }
        .login-card p {
            color: #49635d;
        }
        .login-dialog-copy {
            color: #11332b;
            margin-bottom: 0.85rem;
        }
        .login-dialog-copy p {
            color: #35544c;
            margin-bottom: 0;
        }
        .hero-button {
            display: inline-block;
            padding: 0.85rem 1.2rem;
            background: rgba(255,255,255,0.96);
            color: #11332b;
            border-radius: 14px;
            font-weight: 700;
            border: 0;
            margin-top: 1rem;
        }
        .section-card {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(17, 51, 43, 0.08);
            margin-bottom: 1rem;
        }
        section[data-testid="stSidebar"] button[kind="secondary"] {
            background: #fdecea !important;
            color: #b71c1c !important;
            border-color: #f5c6c6 !important;
        }
        section[data-testid="stSidebar"] button[kind="secondary"]:hover {
            background: #c62828 !important;
            color: white !important;
            border-color: #c62828 !important;
        }
        @keyframes fadeSlide {
            0% { opacity: 0; }
            8% { opacity: 1; }
            28% { opacity: 1; }
            36% { opacity: 0; }
            100% { opacity: 0; }
        }
        @media (max-width: 900px) {
            .overlay-content {
                min-height: auto;
            }
            .welcome-panel {
                padding: 1rem;
            }
            .welcome-panel h1 {
                font-size: 2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_topbar() -> None:
    st.markdown(
        """
        <div class="topbar">
            <div class="brand">Heart Disease Prediction</div>
            <div class="nav-links">Analyse | Resultats | Prediction | Guide</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login_shell() -> None:
    images = get_image_paths()
    slide_html = ""
    for index, image_path in enumerate(images):
        delay = index * 5
        slide_html += (
            f"<div class='carousel-layer' style=\"background-image:url('{image_to_data_uri(image_path)}');"
            f"animation-delay:{delay}s;\"></div>"
        )

    if not slide_html:
        slide_html = "<div class='carousel-layer' style=\"opacity:1;background:linear-gradient(135deg,#0f3d34,#1d6784);\"></div>"

    st.markdown(
        f"""
        <div class="login-shell">
            {slide_html}
            <div class="carousel-overlay"></div>
            <div class="overlay-content">
                <div class="welcome-panel">
                    <div class="pill-row">
                        <div class="pill">Prediction accompagnee</div>
                        <div class="pill">Interface claire</div>
                        <div class="pill">Resultats telechargeables</div>
                    </div>
                    <h1>Une application simple pour visualiser et estimer le risque cardiaque.</h1>
                    <p>
                        Cette interface a ete pensee pour guider l'utilisateur pas a pas :
                        comprendre les donnees, voir les resultats et obtenir une estimation
                        individuelle de facon lisible.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dataframe_to_csv_bytes(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8")


def excel_export_available() -> bool:
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        return False
    return True


def dataframe_to_excel_bytes(dataframe: pd.DataFrame, sheet_name: str = "donnees") -> bytes:
    if not excel_export_available():
        raise ImportError("openpyxl is required for Excel export.")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name=sheet_name)
    buffer.seek(0)
    return buffer.getvalue()


def render_export_menu(dataframe: pd.DataFrame, base_filename: str, sheet_name: str, label: str = "Exporter") -> None:
    with st.popover(label, use_container_width=True):
        st.download_button(
            "Telecharger en CSV",
            data=dataframe_to_csv_bytes(dataframe),
            file_name=f"{base_filename}.csv",
            mime="text/csv",
            use_container_width=True,
        )
        if excel_export_available():
            st.download_button(
                "Telecharger en Excel",
                data=dataframe_to_excel_bytes(dataframe, sheet_name),
                file_name=f"{base_filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        else:
            st.caption("Le format Excel est momentanement indisponible.")
