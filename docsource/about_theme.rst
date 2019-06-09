:github_url: https://github.com/karlredman/EditFrontMatter/blob/master/docsource/README.md

.. role:: raw-html(raw)
   :format: html

:raw-html:`<font color="#7D6608">About Theme</font>`
====================================================

.. toctree::
    :maxdepth: 1

    dev_notes
    conf
    theme_readme

:Description:

* This is an out-of-the-box implementation of the `Sphinx RTD Theme <https://github.com/rtfd/sphinx_rtd_theme>`_ v0.4.3.

* The configuration for this theme will **eventualy** be converted into a boilerplate project on it's own.

* The layout for this configuration is outlined below.

* For more configuration specifics see the (relatively organized) `developer notes <https://karlredman.github.io/EditFrontMatter/about_theme/dev_notes.html>`_

:Current features for this theme boilerplate configuration:

* The main index page and subsequent section introductions (including this page) import the development `README.md` files via the `m2r <https://pypi.org/project/m2r/>`_ Sphinx extension.

* A compartmentalized `config.py <https://karlredman.github.io/EditFrontMatter/about_theme/conf.html>`_:

  * most configuration will move to yaml in the future

  * `Custom CSS settings <https://github.com/karlredman/EditFrontMatter/blob/master/docsource/source/_static/theme_customization.css>`_:

  * Widen visible content area

  * normalize preformatted text widths

  * dynamically avoid 'Fork me on Github' component conflicts

* Configurable 'Fork me on Github' ribbon

* Custom colorization for TOC sidebar items

* TOC class method itimization in sidebar:

  * see `Class: EditFrontMatter documentation <https://karlredman.github.io/EditFrontMatter/editfrontmatter/editfrontmatter.EditFrontMatter.EditFrontMatter.html>`_


