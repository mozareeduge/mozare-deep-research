.PHONY: install test audit compile check schemas templates wheel package

install:
	python -m pip install -e .

test:
	python -m pytest

audit:
	python -m mros audit . --release

compile:
	python -m mros compile-method .

schemas:
	python scripts/export_schemas.py

templates:
	python scripts/sync_templates.py

wheel:
	python -m pip wheel . --no-deps -w dist

check:
	python scripts/export_schemas.py --check
	python scripts/sync_templates.py --check
	python -m compileall -q src tests scripts
	python -m pytest
	python -m mros verify .
	python -m mros audit . --release

package:
	python scripts/package_repo.py
