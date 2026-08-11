"""Shim — the one-file legacy app lives at the repo root as ``legacy.py``."""

from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parents[2] / "legacy.py"), run_name="__main__")
