.PHONY: clean test test-docs test-all html report build-docs repl show-docs show-cov typecheck

all: clean test report html

BUILDDIR=$(DEV_HOME)/build/astral

clean:
	@COVERAGE_FILE=$(BUILDDIR)/.coverage coverage erase
	@rm -rf $(BUILDDIR)/doctrees

test:
	tox

test-docs:
	tox -e doc

test-all:
	tox -e py36,py37,nopytz,doc

html:
	@COVERAGE_FILE=$(BUILDDIR)/.coverage coverage html -d $(BUILDDIR)/htmlcov/

report:
	@COVERAGE_FILE=$(BUILDDIR)/.coverage coverage report

build-docs:
	sphinx-build -a -b html -d $(BUILDDIR)/doctrees ./src/docs ./docs

repl:
	@PYTHONPATH=src winpty python

show-docs:
	/usr/bin/start ./doc/index.html

publish-docs:
	git subtree push --prefix docs origin gh-pages

show-cov:
	/usr/bin/start $(BUILDDIR)/htmlcov/index.html

typecheck:
	@cd src
	mypy astral
	@cd ..
