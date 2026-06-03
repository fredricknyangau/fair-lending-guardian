"""CrewAI environment setup for local writable storage."""

import os
from pathlib import Path


def _push_streamlit_secrets() -> None:
    """Copy Streamlit secrets into os.environ so LiteLLM and dotenv see them.

    When running under Streamlit, secrets.toml is the authoritative source.
    When running via CLI (python main.py), this is a no-op — os.environ is
    already populated by python-dotenv in agents.py.
    """
    try:
        import streamlit as st  # noqa: PLC0415 — intentional lazy import

        for key, value in st.secrets.items():
            if isinstance(value, str):
                os.environ[key] = value
    except Exception:  # noqa: BLE001 — not running under Streamlit, skip silently
        pass


def configure_crewai_environment() -> None:
    project_root = Path(__file__).resolve().parent
    crewai_home = project_root / ".crewai-home"

    # Push secrets.toml values into os.environ FIRST so they win over .env
    _push_streamlit_secrets()

    os.environ["HOME"] = str(crewai_home)
    os.environ.setdefault("XDG_DATA_HOME", str(project_root / ".crewai-data"))
    os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
    os.environ.setdefault("CREWAI_DISABLE_TRACKING", "true")

