"""CrewAI environment setup for local writable storage."""

import os
from pathlib import Path


def configure_crewai_environment() -> None:
    project_root = Path(__file__).resolve().parent
    crewai_home = project_root / ".crewai-home"

    os.environ["HOME"] = str(crewai_home)
    os.environ.setdefault("XDG_DATA_HOME", str(project_root / ".crewai-data"))
    os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
    os.environ.setdefault("CREWAI_DISABLE_TRACKING", "true")
