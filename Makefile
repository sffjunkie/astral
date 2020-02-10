.PHONY: clean test test_docs test_all html report docs repl show_docs show_cov typecheck

all: clean test report html

BUILDDIR=$(DEV_HOME)/build/astral

clean:
	@COVERAGE_FILE=$(BUILDDIR)/.coverage coverage erase
	@rm -rf $(BUILDDIR)/doctrees

test:
	tox

test_docs:
	tox -e doc

test_all:
	tox -e py36,py37,nopytz,doc

html:
	@COVERAGE_FILE=$(BUILDDIR)/.coverage coverage html -d $(BUILDDIR)/htmlcov/

report:
	@COVERAGE_FILE=$(BUILDDIR)/.coverage coverage report

docs:
	sphinx-build -a -W -b html -d $(BUILDDIR)/doctrees ./src/doc ./doc

repl:
	@PYTHONPATH=src winpty python

show_docs:
	/usr/bin/start ./doc/index.html

show_cov:
	/usr/bin/start $(BUILDDIR)/htmlcov/index.html

typecheck:
	@cd src
	mypy astral
	@cd ..
