import os
import sys

import pytest


# Ensure the repository root is importable so `import app...` works in tests.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


@pytest.fixture(name="patcher")
def patcher_fixture():
    """Fixture providing safe attribute patching with automatic cleanup."""

    patcher_obj = pytest.MonkeyPatch()
    yield patcher_obj
    patcher_obj.undo()

