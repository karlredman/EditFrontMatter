# RTD Theme Developer Notes

* These notes are intended to be part of future documentation for a Sphinx RTD Theme Boilerplate project.
* These notes provide snippiets of information in regard to configuring the current theme.

## Layout:

## Sphinx Notes:

### References:

* [sphinx/directives.rst at master · sphinx-doc/sphinx](https://github.com/sphinx-doc/sphinx/blob/master/doc/usage/restructuredtext/directives.rst)


### Building:

* Setup development environment:

```
cd <project_root>
virtualenv venv
pip install -r requirements.txt
```

* Build docs:

```
# prep build environment
cd <project_root>/docsource
pip install -r requirements.txt

# for each document module (if sources added)
sphinx-apidoc -o source/editfrontmatter ../editfrontmatter
sphinx-apidoc -o source/examples/example1 ../examples/example1
sphinx-apidoc -o source/examples/example2 ../examples/example2
sphinx-apidoc -o source/examples/example3 ../examples/example3
sphinx-apidoc -o source/examples/example4 ../examples/example4

# run doctest (with custom path)
TEST_DATA_DIR="../examples/data/" make doctest

# make the docs (for github pages)
## the path is usually not necessary
TEST_DATA_DIR="../examples/data/" make github
```

* Access/Review:
  * open browser `<project_root>/docs/build/`

### Live update dev server

* [GaretJax/sphinx-autobuild: Watch a Sphinx directory and rebuild the documentation when a change is detected. Also includes a livereload enabled web server.](https://github.com/GaretJax/sphinx-autobuild)
  * only works for sphinx sources. does not catch code changes

```sh
cd <project dir>/docsource
pip install -r requirements.txt
#
cd <project dir>
sphinx-autobuild docsource/source docsource/build/html
```

### Fixes

* Change the width of the displayed page
  * reference: [html - Modifying content width of the Sphinx theme 'Read the Docs' - Stack Overflow](https://stackoverflow.com/a/43186995/1725771)
* quoted from the reference:

```
Just in case someone is still searching for a simple answer... combining the ideas from https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/ and the above suggestions i found that the most easy way of getting a custom window-width is the following:

in conf.py add a function that adds your custom stylesheet (just add the following lines):

########## code block
def setup(app):
    app.add_stylesheet('my_theme.css')
##########

and then create a file called my_theme.css in the _static folder that simply contains the following lines:

########## code block
.wy-nav-content {
max-width: 1200px !important;
}
##########
```

* Setup `Makefile` for building github pages (for `master:/docs')
  * add a `github` target to `Makefile`

  ```makefile
  github:
      @make html
      @rm -rf ../docs/*
      @cp -a build/html/* ../docs/
  ```

* Build message: "WARNING: document isn't included in any toctree for included file: `modules.rst`"
  * add `modules` to the `index.rst` (or appropriat) file

  ```rst
  .. toctree::
      :maxdepth: 2
      :caption: Contents:

      modules
  ```

* Hide contents from page while adding it to `toctree` sidebar

  ```rst
  .. toctree::
      :maxdepth: 2
      :caption: Contents:
      :hidden:

      modules
  ```

* color words / characters in a page
  * reference: [html - sphinx, restructuredtext: set color for a single word - Stack Overflow](https://stackoverflow.com/a/56303496/1725771)
  ```rst
  .. role:: raw-html(raw)
   :format: html

  :raw-html:`<font color="blue">Blue word,</font>` And a word without color
  ```

### Sphinx RTD Theme Notes:

#### References:

* [rtfd/sphinx_rtd_theme: Sphinx theme for readthedocs.org](https://github.com/rtfd/sphinx_rtd_theme)

#### GitHub 'Fork on GitHub' Banner:

* Alternate images: [tholman/github-corners: A fresher "Fork me on GitHub" callout.](https://github.com/tholman/github-corners)
* Add the following to `docsource/source/_templates/layout.html`

```jinja
{% extends '!layout.html' %}
  {% block document %}
  {{super()}}
      <a href="https://github.com/karlredman/EditFrontMatter">
          <img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub">
      </a>
  {% endblock %}

```

#### Site index on sidebar

* reference: [How to add Sphinx-generated index to the sidebar when using Read the Docs theme? - Stack Overflow](https://stackoverflow.com/a/37843854/1725771)
* Note: this will cause issues if `genindex.html` is not handled properly

* Add the following to `docsource/source/_templates/layout.html`

```jinja
{% extends "!layout.html" %}
  {% block menu %}
    <a href="https://karlredman.github.io/EditFrontMatter/genindex.html">Index</a>
    {{ super() }}
  {% endblock %}
```

#### Remove the word "module" from the end of sidebar code elements

* Add the following to `docsource/source/_templates/layout.html`

```jinja
{% extends '!layout.html' %}
{% block extrahead %}
	<script type="text/javascript">
	window.onload = function() {
		document.body.innerHTML = document.body.innerHTML.replace(/ module/g, '');
	}
	</script>
{% endblock %}
```

## Theme Style guide

### References (for later documentation)

* [Example Google Style Python Docstrings — Sphinx 3.0.0+/f63abac2c documentation](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google)
* [Sample Document — sphinx theme for basicstrap style documentation](https://pythonhosted.org/sphinxjp.themes.basicstrap/sample.html)
* [sphinx.ext.napoleon – Support for NumPy and Google style docstrings — Sphinx 3.0.0+/f63abac2c documentation](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
* [Example Google Style Python Docstrings — Sphinx 3.0.0+/f63abac2c documentation](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google)
* [Roles — Sphinx 3.0.0+/f63abac2c documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#xref-syntax)

### Docstrings (python)

* module
  * The module must be documented at the top of the file just below the `shebang`.
    * `moduleauthor` is documented a second time for readablility and compatibility with python standards.
    * a `__main__` bock **must** be used to maintain compatibility with sphinx preprocessing.

```py3
"""
*PROJECT_NAME Module*
===========================================

.. module:: MODULE_NAME

:Synopsis: SYNOPSIS

:Platform: Unix, Windows, |python_version|

:Dependencies:

    .. literalinclude:: ../../../requirements.txt
        :language: text

:License: :download:

.. :moduleauthor: `Karl N. Redman <https://karlredman.github.io>`_

:Module Author: _

:homepage: `PROJECT_NAME <https://karlredman.github.io/PROJECT_NAME>`
:homepage: `PROJECT_NAME <https://github.com/karlredman/PROJECT_NAME>`

:Current Release:
    version: |release|

.. versionadded:: 0.0.1
    Initial Version
"""


def main():
    pass


if __name__ == '__main__':
    main()

```








* class
  * A short docstring must be placed at the top of the class just under the class signature in order for `autosummary` to pick up the text.
    * Note, do **not** document instatniation or attributes at the class level. Use `__init__` for this purpros.
* class `__init__`
  * Use `__init__` to document constructor arguments, attributes, and other similar class related information.
    * Sphinx `autosummary` expects documentation for these things to be located wihin `__init__`
    * the sphinx `config.py` should be configured with the following to properly include the `__init__` method in documentation
      * `napoleon_include_init_with_doc = True`
      * `autodoc_default_options = { 'special-members': '__init__', }`

* method / function
  * Docstrings should followthe layout of the template below:

  ```py3
  def myfunc() -> None:
      """
      :Description:
          SUMMARY

      Args:
          NAME (TYPE):
              DESCRIPTION

      [:rtype: | Returns:]
          RETURN INFO
      """
  ```


### Things to Document

### Rules:

* Order of precedence
  * [autodoc method](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
  * [google method](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google))
    * [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
  * [intersphinx](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html)

* instance attributes are documented as such:

```rst
Attributes:
    DATA_PATH (str):
        generic path if running from the local the `example1`
        directory

    file_path (str):
        path of data (markdown) file to be read

    template_str (str):
        string containing the contents of a Jinja2 template

    proc (EditFrontMatter):
        the EditFrontatter object
```

## Generating class methods for use the sidebar toc and respective individual files

* Autosummary method (with automodule)
* Note that if you use links to files outside of the docsource tree then you willl needto make some decisions .... maybe eliminate `_autosummary`

for a sphinx module directory that is 'wired' to a package, where automodule is used already, it is possible to generate the method files required for adding to the toc. Note that this creates a lot of warnings and the process is rather ughly.

* The docsource directory (sphinx base) looks like this before generating the individal method files:
* This process is, by far, not optimal and probably not entirely practicle
  * maintenance, adding new functions, etc., would be fairly cumbersome

```
.
├── conf.py
├── editfrontmatter
│   └── editfrontmatter.rst
├── index.rst
├── modules.rst
├── _static
│   └── theme_customization.css
└── _templates
    └── layout.html
```

* The chain for the rst files is this:

```
index.rst --> modules --> editfrontmatter.rst
```

### Before adding autosummary functionality

* modules.rst looks like this:

```rst
EditFrontMatter package
=======================

.. toctree::
   :maxdepth: 2

   editfrontmatter/editfrontmatter
```

* editfrontmatter.rst is the package level rst (before autosummary changes)

```
.. automodule:: editfrontmatter.EditFrontMatter
    :noindex:

.. autoclass:: editfrontmatter.EditFrontMatter([options])
    :members:
    :undoc-members:
    :private-members:
    :inherited-members:
    :show-inheritance:
    :special-members: __init__
    :member-order: bysource

.. autoclass:: editfrontmatter.EditFrontMatter_Exception([options])
    :members:
    :undoc-members:
    :private-members:
    :inherited-members:
    :show-inheritance:
    :special-members: __init__
    :member-order: bysource
```

### Generate method files

* add the following to the bottome of `editfrontmatter.rst`. This will add a class definition file into the `_autosummary` subdirectory.

```rst
.. autosummary::
    :toctree: _autosummary

    EditFrontMatter
```

* run sphinx-autogen to add the class files into a subdirectory. Creates file `source/editfrontmatter/_autosource/_autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.rst`

```sh
sphinx-autogen -o source/editfrontmatter/_autosummary source/editfrontmatter/editfrontmatter.rst
```

* edit the new file `<path>/_autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.rst` and add `:toctree` to the `.. autosummary directive`. Here's the entire file after edit:

```rst
editfrontmatter.EditFrontMatter.EditFrontMatter
===============================================

.. currentmodule:: editfrontmatter.EditFrontMatter

.. autoclass:: EditFrontMatter


   .. automethod:: __init__


   .. rubric:: Methods

   .. autosummary::
      :toctree:

      ~EditFrontMatter.__init__
      ~EditFrontMatter.add_JinjaFilter
      ~EditFrontMatter.del_JinjaFilter
      ~EditFrontMatter.dumpFileData
      ~EditFrontMatter.dumpFrontMatter
      ~EditFrontMatter.readFile
      ~EditFrontMatter.run
      ~EditFrontMatter.set_yaml_delim
      ~EditFrontMatter.writeFile
```

* Build sphinx: This will causea lot of warnings. We'll fix some of them in the next step. Also, this will cause the individal method files to be generated.

```
make clean; TEST_DATA_DIR="../examples/data/" make github
```

* `_autosummary/` now looks like this:

```
$ ls _autosummary/
editfrontmatter.EditFrontMatter.EditFrontMatter.add_JinjaFilter.rst  editfrontmatter.EditFrontMatter.EditFrontMatter.__init__.rst  editfrontmatter.EditFrontMatter.EditFrontMatter.set_yaml_delim.rst editfrontmatter.EditFrontMatter.EditFrontMatter.del_JinjaFilter.rst  editfrontmatter.EditFrontMatter.EditFrontMatter.readFile.rst  editfrontmatter.EditFrontMatter.EditFrontMatter.writeFile.rst editfrontmatter.EditFrontMatter.EditFrontMatter.dumpFileData.rst     editfrontmatter.EditFrontMatter.EditFrontMatter.rst editfrontmatter.EditFrontMatter.EditFrontMatter.dumpFrontMatter.rst  editfrontmatter.EditFrontMatter.EditFrontMatter.run.rst
```

* Edit `editfrontmatter.rst` again to remove the `autosummary` directive and add a `toctree` for the newly generated files. The final file looks like this:

```rst
.. automodule:: editfrontmatter.EditFrontMatter
    :noindex:

.. autoclass:: editfrontmatter.EditFrontMatter([options])
    :members:
    :undoc-members:
    :private-members:
    :inherited-members:
    :show-inheritance:
    :special-members: __init__
    :member-order: bysource

.. autoclass:: editfrontmatter.EditFrontMatter_Exception([options])
    :members:
    :undoc-members:
    :private-members:
    :inherited-members:
    :show-inheritance:
    :special-members: __init__
    :member-order: bysource

.. toctree::
    :hidden:

    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.EditFrontMatter
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.__init__
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.add_JinjaFilter
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.del_JinjaFilter
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.dumpFileData
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.dumpFrontMatter
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.readFile
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.run
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.set_yaml_delim
    _autosummary/editfrontmatter.EditFrontMatter.EditFrontMatter.writeFile
```

* finally, rebuild sphinx again
  * optionally change the headings of each of the generated files for easier reading on the sidebar.

### maintenance:

* For each new method added to the source file you will have to:
  * create the new file under `_autosummary`
  * add the method spec to `editfrontmatter.rst`

## Include mardown document in reST

* Reference: [miyakogi/m2r: Markdown to reStructuredText converter](https://github.com/miyakogi/m2r#sphinx-integration)


## Boilerplate features

* Greeting page is automatically linked to project README.md
* Theme documentation is built in
  * easily removed

### configurables

### replacement text restrictions in the docstring for config.py

* text replacement can't be used within grave marks -hence all rst links
* `:homepage:` must be entered without using ext replacement
  * TODO: find different solution
    * [Sphinx html variables - Stack Overflow](https://stackoverflow.com/questions/44591448/sphinx-html-variables)
  * the file docstring title: is not processed for sphinx replacement
    * TODO: needs more investigation




## Pre publishing checklist

* check the gitignore files and adjust accordingly

```
git status --ignored
```

* if it's a sandbox git repo that is already published, replace history:
  * [Steps to clear out the history of a git/github repository · GitHub](https://gist.github.com/stephenhardy/5470814)

  ```
  # double check .gitignore
  git status --ignored

  # check documentation is in order

  # make sure everything builds and runs

  # make sure tests pass

  # Remove the history from
  rm -rf .git

  # recreate the repos from the current content only
  git init
  git add -A
  git commit -m "Initial commit"

  # push to the github remote repos ensuring you overwrite history
  git remote add origin git@github.com:<YOUR ACCOUNT>/<YOUR REPOS>.git
  git push -u --force origin master

  # checkout the project again and reverify / retest everything
  ```


## Packaging / PyPi Notes:

### References:

* [How to Publish an Open-Source Python Package to PyPI – Real Python](https://realpython.com/pypi-publish-python-package/)
* [Minimal Structure — Python Packaging Tutorial](https://python-packaging.readthedocs.io/en/latest/minimal.html)

### pip install locally

```sh
# cd <project dir>
pip install -e .
```
