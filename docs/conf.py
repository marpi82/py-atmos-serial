"""Sphinx configuration for py-atmos-serial."""

from __future__ import annotations

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath("../src"))

project = "py-atmos-serial"
author = "MarPi82"
copyright = f"{datetime.now():%Y}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]
source_suffix = {".rst": "restructuredtext"}
exclude_patterns = ["_build"]
napoleon_google_docstring = True
napoleon_numpy_docstring = False
html_theme = "furo"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
