# run vars
SRC_DIR = src
PYTHON = python3
ENTRYPOINT_MODULE = core.main

# install vars
REQUIREMENTS_DIR = requirements.txt
PIP = pip3

# venv vars
VENV_DIR = .venv

# pristine vars
PYTEST_CACHE_DIR = .pytest_cache

# test vars
TESTS_DIR = tests

.PHONY: help
help:
	@echo -e "\033[35mmake\033[0m Command Help:"
	@echo -e "    \033[36mvenv:\033[0m creates python virtual environment without dependencies"
	@echo -e "    \033[36minstall:\033[0m creates virtual environment with dependencies"
	@echo -e "    \033[36mrun:\033[0m runs the chess game"
	@echo -e "    \033[36mclean:\033[0m cleans all the cached bytecode"
	@echo -e "    \033[36mpristine:\033[0m cleans code cache, test cache, removes environment."
	@echo -e "    \033[36mtest:\033[0m run unit tests"

.PHONY: venv
venv:
	@echo Creating virtual environment
	$(PYTHON) -m venv $(VENV_DIR)

.PHONY: install
install: venv
	@echo Installing dependencies...
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS_DIR)

.PHONY: run
run:
	@echo Running Chess Game...
	PYTHONPATH=$(SRC_DIR) $(PYTHON) -m $(ENTRYPOINT_MODULE)

.PHONY: clean
clean:
	@echo Deleting cache...
	find $(SRC_DIR) -type d -name "__pycache__" -exec rm -rf {} +
	find $(TESTS_DIR) -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: pristine
pristine: clean
	@echo Making build pristine...
	find . -type d -name $(VENV_DIR) -exec rm -rf {} +
	find . -type d -name $(PYTEST_CACHE_DIR) -exec rm -rf {} +

.PHONY: test
test:
	@echo Running unit tests with pytest...
	PYTHONPATH=$(SRC_DIR) $(PYTHON) -m pytest $(TESTS_DIR) -v
