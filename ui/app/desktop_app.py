"""
Launch SV Debug Agent as a native desktop window (not a browser tab).

Uses pywebview + the local FastAPI server. Debugging logic stays in sv_debug/.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent.parent
DIST = APP_DIR / "frontend" / "dist"
HOST = "127.0.0.1"
PORT = 8765
URL = f"http://{HOST}:{PORT}"


def ensure_paths() -> None:
    os.chdir(APP_DIR)
    for path in (REPO_ROOT, APP_DIR):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))


def ensure_frontend_build() -> None:
    """Build the React UI once if dist/ is missing."""
    if (DIST / "index.html").exists():
        return

    frontend = APP_DIR / "frontend"
    if not frontend.exists():
        raise SystemExit("ui/app/frontend/ folder not found.")

    print("Building frontend (first run)...")
    npm = "npm.cmd" if sys.platform.startswith("win") else "npm"
    subprocess.run([npm, "install"], cwd=frontend, check=True)
    subprocess.run([npm, "run", "build"], cwd=frontend, check=True)

    if not (DIST / "index.html").exists():
        raise SystemExit("Frontend build failed — frontend/dist/index.html missing.")


def wait_for_server(timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{URL}/api/health", timeout=1) as res:
                if res.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.15)
    raise SystemExit(f"Server did not start at {URL}")


def run_server() -> None:
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=HOST,
        port=PORT,
        log_level="warning",
    )


def main() -> None:
    ensure_paths()
    ensure_frontend_build()

    server = threading.Thread(target=run_server, daemon=True)
    server.start()
    wait_for_server()

    try:
        import webview
    except ImportError as exc:
        raise SystemExit(
            "pywebview is required for the desktop app.\n"
            "Run: pip install pywebview"
        ) from exc

    webview.create_window(
        title="SV Debug Agent",
        url=URL,
        width=1280,
        height=860,
        min_size=(900, 640),
    )
    webview.start()


if __name__ == "__main__":
    main()
