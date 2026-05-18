from __future__ import annotations

import base64
import io
import importlib.util
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils import load_config, resolve_path, setup_logger
from streamlit_app.theme import inject_medical_theme


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
    st.session_state.setdefault("confirm_logout", False)


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

    st.markdown(
        f"""
        <div class="demo-box">
            <div class="demo-title">Compte de demonstration</div>
            <div class="demo-grid">
                <div class="demo-item">
                    <span class="demo-label">Email</span>
                    <strong>{config['auth']['demo_user']['email']}</strong>
                </div>
                <div class="demo-item">
                    <span class="demo-label">Mot de passe</span>
                    <strong>{config['auth']['demo_user']['password']}</strong>
                </div>
            </div>
            <p class="demo-note">Une fois connecte, vous pourrez naviguer librement dans toute l'application.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
    inject_global_styles()
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


@st.dialog("Confirmer la deconnexion")
def logout_confirmation_dialog() -> None:
    st.write("Voulez-vous vraiment vous deconnecter ?")
    left, right = st.columns(2)
    with left:
        if st.button("Annuler", use_container_width=True):
            st.session_state["confirm_logout"] = False
            st.rerun()
    with right:
        if st.button("Confirmer", type="primary", use_container_width=True):
            st.session_state["confirm_logout"] = False
            logout()


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
            st.session_state["confirm_logout"] = True
    if st.session_state.get("confirm_logout", False):
        logout_confirmation_dialog()


def inject_global_styles() -> None:
    inject_medical_theme()
    st.markdown(
        """
        <style>
        .login-shell {
            position: relative;
            min-height: 72vh;
            border-radius: 28px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18);
            margin-bottom: 1rem;
        }
        .carousel-layer {
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center;
            opacity: 0;
            animation: fadeSlide 25s infinite;
            transform: scale(1.02);
        }
        .carousel-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, rgba(10, 37, 64, 0.75), rgba(5, 150, 105, 0.42));
        }
        .overlay-content {
            position: relative;
            z-index: 2;
            display: flex;
            align-items: center;
            min-height: 72vh;
            padding: 2rem;
        }
        .welcome-panel {
            color: #ffffff;
            max-width: 46rem;
        }
        .welcome-panel h1 {
            color: #ffffff;
            font-size: 3rem;
            line-height: 1.05;
            margin: 1rem 0 0.8rem 0;
            text-shadow: 0 10px 24px rgba(0,0,0,0.2);
        }
        .welcome-panel p {
            color: rgba(255,255,255,0.92);
            font-size: 1.05rem;
            max-width: 40rem;
        }
        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
        }
        .pill {
            padding: 0.55rem 0.95rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.22);
            color: #ffffff;
            font-size: 0.92rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }
        .section-card {
            padding: 1.15rem 1.2rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        }
        .login-dialog-copy h3 {
            color: #0f172a !important;
            margin-bottom: 0.35rem;
        }
        .login-dialog-copy p {
            color: #475569 !important;
        }
        .demo-box {
            margin-top: 1rem;
            padding: 1rem 1.1rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
            border: 1px solid #bfdbfe;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.08);
        }
        .demo-title {
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 0.7rem;
        }
        .demo-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
            margin-bottom: 0.6rem;
        }
        .demo-item {
            background: #ffffff;
            border: 1px solid #dbeafe;
            border-radius: 12px;
            padding: 0.8rem;
        }
        .demo-label {
            display: block;
            font-size: 0.82rem;
            color: #475569;
            margin-bottom: 0.2rem;
        }
        .demo-note {
            color: #475569 !important;
            margin: 0;
            font-size: 0.92rem;
        }
        [data-testid="stDialog"] .stTextInput input,
        [data-testid="stDialog"] .stTextInput input:focus,
        [data-testid="stDialog"] .stNumberInput input,
        [data-testid="stDialog"] .stNumberInput input:focus {
            background: #ffffff !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }
        [data-testid="stDialog"] label,
        [data-testid="stDialog"] p,
        [data-testid="stDialog"] span,
        [data-testid="stDialog"] div {
            color: #0f172a;
        }
        [data-testid="stDialog"] code {
            color: #0f172a !important;
        }
        [data-testid="stDialog"] button[aria-label*="password"] svg,
        [data-testid="stDialog"] [data-baseweb="input"] svg {
            fill: #ffffff !important;
            color: #ffffff !important;
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
                min-height: 60vh;
                padding: 1.25rem;
            }
            .welcome-panel h1 {
                font-size: 2.2rem;
            }
            .demo-grid {
                grid-template-columns: 1fr;
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


def get_excel_engine() -> str:
    """Return the first available Excel writer engine."""
    if importlib.util.find_spec("openpyxl") is not None:
        return "openpyxl"
    if importlib.util.find_spec("xlsxwriter") is not None:
        return "xlsxwriter"
    raise ImportError("Neither openpyxl nor xlsxwriter is installed.")


def _column_letter(index: int) -> str:
    """Convert a 1-based column index to Excel column letters."""
    result = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def _excel_cell(value) -> tuple[str, str]:
    """Return Excel cell type and serialized value."""
    if pd.isna(value):
        return "inlineStr", ""
    if isinstance(value, (bool,)):
        return "b", "1" if value else "0"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "n", str(value)
    text = escape(str(value))
    return "inlineStr", text


def dataframe_to_excel_bytes_stdlib(dataframe: pd.DataFrame, sheet_name: str = "donnees") -> bytes:
    """Create a minimal .xlsx file without third-party Excel engines."""
    output = io.BytesIO()
    safe_sheet_name = escape((sheet_name or "donnees")[:31])

    sheet_rows: list[str] = []

    # Header row
    header_cells = []
    for col_idx, column in enumerate(dataframe.columns, start=1):
        cell_ref = f"{_column_letter(col_idx)}1"
        header_cells.append(
            f'<c r="{cell_ref}" t="inlineStr"><is><t>{escape(str(column))}</t></is></c>'
        )
    sheet_rows.append(f'<row r="1">{"".join(header_cells)}</row>')

    # Data rows
    for row_idx, row in enumerate(dataframe.itertuples(index=False, name=None), start=2):
        cells = []
        for col_idx, value in enumerate(row, start=1):
            cell_ref = f"{_column_letter(col_idx)}{row_idx}"
            cell_type, serialized = _excel_cell(value)
            if cell_type == "inlineStr":
                cells.append(
                    f'<c r="{cell_ref}" t="inlineStr"><is><t>{serialized}</t></is></c>'
                )
            else:
                cells.append(f'<c r="{cell_ref}" t="{cell_type}"><v>{serialized}</v></c>')
        sheet_rows.append(f'<row r="{row_idx}">{"".join(cells)}</row>')

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData>'
        "</worksheet>"
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheets><sheet name="{safe_sheet_name}" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )

    workbook_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
        "</Relationships>"
    )

    root_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="2"><fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        "</styleSheet>"
    )

    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        "</Types>"
    )

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml)
        archive.writestr("_rels/.rels", root_rels_xml)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        archive.writestr("xl/styles.xml", styles_xml)

    output.seek(0)
    return output.getvalue()


def dataframe_to_excel_bytes(dataframe: pd.DataFrame, sheet_name: str = "donnees") -> bytes:
    try:
        engine = get_excel_engine()
    except ImportError:
        return dataframe_to_excel_bytes_stdlib(dataframe, sheet_name)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine=engine) as writer:
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
        try:
            excel_bytes = dataframe_to_excel_bytes(dataframe, sheet_name)
            st.download_button(
                "Telecharger en Excel",
                data=excel_bytes,
                file_name=f"{base_filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except Exception as exc:
            logger.warning("Excel export unavailable for %s: %s", base_filename, exc)
            st.caption("Le format Excel est momentanement indisponible.")
