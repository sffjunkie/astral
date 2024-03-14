home_dir := env_var('HOME')
dev_home := env_var_or_default("DEVELOPMENT_HOME", "{{home_dir}}/development")
build_dir := dev_home + '/build/astral'
pypm := 'pdm'

test:
    {{pypm}} run tox

test-docs:
    {{pypm}} run tox -e doc

test-types:
    {{pypm}} run mypy ./src/astral

export COVERAGE_FILE := build_dir + '/coverage'
test-coverage:
    {{pypm}} run pytest --cov=src/astral src/test

test-coverage-html:
    {{pypm}} run coverage html -d "{{build_dir}}/htmlcov/"
    @xdg-open "{{build_dir}}/htmlcov/index.html" 2>&1 >/dev/null

test-coverage-term:
    {{pypm}} run coverage report
    @xdg-open "{{build_dir}}/htmlcov/index.html" 2>&1 >/dev/null

build-docs:
    {{pypm}} run sphinx-build -a -b html -d {{build_dir}}/doctrees ./src/docs ../gh-pages

view-docs:
    @xdg-open ../gh-pages/index.html 2>&1 >/dev/null

publish-docs:
	git subtree push --prefix docs origin gh-pages

repl:
    @{{pypm}} run python
