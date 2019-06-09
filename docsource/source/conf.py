"""
Sphinx config.py
===========================================

.. module:: conf.py

:Synopsis: Sphinx config file.

:Description:
    This is an early version of a Sphinx RTD theme boilerplate `config.py` file.
    Future versions will be better organized and will, eventually, be
    configurable from yaml.

    Reasons for this `config.py` structure:

        * enforce precedence
        * compartmentalized configuration topics
        * increase maintainability
        * preparation for implementing dynamic variable instantiation:

            * configuration will move to yaml format
            * Sphinx API will be used to manage configuration entities

:Platform: Unix, Windows, |python_version|

:Dependencies:

    .. literalinclude:: ../../requirements.txt
        :language: text

:License:
    :download:`Sphinx RTD Theme Project Owner: MIT <https://github.com/rtfd/sphinx_rtd_theme/blob/master/LICENSE>`

    :download:`RTD Boilerplate: `MIT <../../LICENSE>`

    :download:`EditFrontMatter: `MIT <../../LICENSE>`

.. :moduleauthor: `Karl N. Redman <https://karlredman.github.io>`_

:Module Author: |author|

:homepage:

    `Sphinx RTD Boilerplate <https://karlredman.github.io/spinx-rtd-boilerplate>`_

    `EditFrontMatter <https://karlredman.github.io/EditFrontMatter>`_

:Current Release:
    version: |release|

.. versionadded:: 0.0.1
    Initial Version

Note:

    Module attributes below
"""
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import os
import sys
import time


def path_setup():
    """Path setup: If extensions (or modules to document with autodoc) are in
    another directory, add these directories to sys.path here. If the directory
    is relative to the documentation root, use os.path.abspath to make it
    absolute, like shown here.
    """
    sys.path.insert(0, os.path.abspath('./'))
    sys.path.insert(0, os.path.abspath('../..'))
    sys.path.insert(0, os.path.abspath('../../examples/data'))
    sys.path.insert(0, os.path.abspath('../../examples/example1'))
    sys.path.insert(0, os.path.abspath('../../examples/example2'))
    sys.path.insert(0, os.path.abspath('../../examples/example3'))


def sphinx_setup():
    """Sphinx setup config variables"""

    globals()['templates_path'] = ['_templates']
    """Add any paths that contain templates here, relative to this directory."""

    # globals()['exclude_patterns'] = ['*.md','LICENSE']
    # """ List of patterns, relative to source directory, that match files and
    # directories to ignore when looking for source files. This pattern also
    # affects html_static_path and html_extra_path.
    # """

    globals()['today_fmt'] = '%B %d, %Y'
    """The format for `|today| replacement directives`. There are two options for
    replacing |today|: either, you set today to some non-false value, then it is
    used: today = '' Else, today_fmt is used as the format for a strftime call.
    """

    globals()['html_last_updated_fmt'] = '%b %d, %Y'
    """The format for \"Last updated on\" timestamps inserted on page footers If not
    '', a 'Last updated on:' timestamp is inserted at every page bottom, using the
    given strftime format.
    """

    globals()['add_module_names'] = False
    """A boolean that decides whether module names are prepended to all object
    names. Set to False to avoid `autosummary` clashes with object names. This is
    due to the order of processing between `autodoc` and `autosummary`.
    """





