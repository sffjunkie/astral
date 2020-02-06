.PHONY: clean test test_docs test_all html report docs repl

all: clean test report html

BUILDDIR=$(DEV_HOME)/build/astral/master

clean:
	@COVERAGE_FILE=$(BUILDDIR)/.coverage coverage erase

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
	sphinx-build -W -b html -d $(BUILDDIR)/doctrees ./src/doc ./doc

repl:
	@PYTHONPATH=src winpty python

