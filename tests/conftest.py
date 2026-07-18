from __future__ import annotations

from pathlib import Path

import pytest

from mros.project import init_project


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    init_project(root, "test-project", "Test Project")
    return root
