# Justfile for Python projects using mypy, pdm, pytest, ruff, tox
pypm := 'pdm'
project := 'astral'

home_dir := env_var('HOME')
dev_home := env_var_or_default("DEVELOPMENT_HOME", home_dir + "/development")
cache_dir := dev_home + '/cache/' + project

default:
    just --list

# Lint the source
lint:
    #!/bin/sh
    if command -v ruff &>/dev/null; then
        ruff check --config "cache-dir = '{{cache_dir}}/ruff'" src/{{project}}
    else
        pdm run ruff check --config "cache-dir = '{{cache_dir}}/ruff'" src/{{project}}
    fi
    if [ $? -eq 0 ]; then
        echo "ruff: no problems found"
    fi

# Run tox to test unit and integration tests
test:
    {{pypm}} run tox --workdir {{cache_dir}}/tox

# Ron tox to test documentation generation
test-docs:
    {{pypm}} run tox --workdir {{cache_dir}}/tox -e doc

# Run the type checker (mypy)
test-types:
    {{pypm}} run mypy --cache-dir={{cache_dir}}/mypy ./src/{{project}}

export COVERAGE_FILE := cache_dir + '/coverage'
# Generate test coverage metrics
test-coverage:
    {{pypm}} run pytest -o cache_dir={{cache_dir}}/pytest --cov=src/{{project}} src/test

# Generate test coverage HTML report
test-coverage-html:
    {{pypm}} run coverage html -d {{cache_dir}}/htmlcov/
    @xdg-open "{{cache_dir}}/htmlcov/index.html" 2>&1 >/dev/null

# Show test coverage in the terminal
test-coverage-term:
    {{pypm}} run coverage report

# Build documentation
docs-build:
    {{pypm}} run sphinx-build -a -b html -d {{cache_dir}}/doctrees ./src/docs ../gh-pages

# View built documentation
docs-view:
    @xdg-open ../gh-pages/index.html 2>&1 >/dev/null

# Run a python repl
repl:
    @{{pypm}} run python
