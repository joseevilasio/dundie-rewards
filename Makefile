# Makefile
.PHONY: install virtualenv ipython clean test watch


install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e '.[dev]'

virtualenv:
	@.venv/bin/python -m pip -m venv .venv

test:
	@.venv/bin/pytest --v -s

watch:
	# @.venv/bin/ptw
	@ls **/*.py | entr pytest

ipython:
	@.venv/bin/ipython

lint:
	@.venv/bin/pflake8

clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
