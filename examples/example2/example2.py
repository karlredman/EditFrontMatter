#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
*Advanced, Multi-Pass, Front Matter Editing Example*
=======================================================

.. module:: example2

:Program: example2

:Synopsis: Example program that performs the following actions:

    #. Derives a class from `EditFrontMatter`

    #. Performs execution in a try block

        #. raises an exception form the derived class for example purposes
        #. catches the exception and prints a messae

    #. Sets up a signal handler for `SIGHUP` and `SIGINT` for testing/example

    #. Set up a `try` block for catching exceptions: Can be tested by providing \
        a nonexistant file name for input

    #. Uses a Jinja2 template

        .. literalinclude:: ../../../../examples/data/template1.j2
            :language: jinja

    #. Reads a mardown file that contains yaml front matter via \
        :func:`editfrontmatter.EditFrontMatter.EditFrontMatter.readFile`

        .. literalinclude:: ../../../../examples/data/example1.md
            :language: md

    #. Extracts the front matter from the source file

    #. Prorammitically edits the front matter via \
        :func:`editfrontmatter.EditFrontMatter.EditFrontMatter.run`

    #. Concatinates the edited front matter with the original file content via \
        :func:`editfrontmatter.EditFrontMatter.EditFrontMatter.dumpFileData`

    #. Prints the edited file to `stdout`

    #. Resets the Jinja2 template for secondary processing

    #. Resets the input file for processing against a new template

        .. literalinclude:: ../../../../examples/data/template2.j2
            :language: jinja

    #. Reprocesses the previous output as input while concatinating the new input file

        .. literalinclude:: ../../../../examples/data/example2.md
            :language: md

    #. Prints the edited output to `stdout`

:Platform: Unix, Windows, |python_version|

:Dependencies:

    .. literalinclude:: ../../../../requirements.txt
        :language: text

:License: :download:`MIT <../../../../LICENSE>`

.. :moduleauthor: `Karl N. Redman <https://karlredman.github.io>`_

:Author: `Karl N. Redman <https://karlredman.github.io>`_

:homepage: `EditFrontMatter Example 2 <https://karlredman.github.io/EditFrontMatter/examples/example2/readme.html>`_

:Current Release:
    version: |release|

.. versionadded:: 0.0.1
    Initial Version
"""

import os
import signal
from editfrontmatter import EditFrontMatter
from editfrontmatter import EditFrontMatter_Exception


# setup signal handler for kicks and giggles
class Signal_Caught(Exception):
    pass


def SignalHandler(sig, frame):
    """Generic Signal handler"""
    message = ("Received signal {} on line {} in {}"
               .format(str(sig), str(frame.f_lineno), frame.f_code.co_filename))
    raise Signal_Caught(message)


# catch signals
signal.signal(signal.SIGINT, SignalHandler)
signal.signal(signal.SIGHUP, SignalHandler)


# Derive class
class Derived_EditFrontMatter (EditFrontMatter):
    """EditFrontMatter derived class for example purposes"""
    def __init__(self, Superfluous, **kwargs):
        """A specialized signature for the derived class"""
        EditFrontMatter.__init__(self, **kwargs)
        self.Superfluous = Superfluous

    def canPublish_method(self, var) -> bool:
        """Class level callback method

        Note:
            It's important that class level callbacks are codded to be reentrant.
            If the class is used in a threaded app class level veriables would not
            be thread-safe. Also, use critical sections if working with threads.


        Returns: a mock value
        """
        return "none"
        pass

    def run(self, template_str, file_path, **kwargs) -> None:
        """A override method for the baseclass `run` method

        This is just a contrived example meant to demonstrate some advanced usage
        of the base class.
        """

        # update member vars
        self.template_str = template_str
        self.file_path = file_path

        # save file data and yaml object (fmatter) yaml_end point
        orig_file_lines = self.file_lines
        orig_yaml_obj = self.fmatter
        orig_yaml_end = self.yaml_end

        # read new (no front matter) file
        self.readFile(file_path)

        # replace filter with class method
        self.del_JinjaFilter('canPublish')
        self.add_JinjaFilter('canPublish', self.canPublish_method)

        # concatinate orig_file with new file
        orig_file_lines.append("\n")
        self.file_lines = orig_file_lines + self.file_lines

        # replace new yaml obj with original
        self.fmatter = orig_yaml_obj

        self.keys_toDelete = ['stuff']

        # procesess the data
        super().run(extraVars_dict={'weight': 10})

        # restore yaml_end so we can dump the file with the original end point
        # (.i.e so we can dump the new yaml with the old file content starting
        # point).
        self.yaml_end = orig_yaml_end

    def parent_run(self, extra_vars):
        """cheezy method to call a parent method"""
        super().run(extra_vars)


# callback function for jinja filter
def canPublish_func(var) -> bool:
    """Callback function for Jinja2 filters"""
    # ...do processing
    return True


def main():
    """Main function

    Attributes:

        DATA_PATH (str):
            Path that points to the data file directory. Must end with a `/`

        file_path1 (str):
            Path to input source 1
        file_path2 (str):
            Path to input source 2

        template_str1 (str):
            Contents of template1
        template_str2 (str):
            Contents of template2

    :envvar: TEST_DATA_DIR
        Variable used to specify the path to the data files.

    Returns:
        program exit status (0 or 1)

    Example:

        To run from a non program directory use the environment variable::

            TEST_DATA_DIR="./data/" example2/example2.py

    """

    # generic path - overridden by env var `TEST_DATA_DIR`
    DATA_PATH = "../data/"

    if "TEST_DATA_DIR" in os.environ:
        DATA_PATH = os.path.abspath(os.environ.get("TEST_DATA_DIR")) + "/"

    # set path to input file
    file_path1 = os.path.abspath(DATA_PATH + "example1.md")
    file_path2 = os.path.abspath(DATA_PATH + "example2.md")      # no front matter

    # initialize `template_str` with template file content
    template_str1 = ''.join(open(os.path.abspath(DATA_PATH + "template1.j2"), "r").readlines())
    template_str2 = ''.join(open(os.path.abspath(DATA_PATH + "template2.j2"), "r").readlines())

    # create object
    proc = Derived_EditFrontMatter(None, template_str=template_str1, do_readFile=False)

    # add jinja filter for callback
    proc.add_JinjaFilter('canPublish', canPublish_func)

    try:
        # normal processing
        proc.readFile(file_path=file_path1)
        proc.parent_run({'toc': 'no effect', 'hasMath': "false",
                         'addedVariable': ['one', 'two', 'three']})
        print(proc.dumpFileData())

        print("##################### PASS SEPERATION #######################")
        # new swap the template
        proc.run(template_str2, file_path2)
        print(proc.dumpFileData())

    except Signal_Caught as e:
        print(str(e))
        os.exit(1)
    except EditFrontMatter_Exception as e:
        print(str(e))
        os.exit(1)
    else:
        print("No Exceptions.")
    finally:
        print("done.")

    print("end program")


if __name__ == '__main__':
    main()
