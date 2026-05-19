"""Professional medical theme for Heart Disease Prediction application.
Modern, ergonomic, health-oriented CSS styling with Font Awesome icons.
"""

import streamlit as st


def inject_medical_theme() -> None:
    """Inject modern health-oriented medical theme with Font Awesome icons and ergonomic styling."""
    
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
        /* Force full width */
        .main .block-container {
            max-width: 1400px !important;
            width: 100% !important;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        
        /* Force sidebar color */
        [data-testid="stSidebar"] {
            background-color: #0F172A !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background-color: #0F172A !important;
        }
        
        /* Force button text visibility */
        .stButton > button {
            color: #FFFFFF !important;
        }

        /* Make sidebar 'Se deconnecter' (secondary) text readable (no white-on-white issues) */
        [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
            background: transparent !important;
            border: 1px solid rgba(239, 68, 68, 0.8) !important;
            color: #EF4444 !important;
        }

        [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
            background: rgba(239, 68, 68, 0.08) !important;
            border-color: #EF4444 !important;
            color: #EF4444 !important;
        }

        
        .stButton > button[kind="secondary"] {
            color: #2563EB !important;
        }
        
        /* ==================== MODERN HEALTH COLOR PALETTE ==================== */
        :root {
            --color-primary: #2563EB;
            --color-primary-dark: #1E40AF;
            --color-primary-light: #3B82F6;
            --color-sidebar: #0F172A;
            --color-sidebar-gradient: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
            --color-bg: #F8FAFC;
            --color-bg-gradient: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
            --color-accent-heart: #EF4444;
            --color-accent-heart-light: #FCA5A5;
            --color-health-green: #10B981;
            --color-health-teal: #14B8A6;
            --color-risk-low: #059669;
            --color-risk-medium: #F59E0B;
            --color-risk-high: #DC2626;
            --color-white: #FFFFFF;
            --color-text: #1E293B;
            --color-text-secondary: #475569;
            --color-text-muted: #94A3B8;
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --radius-xl: 24px;
        }
        
        /* ==================== GLOBAL STYLES ==================== */
        .stApp {
            background: var(--color-bg-gradient);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .main {
            max-width: 1400px !important;
            width: 100% !important;
            margin: 0 auto !important;
            padding: 2rem 1rem !important;
        }
        
        .main .block-container {
            max-width: 1400px !important;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-weight: 600;
            color: var(--color-text);
        }
        
        /* ==================== SIDEBAR ==================== */
        [data-testid="stSidebar"] {
            background: var(--color-sidebar-gradient);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background: transparent;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: var(--color-white);
        }
        
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown span,
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: var(--color-white);
        }
        
        [data-testid="stSidebar"] a {
            color: rgba(255, 255, 255, 0.85);
            transition: all 0.2s ease;
            border-radius: var(--radius-md);
            padding: 0.5rem 0.75rem;
            display: block;
        }
        
        [data-testid="stSidebar"] a:hover {
            color: var(--color-white);
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(4px);
        }
        
        [data-testid="stSidebar"] button {
            background: var(--color-primary);
            color: var(--color-white);
            border: none;
            border-radius: var(--radius-md);
            padding: 0.75rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        [data-testid="stSidebar"] button:hover {
            background: var(--color-primary-dark);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        /* ==================== BUTTONS ==================== */
        .stButton > button {
            height: 48px;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 14px;
            border: none;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
            letter-spacing: 0.5px;
            color: var(--color-white) !important;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: var(--color-white) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
            color: var(--color-white) !important;
        }
        
        .stButton > button[kind="secondary"] {
            background: var(--color-white);
            color: var(--color-primary) !important;
            border: 2px solid var(--color-primary);
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(37, 99, 235, 0.05);
            border-color: var(--color-primary-dark);
            color: var(--color-primary-dark) !important;
        }
        
        .stButton > button:disabled {
            background: #E2E8F0 !important;
            color: #94A3B8 !important;
            cursor: not-allowed;
        }
        
        /* ==================== INPUTS & FORMS ==================== */
        /* Tous les textes et valeurs en noir pour meilleure lisibilité */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            height: 48px;
            border-radius: var(--radius-md);
            border: 2px solid #E2E8F0;
            font-size: 14px;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            transition: all 0.2s ease;
            background: var(--color-white) !important;
            color: #1E293B !important;
            -webkit-text-fill-color: #1E293B !important;
            padding: 0.75rem 1rem;
        }

        /* Placeholder text en gris clair pour contraste */
        .stTextInput > div > div > input::placeholder,
        .stNumberInput > div > div > input::placeholder {
            color: #94A3B8 !important;
            -webkit-text-fill-color: #94A3B8 !important;
        }

        /* BaseWeb selectbox - force texte noir (état fermé & ouvert) */
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [role="combobox"],
        .stSelectbox [data-baseweb="select"] span,
        .stSelectbox [data-baseweb="select"] div,
        .stSelectbox [data-baseweb="select"] p,
        .stSelectbox [data-baseweb="select"] label,
        .stSelectbox [role="combobox"] span,
        .stSelectbox [role="combobox"] div {
            color: #1E293B !important;
            -webkit-text-fill-color: #1E293B !important;
            background: #FFFFFF !important;
        }

        /* Zone d'affichage de la valeur (baseweb) */
        .stSelectbox [data-baseweb="select"] [data-testid="stSelectbox"] {
            color: #1E293B !important;
            background: #FFFFFF !important;
        }

        /* Select HTML - fond blanc, texte noir (fallback) */
        .stSelectbox > div > div > select,
        .stSelectbox select {
            background: var(--color-white) !important;
            border: 2px solid #E2E8F0;
            color: #1E293B !important;
            -webkit-text-fill-color: #1E293B !important;
            height: 48px;
            border-radius: var(--radius-md);
            font-size: 14px;
            padding: 0.75rem 1rem;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }


        /* Options du select - fond blanc, texte noir */
        .stSelectbox > div > div > select option {
            background: var(--color-white) !important;
            color: #1E293B !important;
            -webkit-text-fill-color: #1E293B !important;
        }

        /* Options sélectionnées */
        .stSelectbox > div > div > select option:checked {
            background: rgba(37, 99, 235, 0.15) !important;
            color: #1E293B !important;
        }

        /* Dropdown listbox BaseWeb */
        .stSelectbox [role="listbox"] {
            background: var(--color-white) !important;
        }
        .stSelectbox [role="listbox"] div,
        .stSelectbox [role="listbox"] span {
            color: #1E293B !important;
            -webkit-text-fill-color: #1E293B !important;
        }

        /* Focus state */
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: var(--color-primary);
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
            outline: none;
            color: #1E293B !important;
            -webkit-text-fill-color: #1E293B !important;
        }
        
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, var(--color-health-green), var(--color-health-teal), var(--color-accent-heart));
            border-radius: var(--radius-sm);
        }
        
        .stSlider [role="slider"] {
            background: var(--color-primary);
            border: 3px solid var(--color-white);
            box-shadow: var(--shadow-md);
        }
        
        /* ==================== CARDS & CONTAINERS ==================== */
        .card {
            background: var(--color-white);
            border-radius: var(--radius-lg);
            padding: 24px;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(226, 232, 240, 0.8);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
            border-color: var(--color-primary-light);
        }
        
        /* ==================== RESULT CARDS ==================== */
        .result-card {
            border-radius: var(--radius-lg);
            padding: 32px;
            margin: 24px 0;
            box-shadow: var(--shadow-lg);
            border-left: 6px solid;
            background: var(--color-white);
            transition: all 0.3s ease;
        }
        
        .result-card:hover {
            box-shadow: var(--shadow-xl);
            transform: translateY(-2px);
        }
        
        .result-low {
            background: linear-gradient(135deg, rgba(5, 150, 105, 0.08) 0%, rgba(5, 150, 105, 0.02) 100%);
            border-left-color: var(--color-risk-low);
            border: 1px solid rgba(5, 150, 105, 0.2);
        }
        
        .result-medium {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(245, 158, 11, 0.02) 100%);
            border-left-color: var(--color-risk-medium);
            border: 1px solid rgba(245, 158, 11, 0.2);
        }
        
        .result-high {
            background: linear-gradient(135deg, rgba(220, 38, 38, 0.08) 0%, rgba(220, 38, 38, 0.02) 100%);
            border-left-color: var(--color-risk-high);
            border: 1px solid rgba(220, 38, 38, 0.2);
        }
        
        .result-title {
            font-size: 24px;
            font-weight: 700;
            margin: 0 0 16px 0;
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .result-title-low { color: var(--color-risk-low); }
        .result-title-medium { color: var(--color-risk-medium); }
        .result-title-high { color: var(--color-risk-high); }
        
        .result-description {
            font-size: 16px;
            font-weight: 500;
            margin: 16px 0;
            color: var(--color-text);
            line-height: 1.6;
        }
        
        .result-recommendation {
            font-size: 15px;
            margin: 16px 0 0 0;
            line-height: 1.7;
            color: var(--color-text-secondary);
            background: rgba(255, 255, 255, 0.5);
            padding: 16px;
            border-radius: var(--radius-md);
        }
        
        .result-recommendation strong {
            color: var(--color-text);
            font-weight: 600;
        }
        
        /* ==================== METRIC CARDS ==================== */
        .metric-card {
            background: var(--color-white);
            border-radius: var(--radius-lg);
            padding: 24px;
            text-align: center;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(226, 232, 240, 0.8);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: var(--color-primary);
            margin: 12px 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .metric-label {
            font-size: 13px;
            color: var(--color-text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        
        /* ==================== SECTION HEADERS ==================== */
        .section-header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin: 32px 0 20px 0;
            padding-bottom: 16px;
            border-bottom: 3px solid var(--color-primary);
        }
        
        .section-header h2 {
            margin: 0;
            font-size: 22px;
            font-weight: 700;
            color: var(--color-text);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .section-icon {
            font-size: 28px;
            color: var(--color-primary);
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(37, 99, 235, 0.1);
            border-radius: var(--radius-md);
        }
        
        /* ==================== CONFIDENCE BADGE ==================== */
        .confidence-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 12px 24px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 15px;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }
        
        .confidence-badge:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow-md);
        }
        
        .badge-low {
            background: linear-gradient(135deg, rgba(5, 150, 105, 0.15) 0%, rgba(5, 150, 105, 0.08) 100%);
            color: var(--color-risk-low);
            border: 1px solid rgba(5, 150, 105, 0.3);
        }
        
        .badge-medium {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
            color: var(--color-risk-medium);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        
        .badge-high {
            background: linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(220, 38, 38, 0.08) 100%);
            color: var(--color-risk-high);
            border: 1px solid rgba(220, 38, 38, 0.3);
        }
        
        /* ==================== FORM SECTIONS ==================== */
        .form-section {
            background: var(--color-white);
            border-radius: var(--radius-lg);
            padding: 28px;
            margin: 20px 0;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(226, 232, 240, 0.8);
            transition: all 0.3s ease;
        }
        
        .form-section:hover {
            box-shadow: var(--shadow-lg);
            border-color: var(--color-primary-light);
        }
        
        .form-section-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--color-text);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .form-section-icon {
            font-size: 20px;
            color: var(--color-primary);
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(37, 99, 235, 0.1);
            border-radius: var(--radius-md);
        }
        
        /* ==================== INFO BOX ==================== */
        .info-box {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(37, 99, 235, 0.03) 100%);
            border: 1px solid rgba(37, 99, 235, 0.2);
            border-radius: var(--radius-md);
            padding: 20px;
            margin: 20px 0;
            color: var(--color-text);
            border-left: 4px solid var(--color-primary);
            box-shadow: var(--shadow-sm);
        }
        
        .info-box-title {
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .info-box-icon {
            font-size: 20px;
            color: var(--color-primary);
        }
        
        /* ==================== DATAFRAME STYLING ==================== */
        .stDataFrame {
            box-shadow: var(--shadow-md);
            border-radius: var(--radius-lg);
            overflow: hidden;
            border: 1px solid rgba(226, 232, 240, 0.8);
        }
        
        .stDataFrame [role="grid"] {
            border-radius: var(--radius-lg);
        }
        
        .stDataFrame th {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: var(--color-white);
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stDataFrame td {
            font-size: 14px;
            color: var(--color-text);
        }
        
        /* ==================== EXPANDER ==================== */
        .stExpander {
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(226, 232, 240, 0.8);
            background: var(--color-white);
        }
        
        .stExpander > div > div > div > div {
            background: var(--color-white);
        }
        
        /* ==================== TABS ==================== */
        .stTabs [role="tablist"] {
            border-bottom: 2px solid rgba(226, 232, 240, 0.8);
            gap: 8px;
        }
        
        .stTabs [role="tab"] {
            background: var(--color-white);
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: var(--radius-md) var(--radius-md) 0 0;
            padding: 12px 24px;
            font-weight: 500;
            color: var(--color-text-secondary);
            transition: all 0.2s ease;
        }
        
        .stTabs [role="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: var(--color-white);
            border-color: var(--color-primary);
            box-shadow: var(--shadow-sm);
        }
        
        .stTabs [role="tab"]:hover:not([aria-selected="true"]) {
            background: rgba(37, 99, 235, 0.05);
            color: var(--color-primary);
        }
        
        /* ==================== METRICS ==================== */
        [data-testid="stMetricValue"] {
            font-size: 32px;
            font-weight: 700;
            color: var(--color-primary);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 13px;
            color: var(--color-text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        
        /* ==================== SUCCESS/INFO/WARNING/ERROR ==================== */
        .stSuccess {
            background: linear-gradient(135deg, rgba(5, 150, 105, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
            border: 1px solid rgba(5, 150, 105, 0.3);
            border-radius: var(--radius-md);
            padding: 16px;
        }
        
        .stInfo {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(37, 99, 235, 0.05) 100%);
            border: 1px solid rgba(37, 99, 235, 0.3);
            border-radius: var(--radius-md);
            padding: 16px;
        }
        
        .stWarning {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: var(--radius-md);
            padding: 16px;
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
            border: 1px solid rgba(220, 38, 38, 0.3);
            border-radius: var(--radius-md);
            padding: 16px;
        }
        
        /* ==================== RESPONSIVE ==================== */
        @media (max-width: 768px) {
            .main {
                padding: 1rem 0.5rem;
            }
            
            .result-card {
                padding: 20px;
                margin: 16px 0;
            }
            
            .result-title {
                font-size: 20px;
            }
            
            .metric-card {
                padding: 16px;
            }
            
            .metric-value {
                font-size: 24px;
            }
            
            .form-section {
                padding: 20px;
            }
            
            .section-header {
                margin: 24px 0 16px 0;
            }
            
            .section-header h2 {
                font-size: 18px;
            }
        }
        
        @media (max-width: 480px) {
            .result-card {
                padding: 16px;
            }
            
            .result-title {
                font-size: 18px;
            }
            
            .metric-value {
                font-size: 20px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
