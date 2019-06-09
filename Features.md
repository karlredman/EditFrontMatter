# Full Features List

* Add / Update / Delete any front matter fields

* Preserves front matter element order via [oyaml](https://github.com/wimglenn/oyaml)

* Uses [Jinja2](http://jinja.pocoo.org/) Templates for configuration and processing:

    * Use Jinja2 filters for complex processing
    * Incrementally process files with multiple templates (iteratively)

* Allows for multiple passes per source file

* Provides exception handling easier debugging

* Examples for implementation:

    #. [Basic usage](examples/example1/readme)
    #. [Advanced mulit-pass processor](examples/example2/readme)
    #. [Recursive directory walker](examples/example3/readme) that uses multi-threading to edit files

* Extensive Documented

    * with [Sphinx](https://www.sphinx-doc.org/en/master/)
    * hosted on Github: [here](https://karlredman.github.io/EditFrontMatter)
    * Remote references (via sphinx intersphinx) is enabled
    * Compatible with pydoc
    * Bonus documentation of the documentation system and theme used.

* Documentation Boilerplate

    * The documentation can be easily extracted and used for other projects

* [MIT](https://github.com/karlredman/EditFrontMatter/blob/master/LICENSE) Licensed
