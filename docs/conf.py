# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Holiday Homes"
copyright = "2023, Orange County Lettings"
author = "Orange County Lettings"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Ajout de support pour Mermaid (diagrammes UML)
html_js_files = [
    "https://cdn.jsdelivr.net/npm/mermaid@8.13.3/dist/mermaid.min.js",
]


def setup(app):
    app.add_js_file("custom.js")


# Créer un fichier JavaScript personnalisé pour initialiser Mermaid
os.makedirs("_static", exist_ok=True)
with open("_static/custom.js", "w") as f:
    f.write(
        """
document.addEventListener('DOMContentLoaded', function() {
    mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        flowchart: { useMaxWidth: true, htmlLabels: true },
    });
});
"""
    )

# -- Extension configuration -------------------------------------------------
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "undoc-members": True,
}

# Seulement initialiser Django si nous ne sommes pas sur Read the Docs
on_rtd = os.environ.get("READTHEDOCS", None) == "True"
if not on_rtd:
    # Ajouter le répertoire parent au chemin Python pour les imports
    sys.path.insert(0, os.path.abspath(".."))

    # Setup Django uniquement en local, pas sur ReadTheDocs
    os.environ["DJANGO_SETTINGS_MODULE"] = "oc_lettings_site.settings"
    import django

    django.setup()
