#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
*Threaded, Directory Walking Example*
===========================================

.. program:: example3.py

:Synopsis: Multithreaded example with signal handling that also demonstrates
    error handling.

:Platform: Unix, Windows, |python_version|

:Dependencies:

    .. Note: literal include is relative to the documentation directory

    .. literalinclude:: ../../../../requirements.txt
        :language: text

:License: `MIT <https://karlredman.github.io/EditFrontMatter/LICENSE>`_

.. :moduleauthor: `Karl N. Redman <https://karlredman.github.io>`_

:Author: `Karl N. Redman <https://karlredman.github.io>`_

:homepage: `EditFrontMatter Example 3 <https://karlredman.github.io/EditFrontMatter/examples/example3/readme.html>`_

:Current Release:
    version: |release|

.. versionadded:: 0.0.1
    Initial Version
"""


import os
import sys
import re
import signal
import concurrent.futures as CFutures
import threading

from editfrontmatter import EditFrontMatter
from editfrontmatter import EditFrontMatter_Exception

# Globals:
print_lock = threading.Lock()
"""Tread lock used for printing"""

STOP_ALL = False
"""a global thread cancel flag"""


class Signal_Caught(Exception):
    """Exception to catch program signals"""
    pass


def SignalHandler(sig, frame):
    """Generic Signal handler.

    Description:
        Catches: SIGINT, SIGHUP
    """
    message = ("Received signal {} on line {} in {}"
               .format(str(sig), str(frame.f_lineno), frame.f_code.co_filename))
    raise Signal_Caught(message)


# catch signals
signal.signal(signal.SIGINT, SignalHandler)
signal.signal(signal.SIGHUP, SignalHandler)


class Derived_EditFrontMatter (EditFrontMatter):
    """EditFrontMatter derived class for example purposes"""

    def __init__(self, **kwargs):
        """Init override with some self thread handling.

        :Description:
            Instantiates the class with some thread self awareness for example
            puproses. Also files are read during the init process.

        Attributes:
            self.EXCEPTION (bool):
                [default: False] Controls flow in methods if an exception is thrown during the init
                process.

            STOP_ALL (bool):
                [Global var] Allows for safe termination of the thread through flow control.

        Throws:
            EditFrontMatter_Exception
        """

        # cancel thread if needed
        self.EXCEPTION = False
        global STOP_ALL
        if STOP_ALL:
            return

        try:
            EditFrontMatter.__init__(self, **kwargs)
        except EditFrontMatter_Exception:
            # we'll fail gracefully -probably a bad source file (i.e. missing
            # and yaml_end delimiter
            with print_lock:
                print("Error (exception): @Derived_EditFrontMatter.__init__(): {file_path}".format(file_path=self.file_path), file=sys.stderr)
            self.EXCEPTION = True

    def run(self, write_file=False, extraVars_dict={}, keys_toDelete=[], *args, **kwargs) -> str:
        """A method overload to process files.

        :Description:
            Class method that performs setup for a call to
            :func:`editfrontmatter.EditFrontMatter.EditFrontMatter.run`.

            The method follows some flow control mechanisms for thread safety.

            The method supresses IOError Exception with a comment loged to
            stderr if the exception occurs.

        Args:
            write_file (bool):
                [default: False] Writes to the source file if True

            extraVars_dict (dict):
                [default: {}]: see :class:`editfrontmatter.EditFrontMatter.EditFrontMatter`

            keys_toDelete (dict):
                [default: []] see :class:`editfrontmatter.EditFrontMatter.EditFrontMatter`

        Calls:
            :func:`editfrontmatter.EditFrontMatter.EditFrontMatter.run`

        Returns:
            The altered file as a string or a null string on error
        """

        # cancel thread if needed
        global STOP_ALL
        if STOP_ALL:
            return ""

        # init() could throw an exception.
        # Allow thread to die gracefully.
        if self.EXCEPTION:
            return ""

        # set fields to delete from yaml
        self.keys_toDelete = keys_toDelete

        # add jinja filter for callback
        self.add_JinjaFilter('canPublish', self.canPublish_func)

        # add vars to change and run the parent run()
        super().run(extraVars_dict=extraVars_dict, keys_toDelete=keys_toDelete)

        err = False
        if not self.has_source_data():
            # file does not contain any data -punt
            with print_lock:
                print("Error: No source data: {file_path}".
                      format(file_path=self.file_path), file=sys.stderr)
            err = True

        if not self.has_source_yaml():
            # file does not contain yaml -punt
            with print_lock:
                print("Error: No source yaml: {file_path}".
                      format(file_path=self.file_path), file=sys.stderr)
            err = True

        try:
            # write if allowed
            if write_file and not err:
                if not self.writeFile():
                    return ""

            # return the concatinated file data as a string
            return self.dumpFileData() if err is False else ""

        except IOError:
            # report that the file write failed and move on
            with print_lock:
                print("Error (IOError exception): @EditFrontMatter.run(): {file_path}"
                      .format(file_path=self.filepath), file=sys.stderr)
            return ""


    def canPublish_func(self, val) -> bool:
        """simple callback for a jinja2 filter variable."""
        return True


def main():
    """Main function for the program.

    :Description:
        The function set's up the environment and artificats for processing
        markdown files with yaml content to be updated. The function also
        manages threads that perform the work.


    Returns:
        * 0 on success
        * 1 on error
    """


    # generic path - overridden by env var `TEMPLATE_DIR`
    TEST_DATA_DIR = os.path.abspath("../data/")
    if "TEST_DATA_DIR" in os.environ:
        TEST_DATA_DIR = os.path.abspath(os.environ.get("TEST_DATA_DIR")) + "/"

    # thread setup
    max_threads = 5

    # data setup
    exclude_dirs = [os.path.abspath(TEST_DATA_DIR + "/example_dir_structure/a/c/b")]
    include_dirs = [os.path.abspath(TEST_DATA_DIR + "/example_dir_structure")]

    # jinja template filter
    template_str = ''.join(open(os.path.abspath(TEST_DATA_DIR + "/template1.j2"), "r").readlines())

    # list of files to process in this tree
    files_to_process_list = []

    # only files ending in `.md` extension
    filename_pattern = re.compile(".*\.md$")

    # make sure includes are not excludes -would mess up the os.walk() otherwise
    for top in include_dirs:
        if os.path.normpath(top) in (os.path.normpath(p) for p in exclude_dirs):
            # error
            print("Error: Included dir, {top}, found in exclude_dirs list".
                  format(top), file=sys.stderr)
            exit(1)

    # build file list by walking the included directories
    for top in include_dirs:
        for root, dirs, files in os.walk(top, topdown=True):
            # exclude recursive path if it's in the exclusion list
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]

            # save file to list
            for file in files:
                if filename_pattern.match(file):
                    files_to_process_list.append(os.path.join(root, file))

    # process files via threaded instances of our derived class
    processed_count = 0
    threads = {}
    try:
        with CFutures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            # submit threads
            threads = {executor.submit(Derived_EditFrontMatter(
                template_str=template_str, file_path=path, do_readFile=True).run,
                write_file=False,               # Set True to write files
                extraVars_dict={'toc': 'no effect',
                                'hasMath': "false",
                                'addedVariable': ['one', 'two', 'three']},
                keys_toDelete=['deleteme']
            ):
                path for path in files_to_process_list}

            # wait for completed threads
            for future in CFutures.as_completed(threads):

                # our thread returns the file path
                file_path = threads[future]

                try:
                    # retain the returned data from run
                    data = future.result()
                except Exception as exc:
                    # generic exception handler.... eeep!
                    print("{file_path} generated an exception: {exc}".
                          format(file_path=file_path, exc=exc), file=sys.stderr)
                else:
                    # print the file path and file data returned from run()
                    # print(f"processed: {file_path}\n{data}")

                    # just print the file paths
                    print("processed: {file_path}".format(file_path=file_path))

                    # detect if there was an error -with extra of cheeze
                    if data != "":
                        processed_count += 1
    except Signal_Caught as e:
        # gracefully shutdown (caught c-c, etc)
        print("Exception: ....shutting down: {e}".format(e=str(e)), file=sys.stderr)
        global STOP_ALL
        STOP_ALL = True

    # report
    print("number of files: {fl}".format(fl=len(files_to_process_list)))
    print("number processed: {processed_count}".format(processed_count=processed_count))

    if STOP_ALL:
        print("There were errors", file=sys.stderr)
        exit(1)

    print("done.")


if __name__ == '__main__':
    main()
