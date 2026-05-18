"""Reusable UI components for medical interface."""

import streamlit as st
from typing import Optional

def numeric_slider_input(
    label: str,
    key: str,
    min_value: float,
    max_value: float,
    step: float = 1.0,
    default: Optional[float] = None,
    unit: str = ""
) -> float:
    """Slider uniquement, sans manipulation manuelle du session_state."""

    col_slider, col_unit = st.columns([0.95, 0.05])

    with col_slider:
        value = st.slider(
            label,
            min_value=min_value,
            max_value=max_value,
            value=default if default is not None else min_value,
            step=step,
            key=key
        )

    with col_unit:
        if unit:
            st.caption(unit)

    return float(value)
    
def section_title(title: str, icon: str = "circle") -> None:
    """Display a section title with Font Awesome icon."""
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-icon">
                <i class="fas fa-{icon}"></i>
            </div>
            <h2>{title}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

def result_card(
    title: str,
    description: str,
    recommendation: str,
    risk_level: str = "low",
    icon: str = "check-circle"
) -> None:

    risk_classes = {
        "low": "result-low",
        "medium": "result-medium",
        "high": "result-high",
    }

    title_classes = {
        "low": "result-title-low",
        "medium": "result-title-medium",
        "high": "result-title-high",
    }

    risk_class = risk_classes.get(risk_level, "result-low")
    title_class = title_classes.get(risk_level, "result-title-low")

    # Carte vide (structure uniquement)
    st.markdown(
        f"""
        <div class="result-card {risk_class}">
            <div class="result-title {title_class}">
                <i class="fas fa-{icon}" style="font-size:20px;"></i>
                {title}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Contenu injecté PROPREMENT
    st.markdown(f"<div class='result-description'>{description}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-recommendation'>{recommendation}</div>", unsafe_allow_html=True)

def info_box(message: str, title: str = "Information", icon: str = "info-circle") -> None:
    """Display an information box."""
    st.markdown(
        f"""
        <div class="info-box">
            <div class="info-box-title">
                <i class="info-box-icon fas fa-{icon}"></i>
                <span>{title}</span>
            </div>
            <div>{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def confidence_badge(risk_level: str, percentage: float) -> None:
    """Display confidence level badge."""
    badge_classes = {
        "low": "badge-low",
        "medium": "badge-medium",
        "high": "badge-high",
    }
    
    badge_icons = {
        "low": "shield-alt",
        "medium": "exclamation-triangle",
        "high": "alert",
    }
    
    badge_labels = {
        "low": "Risque Faible",
        "medium": "Risque Modéré",
        "high": "Risque Élevé",
    }
    
    badge_class = badge_classes.get(risk_level, "badge-low")
    badge_icon = badge_icons.get(risk_level, "shield-alt")
    badge_label = badge_labels.get(risk_level, "Faible")
    
    st.markdown(
        f"""
        <div class="confidence-badge {badge_class}">
            <i class="fas fa-{badge_icon}"></i>
            {badge_label} ({percentage:.0%})
        </div>
        """,
        unsafe_allow_html=True,
    )


def form_section_title(title: str, icon: str = "clipboard") -> None:
    """Display a form section title with icon."""
    st.markdown(
        f"""
        <div class="form-section-title">
            <i class="form-section-icon fas fa-{icon}"></i>
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider() -> None:
    """Display a visual divider."""
    st.markdown("<hr style='margin: 24px 0; border: none; border-top: 1px solid #E5E9F0;'>", unsafe_allow_html=True)
