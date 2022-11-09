# -*- coding: utf-8 -*-
import os
import sys

on_rtd = os.environ.get("READTHEDOCS", None) == "True"

project = "Astral"
author = "Simon Kennedy"
copyright = "2009-2022, %s" % author
version = "3.2"
release = "3.2"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
]

intersphinx_mapping = {
    "python": ("http://docs.python.org/3", "python3_intersphinx.inv")
}

# Add parent directory so autodoc can find the source code
sys.path.insert(0, os.path.join(os.path.abspath("..")))

source_suffix = ".rst"
master_doc = "index"

pygments_style = "sphinx"

templates_path = ["templates"]
# endregion

if not on_rtd:
    html_theme = "sphinx_book_theme"
else:
    html_theme = "basic"
html_logo = os.path.join("static", "earth_sun.png")

if not on_rtd:
    html_favicon = os.path.join("static", "weather-sunny.png")

html_static_path = ["static"]

html_css_files = [
    "astral.css",
]

html_domain_indices = False