def runtime_setup():
    """Standard boilerplate variables"""

    globals()['year'] = time.strftime("%Y")      # or "%y"
    """Current year at build time. This is a calculated value. Used for copyright information."""

    globals()['project'] = 'EditFrontMatter'
    """VCS and the like project name. The project name used for sites like github and
    pypi. Appears in the heading and is used for `_templates/layout.html` links.
    Note that this variable is used by sphinx internally as well."""

    globals()['project_name'] = globals()['project']
    """This is a copy of `project` to reduce ambiguity. This variable should be used
    in all new development where `project` used relative to future versions of the
    theme boilerplate.
    """

    globals()['project_title'] = 'Edit Front Matter Module'
    """The title of the project that is represented by the `project_name`"""

    # project_homepage = '\`Sphinx RTD Boilerplate <https://karlredman.github.io/spinx-rtd-boilerplate>\`_'

    globals()['author'] = 'Karl N. Redman'
    """Name of the author (or organization)."""

    globals()['author_homepage'] = "https://karlredman.github.io"
    """Author (or organization's) homepage."""

    globals()['copyright'] = '{}, {}'.format(globals()['year'], globals()['author'])
    """copyright statement (autoformatted)."""

    globals()['vcs_domain'] = "github.com"
    """The online VCS domain (i.e. github). Used for `Edit on Github` and similar
        links from `_templates/layout.html`"""

    globals()['vcs_username'] = 'karlredman'
    """The online VCS user name. Used for `_templates/layout.html` links."""

    globals()['doc_domain'] = "github.io"
    """The domain used for documentation. Used for `_templates/layout.html` links"""

    globals()['release'] = '0.0.1'
    """The full release version string for the project, including alpha/beta/rc tags."""

    # language versions
    globals()['python_version'] = "3.5.3"
    """Minimum python version -used to fill in documentation for modules and other sources."""

    # widget behavior
    globals()['use_vcs_ribbon'] = True
    """bool display the customizable 'fork on github' style ribbon
    """

    globals()['ribbon_target'] = 'target="_blank"'
    """Controls if the ribbon opens in the current tab/window or opens a new one.
        Set to null string to open in same window / `target=_blank` to open in new tab/window"""

    globals()['ribbon_title'] = 'Fork me on GitHub'
    """Title used displayed on the ribbon"""



def extensions_setup():
    """
    Add any Sphinx extension module names here, as strings. They can be
    extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
    ones.

    :Extensions (alphabetical):

        * `m2r <https://pypi.org/project/m2r/>`_

            * M2R converts a markdown file including reStructuredText (rst)
              markups to a valid rst format.

            * Likely to cause warnings for some markdown `pygments` highlighting
              code blocks.

        * `sphinx.ext.autodoc
          <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_

            * Include documentation from docstrings.

        * `sphinx.ext.autosummary
          <https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html>`_

            * Generate autodoc summaries

            * Likely to cause `duplicat object` definition warnings that seem to
              be unfixable.

        * `sphinx.ext.doctest
          <https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html>`_

            * Test snippets in the documentation

        * `sphinx.ext.githubpages
          <https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html>`_

            * Publish HTML docs in GitHub Pages

        * `sphinx.ext.intersphinx
          <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`_

            * Link to other projects’ documentation

        * `sphinx.ext.napoleon
          <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_

            * Support for `NumPy
              <https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_
              and `Google
              <https://google.github.io/styleguide/pyguide.html#Comments>`_
              style docstrings.

        * `sphinx.ext.todo
          <https://www.sphinx-doc.org/en/latest/usage/extensions/todo.html>`_

            * Support for todo items

        * `sphinx.ext.viewcode
          <https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html>`_

            * Add links to highlighted source code
    """
    globals()['extensions'] = [
        'm2r',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.doctest',
        'sphinx.ext.intersphinx',
        'sphinx.ext.githubpages',
        'sphinx.ext.napoleon',
        'sphinx.ext.todo',
        'sphinx.ext.viewcode',
        # 'recommonmark',
        # 'sphinx.ext.ifconfig',
        # 'sphinx.ext.inheritance_diagram',
    ]


def html_config():
    """Sphinx HTML config
    """

    # default: html_theme = 'alabaster'
    globals()['html_theme'] = 'sphinx_rtd_theme'
    """
    The theme to use for HTML and HTML Help pages.  See the documentation for
    a list of builtin themes.
    """


    globals()['html_static_path'] = ['_static']
    """
    Add any paths that contain custom static files (such as style sheets) here,
    relative to this directory. They are copied after the builtin static files,
    so a file named "default.css" will overwrite the builtin "default.css".
    """

    # globals()['html_logo'] = "mylogo_400x400.png"
    """
    Logo image
    """

    globals()['html_context'] = {
        'project_name': globals()['project_name'],
        'project_title': globals()['project_title'],
        'release': globals()['release'],
        'vcs_domain': globals()['vcs_domain'],
        'vcs_username': globals()['vcs_username'],
        'use_vcs_ribbon': globals()['use_vcs_ribbon'],
        'ribbon_target': globals()['ribbon_target'],
        'author_homepage': globals()['author_homepage'],
        'doc_domain': globals()['doc_domain'],
    }
    """
    Variables used for replacing text in html templates.
    ref: [Get variables in Sphinx templates - Stack Overflow](https://stackoverflow.com/questions/27381997/get-variables-in-sphinx-templates)
    """

    # globals()['html_sidebars'] = { '**': ['localtoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'] }


