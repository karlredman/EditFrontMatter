#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
*Basic Front Matter Editing Example*
====================================

.. module:: example1

.. program:: example1

:Synopsis: Example program that performs the following actions:

    #. Reads a Jinja2 template

        .. literalinclude:: ../../../../examples/data/template1.j2
            :language: jinja

    #. Reads a mardown file that contains yaml front matter via :func:`editfrontmatter.EditFrontMatter.readFile`

        .. literalinclude:: ../../../../examples/data/example1.md

    #. Extracts the front matter from the source file

    #. Prorammitically edits the front matter via \
        :func:`editfrontmatter.EditFrontMatter.run`

    #. Concatinates the edited front matter with the original file content via \
        :func:`editfrontmatter.EditFrontMatter.dumpFileData`

    #. Prints the edited file to `stdout`

:Dependencies:

    .. literalinclude:: ../../../../examples/requirements.txt
        :language: text

:Platform: Unix, Windows, |python_version|

:License: :download:`MIT <../../../../LICENSE>`

.. :moduleauthor: `Karl N. Redman <https://karlredman.github.io>`_

:Author: `Karl N. Redman <https://karlredman.github.io>`_

:homepage: `EditFrontMatter Example 1 <https://karlredman.github.io/EditFrontMatter/examples/example1/readme.html>`_

:Current Release:
    version: |release|

.. versionadded:: 0.0.1
    Initial Version
"""


from editfrontmatter import EditFrontMatter
import os


def canPublish_func(val):
    """
    :Description:
        Example callback function used to populate a jinja2 variable. Note that
        this function must be reentrant for threaded applications.

    Args:
        val (object): generic object for the example

    Returns:
        example content (True)
    """
    # do some processing....
    return True


def main():
    """
    :Description:
        Basic example function for processing yaml with a jinja template and a
        markdown file with yaml content.

    :envvar: TEST_DATA_DIR
        Variable used to specify the path to the data files.

    Attributes:
        DATA_PATH (str):
            generic path if running from the local `example1` directory

        file_path (str):
            path of data (markdown) file to be read

        template_str (str):
            string containing the contents of a Jinja2 template

        proc (EditFrontMatter):
            the EditFrontmatter object

    Returns:
        program exit status (0 or 1)

    Example:

        To run from a non program directory use the environment variable::

            TEST_DATA_DIR="./data/" example1/example1.py

    """

    # generic path - overridden by env var `TEST_DATA_DIR`
    DATA_PATH = "../data/"

    if "TEST_DATA_DIR" in os.environ:
        DATA_PATH = os.path.abspath(os.environ.get("TEST_DATA_DIR")) + "/"

    # set path to input file
    file_path = os.path.abspath(DATA_PATH + "example1.md")

    # initialize `template_str` with template file content
    template_str = ''.join(open(os.path.abspath(DATA_PATH + "template1.j2"), "r").readlines())

    # instantiate the processor
    proc = EditFrontMatter(file_path=file_path, template_str=template_str)

    # set fields to delete from yaml
    proc.keys_toDelete = ['deleteme']

    # add a filter and callback function
    proc.add_JinjaFilter('canPublish', canPublish_func)

    # populate variables and run processor
    proc.run({'toc': 'no effect', 'hasMath': "false",
              'addedVariable': ['one', 'two', 'three']})

    # dump file
    print(proc.dumpFileData())


if __name__ == '__main__':
    main()
