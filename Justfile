# venv vars
VENV_DIR := ".venv"

# run vars
SRC_DIR := "src"
ENTRYPOINT_MODULE := "core.main"

# os specific vars
SYSTEM_PYTHON := if os() == "windows" { "python" } else { "python3" }
PYTHON := if os() == "windows" { VENV_DIR + "/Scripts/python" } \
           else { VENV_DIR + "/bin/python" }
VENV_PIP := if os() == "windows" { VENV_DIR + "/Scripts/pip" } \
             else { VENV_DIR + "/bin/pip" }

# install vars
REQUIREMENTS_DIR := "requirements.txt"

# pristine vars
PYTEST_CACHE_DIR := ".pytest_cache"
RUFF_CACHE_DIR := ".ruff_cache"

# test vars
TESTS_DIR := "tests"

# export pythonpath
export PYTHONPATH := SRC_DIR

# export vars
EXPORT_NAME := "chess"
ASSETS_DIR := "assets"
PYINSTALLER := if os() == "windows" { VENV_DIR + "/Scripts/pyinstaller" } \
               else { VENV_DIR + "/bin/pyinstaller" }
DATA_SEP := if os() == "windows" { ";" } else { ":" }

help:
	@{{SYSTEM_PYTHON}} -c " \
		print('\033[35mjust\033[0m Command Help:'); \
		print('    \033[36mvenv:\033[0m creates python virtual environment without dependencies'); \
		print('    \033[36minstall:\033[0m creates virtual environment with dependencies'); \
		print('    \033[36mrun:\033[0m runs the chess game'); \
		print('    \033[36mclean:\033[0m cleans all the cached bytecode'); \
		print('    \033[36mpristine:\033[0m cleans code cache, test cache, removes environment.'); \
		print('    \033[36mtest:\033[0m run unit tests'); \
		print('    \033[36mlint:\033[0m lint source code'); \
		print('    \033[36mexport:\033[0m builds a standalone executable with 		PyInstaller'); \

	"

export: install
	@{{SYSTEM_PYTHON}} -c "print('Building executable with PyInstaller...')"
	{{PYINSTALLER}} --onefile --windowed \
		--name {{EXPORT_NAME}} \
		--paths {{SRC_DIR}} \
		--add-data "{{ASSETS_DIR}}{{DATA_SEP}}{{ASSETS_DIR}}" \
		{{SRC_DIR}}/core/main.py

venv:
	@{{SYSTEM_PYTHON}} -c "print('Creating virtual environment...')"
	{{SYSTEM_PYTHON}} -m venv {{VENV_DIR}}

lint:
	@{{SYSTEM_PYTHON}} -c "print('Linting code...')"
	ruff format {{SRC_DIR}} -v

install: venv
	@{{SYSTEM_PYTHON}} -c "print('Installing dependencies...')"
	{{VENV_PIP}} install -r {{REQUIREMENTS_DIR}}

run:
	@{{SYSTEM_PYTHON}} -c "print('Running Chess Game...')"
	{{PYTHON}} -m {{ENTRYPOINT_MODULE}}

clean:
	@{{SYSTEM_PYTHON}} -c "print('Clearing cache...')"
	{{PYTHON}} -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"

pristine: clean
	@{{SYSTEM_PYTHON}} -c "print('Making pristine...')"
	{{PYTHON}} -c "import shutil; shutil.rmtree('{{VENV_DIR}}', ignore_errors=True); shutil.rmtree('{{PYTEST_CACHE_DIR}}', ignore_errors=True); shutil.rmtree('{{RUFF_CACHE_DIR}}', ignore_errors=True)"

test:
	@{{SYSTEM_PYTHON}} -c "print('Running unit tests with pytest...')"
	{{PYTHON}} -m pytest {{TESTS_DIR}} -v