# RTD Theme
def html_theme_options_config():
    globals()['html_theme_options'] = {
        'canonical_url':
        'https://{vcs_username}.github.io/{project_name}'.format(vcs_username=globals()['vcs_username'], project_name=globals()['project_name']),
        # 'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
        'logo_only': False,
        'display_version': True,
        'prev_next_buttons_location': 'top',
        'style_external_links': True,
        # 'vcs_pageview_mode': '',
        'style_nav_header_background': 'black',
        # Toc options
        'collapse_navigation': False,
        'sticky_navigation': True,
        'navigation_depth': 400,
        'includehidden': True,
        'titles_only': False,
    }
    """
    Options specific to the RTD Sphinx theme.
    """


def extensions_config():

    # -- Extension configuration -------------------------------------------------

    globals()['autosummary_generate'] = True
    """[c]an be used to generate short “stub” files for the entries listed in the
    `autosummary` directives. This may be causing some issues with dupllicate
    definitions. TODO: more testing needed. This is set to `True` to provide easier
    additions of new modules and programs to toctrees.
    """
    # globals()['autosummary_mock_imports'] = []
    # globals()['autosummary_imported_members'] = False

    # app api settings
    # for m2r extension
    globals()['source_suffix'] = ['.rst', '.md']

    # viewcode
    globals()['viewcode_follow_imported_members'] = True

    # Napoleon
    globals()['napoleon_google_docstring'] = True
    globals()['napoleon_numpy_docstring'] = True
    globals()['napoleon_include_init_with_doc'] = False
    globals()['napoleon_include_private_with_doc'] = True
    globals()['napoleon_include_special_with_doc'] = True
    globals()['napoleon_use_admonition_for_examples'] = True
    globals()['napoleon_use_admonition_for_notes'] = True
    globals()['napoleon_use_admonition_for_references'] = True
    globals()['napoleon_use_ivar'] = True
    globals()['napoleon_use_param'] = True
    globals()['napoleon_use_rtype'] = True


    # github
    globals()['html_context'].update({
        "display_github": True,  # Integrate GitHub
        "github_user": globals()['vcs_username'],  # Username
        "github_repo": globals()['project_name'],  # Repo name
        "github_version": "master",  # Version
        "conf_py_path": "/docsource/source/",  # Path in the checkout to the docs root
    })

    # autodoc
    globals()['autodoc_default_options'] = {
        # 'members': 'var1,var2',
        'member-order': 'bysource',
        # 'special-members': '__init__',
        # 'undoc-members': True,
        # 'exclude-members': '__weakref__'
    }

    globals()['autodoc_default_flags'] = ['members']


    # intersphinx
    globals()['intersphinx_mapping'] = {'jinja2': ('http://jinja.pocoo.org/docs/', None),
                                        'python': ('https://docs.python.org/3', None),
                                        # 'EditFrontMatter': ('https://karlredman.github.io/EditFrontMatter', None),
                                        'editfrontmatter': ('https://karlredman.github.io/EditFrontMatter', None),
                                        # 'pyyaml': ('https://pyyaml.org/wiki/PyYAMLDocumentation')
                                        }

    # todo
    # If true, `todo` and `todoList` produce output, else they produce nothing.
    globals()['todo_include_todos'] = True
    globals()['todo_emit_warnings'] = True


def rst_epilog_config():
    """A string of reST that will be included at the end of every source
    file that is read. This is a possible place to add substitutions that should be
    available in every file (another being `rst_prolog`).

    Note that this string will not replace document titles due to the order by which
    files are processed relative to hierarchical `toctree` directives.
    """
    globals()['rst_epilog'] = """
.. |python_version| replace:: python >=v{python_version}
.. |release| replace:: {release}
.. |author| replace:: {author}
.. |project_title| replace:: {project_title}
.. |project_name| replace:: {project_name}
    """.format(
        python_version=globals()['python_version'],
        release=globals()['release'],
        author=globals()['author'],
        project_title=globals()['project_title'],
        project_name=globals()['project_name'],
    )



def setup(app):
    """setup custom directives for execution of the app, e.g.
    `app.add_stylesheet()`

    References:

        `Sphinx api documentation <https://www.sphinx-doc.org/en/master/extdev/appapi.html?highlight=app>`_

    """
    app.add_stylesheet('theme_customization.css')


# call functions in order of precedence
path_setup()
sphinx_setup()
runtime_setup()
extensions_setup()
html_config()
html_theme_options_config()
extensions_config()
rst_epilog_config()

