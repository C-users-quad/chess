# run vars
SRC_DIR = src
ENTRYPOINT_MODULE = core.main

# detect OS
ifeq ($(OS),Windows_NT)
	PYTHON = python
	VENV_PIP = $(VENV_DIR)/Scripts/pip
else
	PYTHON = python3
	VENV_PIP = $(VENV_DIR)/bin/pip
endif
	
# install vars
REQUIREMENTS_DIR = requirements.txt

# clean vars
PYCACHE_DIR = __pycache__

# venv vars
VENV_DIR = .venv

# pristine vars
PYTEST_CACHE_DIR = .pytest_cache
RUFF_CACHE_DIR = .ruff_cache

# test vars
TESTS_DIR = tests

# export pythonpath
export PYTHONPATH := $(SRC_DIR)

.PHONY: help
help:
	@echo -e "\033[35mmake\033[0m Command Help:"
	@echo -e "    \033[36mvenv:\033[0m creates python virtual environment without dependencies"
	@echo -e "    \033[36minstall:\033[0m creates virtual environment with dependencies"
	@echo -e "    \033[36mrun:\033[0m runs the chess game"
	@echo -e "    \033[36mclean:\033[0m cleans all the cached bytecode"
	@echo -e "    \033[36mpristine:\033[0m cleans code cache, test cache, removes environment."
	@echo -e "    \033[36mtest:\033[0m run unit tests"
	@echo -e "    \033[36mlint:\033[0m lint source code"

.PHONY: venv
venv:
	@echo Creating virtual environment
	$(PYTHON) -m venv $(VENV_DIR)

.PHONY: lint
lint:
	@echo Cleaning up code...
	ruff format $(SRC_DIR) -v

.PHONY: install
install: venv
	@echo Installing dependencies...
	$(VENV_PIP) install -r $(REQUIREMENTS_DIR)

.PHONY: run
run:
	@echo Running Chess Game...
	$(PYTHON) -m $(ENTRYPOINT_MODULE)

.PHONY: clean
clean:
	@echo Deleting cache...
	find . -type d -name $(PYCACHE_DIR) -exec rm -rfv {} +

.PHONY: pristine
pristine: clean
	@echo Making build pristine...
	find . -type d -name $(VENV_DIR) -exec rm -rfv {} +
	find . -type d -name $(PYTEST_CACHE_DIR) -exec rm -rfv {} +
	find . -type d -name $(RUFF_CACHE_DIR) -exec rm -rfv {} +

.PHONY: test
test:
	@echo Running unit tests with pytest...
	$(PYTHON) -m pytest $(TESTS_DIR) -v
