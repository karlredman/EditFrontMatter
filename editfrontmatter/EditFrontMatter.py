#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Edit Front Matter Module
==============================

.. module:: editfrontmatter

:Synopsis: A thread safe class that uses Jinja2 templating to edit yaml front
    matter within text files. This class is intended to be used for batch processing.

:Platform: Unix, Windows, |python_version|

:Dependencies:

    .. literalinclude:: ../../../requirements.txt
        :language: text

:License: `MIT <https://karlredman.github.io/EditFrontMatter/LICENSE>`_

.. :moduleauthor: `Karl N. Redman <https://karlredman.github.io>`_

:Module Author: `Karl N. Redman <https://karlredman.github.io>`_

:Current Release:
    version: |release|

.. versionadded:: 0.0.1
    Initial Version

"""

# Imports
import re
import traceback
import oyaml as yaml    # preserve yaml dict order
import jinja2


class EditFrontMatter_Exception(Exception):
    """Custom exception handler for EditFrontMatter Project"""
    def __init__(self, msg, exc, *args, **kwargs):
        """
        :Description:
            A custom exception handler for the module. Provides a simplified output message for debugging.

        Args:
            msg (str):
                A custom messsage for the exception caught in the code
            exc (Exception):
                Original exception object from try block

        Returns:
            Exception obj
        """
        msg += "\n    {exc}".format(exc=str(exc))
        template = '\n    Error @ {filename}, Line {linenum} in {funcname}:\n    >>>> {source}'

        for tb_info in traceback.extract_tb(exc.__traceback__):
            filename, linenum, funcname, source = tb_info

            if funcname != '<module>':
                funcname = funcname + '()'
                msg += template.format(
                    filename=filename,
                    linenum=linenum,
                    source=source,
                    funcname=funcname)

        # actual traceback
        # tbe = ''.join(traceback.TracebackException(exc.__class__, exc, exc.__traceback__).format())
        msg = "EditFrontMatter_Exception: {msg}".format(msg=msg)

        super().__init__(msg)


class EditFrontMatter(object):
    """Main Class for module"""
    def __init__(
        self, *,
        file_path=None,
        jinja2_env=jinja2.Environment(loader=None),
        template_str="",
        yaml_delim='---',
        keys_toDelete=[],
        do_readFile=True
    ):
        """Main class for the module. Programmatically Adds / Updates / Deletes yaml \
            front matter elements embedded in text/markdown files.

        Hint:
            This class uses keyword only arguments. Inheriting this class would
            look something like the following::

                class Derived_EditFrontMatter (EditFrontMatter):
                    def __init__(self,**kwargs):
                        EditFrontMatter.__init__(self, **kwargs)

        Args:
            yaml_delim (str):
                yaml file section delimiter (i.e. "---")used to locate the source
                file's embedded yaml section.

            do_readFile (bool):
                allow instantiation without implicit
                :func:`readFile` call


        Attributes:

            self.file_lines (list):
                Lines from the data source file. Must be managed after creating the
                class object if `__init__(do_readFile=False)`

            self.file_path (str):
                Path of source data file. Superfluous if :func:`readFile` is never called

            self.fmatter (yaml):
                [default: empty :class:`dict` if yaml not found]
                Front matter as a yaml object. Set in :func:`readFile`.

            self.yaml_delim (str):
                [default:"---"]
                Front matter delimiter. Can be used to change front matter delimter
                between reading the source file into :attr:`file_lines` and executing
                :func:`dumpFrontMatter`/:func:`writeFile`.

            self.yamlSeperator_pattern (:func:`re.compile`):
                Regex patten for the yaml line delimiter. only used if :func:`readFile` is called

            self.yaml_start (int):
                Beginning of the yaml blob in the original source file. Set in :func:`readFile`

            self.yaml_end (int):
                End of the yaml blob in the origional source file. Set in :func:`readFile`

            self.template_str (str):
                Contains the jinja2 template. Can be manipulated between class
                instantiation and executing :func:`run`

            self.jinja2_env (jinja2.Environment):
                This object can be specified during class instantiation if greater control is required

            self.keys_toDelete (list):
                keys to be deleted from :attr:`fmatter` object. Utilized at the end of the :func:`run` method

        Throws:
            :class:`EditFrontMatter_Exception`
        """

        # critical defaults
        self.yaml_start = None
        self.yaml_end = None
        self.file_empty = True

        # file info
        self.file_path = file_path

        # yaml processing
        self.yaml_delim = yaml_delim
        self.yamlSeperator_pattern = re.compile("^" + self.yaml_delim + ".*")

        # jinja2
        self.template_str = template_str
        self.jinja2_env = jinja2_env
        self.keys_toDelete = keys_toDelete

        # possibly postpone reading the file
        if do_readFile:
            self.readFile()

    def set_yaml_delim(self, delim, *args, **kwargs) -> None:
        """ Set the yaml delimiter and compile it.

        Args:
            delim (str):
                A string to use as a delimiter for finding and editing
                frontmatter in a file.
        """
        self.yaml_delim = delim
        self.yamlSeperator_pattern = re.compile("^" + self.yaml_delim + ".*")

    def readFile(self, file_path=None, *args, **kwargs) -> None:
        """ Read a file into :attr:`file_lines` list (if applicable) and
            seperate the front matter into :attr:`fmatter` yaml object. This
            function resets :attr:`fmatter`.

        Args:
            file_path (str): optional file path

        Hint:
            If *local* `file_path`:`None` and :attr:`file_path`:`None`,
            :attr:`file_lines` should be populated before calling this
            function.

            In the example below, the initialization would fail if
            `do_readFile:True`::

                proc = EditFrontMatter(do_readFile=False)
                proc.file_lines = ''.join(open(RUN_PATH + "example.md", "r").readlines())
                # initialize proc.fmatter and record data position
                proc.readFile()
                ...

        Note:
            If the file source content is empty :attr:`file_empty` is set to
            `True`. This affects :func:`dumpFileData` and :func:`writeFile`
            behavior
        """

        if file_path is None:
            file_path = self.file_path
        else:
            self.file_path = file_path

        # if no file path, user is managing `file_lines` outside of the class
        if self.file_path is not None:
            # with open(file_path, "r") as fo:
            #     self.file_lines = fo.readlines()
            try:
                with open(file_path, "r") as fo:
                    self.file_lines = fo.readlines()
            except IOError as e:
                import sys
                t, v, tb = sys.exc_info()
                raise EditFrontMatter_Exception("self.file_path: {file_path}".
                                                format(file_path=self.file_path), e) from e

        # yaml data re-init / paranoia
        self.yaml_start = None
        self.yaml_end = None
        self.fmatter = None
        self.file_empty = True

        yaml_lines = []
        line_num = 0

        # find the beg. and end separators
        # populate yaml_lines
        for line in self.file_lines:
            if self.yamlSeperator_pattern.match(line):
                if self.yaml_start is None:
                    self.yaml_start = line_num
                elif self.yaml_end is None:
                    self.yaml_end = line_num
                    break
            else:
                if self.yaml_start is None:
                    # no yaml section found
                    self.yaml_start = 0
                    self.yaml_end = 0
                    break
                else:
                    yaml_lines.append(line)
            line_num += 1

        # TODO: start != Note and end == None

        # set fmatter obj -empty dict if yaml not found
        try:
            self.fmatter = yaml.load(''.join(yaml_lines), Loader=yaml.FullLoader) or {}
        except Exception as e:
            # probably a bad file (i.e. missing ending yaml delimiter
            raise EditFrontMatter_Exception("yaml.load error -> self.file_path: {file_path}".
                                            format(file_path=self.file_path), e) from e

    def writeFile(self, file_path=None, *args, **kwargs) -> bool:
        """ Write to arg `file_path`, attr :attr:`file_path`

        Note:
            If the original file source data was empty after a call to
            :func:`readFile`, no attempt is maid to write to the file.

        Args:
            file_path (str):
                optional file path

        Returns:
            * `True` if file was written
            * 'False` if file was **not** written
        """

        if not self.has_source_data():
            return False

        if not file_path:
            file_path = self.file_path

        try:
            with open(file_path, "w+") as fo:
                fo.write(self.dumpFileData())
        except IOError as e:
            raise EditFrontMatter_Exception("write to file -> self.file_path: {file_path}".
                                            format(file_path=self.file_path), e) from e

        return True

    def add_JinjaFilter(self, name, func, *args, **kwargs) -> None:
        """ Add a `Jinja filter <http://jinja.pocoo.org/docs/2.10/templates/#filters>`_
            for setting a jinja2 template variable programmatically through callback.


        Args:
            name (str):
                Jinja template variable name
            func (object):
                callback function that will set `name`


        :Example of implementing a filter for callback:

            Programatically change the value of `draft` field in the source
            document `example1.md` using a Jinja2 filter

            :jinja2 template:

            .. literalinclude:: ../../../examples/data/template1.j2
                :language: jinja

            :mardown file:

            .. literalinclude:: ../../../examples/data/example1.md
                :language: md

            :Example code:

            .. testcode::

                from editfrontmatter import EditFrontMatter
                import os

                # a jinja2 filter callback function
                def canPublish_func(val):
                    # do some processing....
                    return True

                # stringify the template file
                template_str = ''.join(open(os.environ.get("TEST_DATA_DIR") +
                    "template1.j2", "r").readlines())

                # creating object
                obj = EditFrontMatter(file_path = os.environ.get("TEST_DATA_DIR") + "example1.md",
                        template_str = template_str)

                # set `canPublish_func` function for our `draft` field callback using
                # `canPublish` template variable.
                obj.add_JinjaFilter('canPublish', canPublish_func)

                # process the front matter from 'example1.md'. `draft` in the front
                # matter will be set to `true`
                obj.run()

                # print the new file contents (uncomment to see dump)
                # print(obj.dumpFileData())
                """
        self.jinja2_env.filters[name] = func

    def del_JinjaFilter(self, name, *args, **kwargs) -> bool:
        """ Delete a Jinja filter.

        Args:
            name (str):
                filter key

        :returns:
            * True if filter found and deleted
            * False if filter not found
        """
        # TODO: check filter exists (assert?)
        del self.jinja2_env.filters[name]
        return True

    def dumpFrontMatter(self, *args, **kwargs) -> str:
        """ Dump `fmatter` as a string

        Returns:
            :attr:`fmatter` content as a string
        """
        return yaml.dump(self.fmatter, default_flow_style=False)

    def dumpFileData(self, *args, **kwargs) -> str:
        """ Concatenate frontmatter with original content and return as a string.

        Returns:
            * A string formed by the concatination of :attr:`fmatter` and \
                :attr:`file_lines` (if file souce content is **not** empty* **and** yaml was present).

            * An empty string if file source content is empty *or* original \
                yaml was *not* present.

        Hint:
            :attr:`fmatter` and :attr:`file_lines` are still available if needed
            beyond this method. One way of managing this data would be to
            manually prepend yaml front matter to :attr:`file_lines` and rerun
            :func:`readFile` before calling this function again.
        """

        # accomidate for empty file or accomidate for empty front matter
        if self.has_source_data() and self.has_source_yaml():
            return self.yaml_delim + "\n" + self.dumpFrontMatter() + \
                self.yaml_delim + "\n" + ''.join(self.file_lines[self.yaml_end + 1:])
        return ""

    def has_source_yaml(self) -> bool:
        """ Checks if the yaml is empty after a call to :func:`readFile`

        Note:
            This return value does not rely on :attr:`fmatter` since that
            attribute is subject to change once :func:`readFile` is called.

        Returns:
            * `True` if the *original* source file data did have a yaml section

            * `False` if the *original* source file data did *not* have a yaml section
        """
        if self.yaml_start == 0 and self.yaml_end == 0:
            return False
        return True

    def has_source_data(self) -> bool:
        """ Checks if the source file data is empty

        Returns:
            * `True` if the source data content **is** empty
            * `False`  if the source data is **not** empty
        """
        return True if len(self.file_lines) > 0 else False

    def run(self, extraVars_dict={}, *args, **kwargs) -> None:
        """Process the front matter changes and delete previously specified yaml keys.

        Variables to change yaml data are passed as a dictionary argument as `extraVars_dict`.

        Args:
            extraVars_dict (dict):
                key,value pairs to be set or added in the :attr:`fmatter` object.

        Example:
            Call EditFrontMatter.run() with variables to change in
            :attr:`fmatter`::

                proc = EditFrontMatter()
                ...
                proc.run({'hasMath': True, 'addedVariable': ['one', 'two', 'three']})
                ...
        """
        # render jinja2 into yaml
        fmatter_replacement = yaml.load(self.jinja2_env.from_string(
            self.template_str).render(extraVars_dict), Loader=yaml.FullLoader)

        # update the original front matter
        # TODO: exception if fmatter:None
        self.fmatter.update(fmatter_replacement)

        # remove unwanted keys (preserved order from oyaml"
        for key in self.keys_toDelete:
            if key in self.fmatter:
                del self.fmatter[key]
