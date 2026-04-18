"""Root conftest: activate PDK for any pytest run.

Covers both this project's tests under tests/ and the gdsfactoryplus
`gfp test` runner, which invokes pytest against a file inside .venv.
pytest walks rootdir → test_file, so a root conftest applies to both.
"""

import pytest

from gf180mcu import PDK


@pytest.fixture(autouse=True)
def activate_pdk() -> None:
    """Activate PDK for every test."""
    PDK.activate()
