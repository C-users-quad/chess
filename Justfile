# run vars
SRC_DIR := "src"
ENTRYPOINT_MODULE := "core.main"

# os specific vars
PYTHON := if os() == "windows" { VENV_DIR + "/Scripts/python" } \
		   else { VENV_DIR + "/bin/python" }
VENV_PIP := if os() == "windows" { VENV_DIR + "/Scripts/pip" } \
			else { VENV_DIR + "/bin/pip" }

# install vars
REQUIREMENTS_DIR := "requirements.txt"

# clean vars
PYCACHE_DIR := "__pycache__"

# venv vars
VENV_DIR := ".venv"

# pristine vars
PYTEST_CACHE_DIR := ".pytest_cache"
RUFF_CACHE_DIR := ".ruff_cache"

# test vars
TESTS_DIR := "tests"

# export pythonpath
export PYTHONPATH := SRC_DIR

help:
	@echo -e "\033[35mjust\033[0m Command Help:"
	@echo -e "    \033[36mvenv:\033[0m creates python virtual environment without dependencies"
	@echo -e "    \033[36minstall:\033[0m creates virtual environment with dependencies"
	@echo -e "    \033[36mrun:\033[0m runs the chess game"
	@echo -e "    \033[36mclean:\033[0m cleans all the cached bytecode"
	@echo -e "    \033[36mpristine:\033[0m cleans code cache, test cache, removes environment."
	@echo -e "    \033[36mtest:\033[0m run unit tests"
	@echo -e "    \033[36mlint:\033[0m lint source code"

venv:
	@echo Creating virtual environment
	python -m venv {{VENV_DIR}}

lint:
	@echo Cleaning up code...
	ruff format {{SRC_DIR}} -v

install: venv
	@echo Installing dependencies...
	{{VENV_PIP}} install -r {{REQUIREMENTS_DIR}}

run:
	@echo Running Chess Game...
	{{PYTHON}} -m {{ENTRYPOINT_MODULE}}

clean:
	@echo Clearing cache...
	{{PYTHON}} -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"

pristine: clean
	@echo Making pristine...
	{{PYTHON}} -c "import shutil; shutil.rmtree('{{VENV_DIR}}', ignore_errors=True); shutil.rmtree('{{PYTEST_CACHE_DIR}}', ignore_errors=True); shutil.rmtree('{{RUFF_CACHE_DIR}}', ignore_errors=True)"

test:
	@echo Running unit tests with pytest...
	{{PYTHON}} -m pytest {{TESTS_DIR}} -v
