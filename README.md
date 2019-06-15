[![Build Status](https://drone-github.parasynthetic.dev/api/badges/karlredman/EditFrontMatter/status.svg)](https://drone-github.parasynthetic.dev/karlredman/EditFrontMatter)
[![PyPI version](https://badge.fury.io/py/editfrontmatter.svg)](https://badge.fury.io/py/editfrontmatter)
[![Issues](https://img.shields.io/github/issues/karlredman/EditFrontMatter.svg)](https://github.com/karlredman/EditFrontMatter/issues)
[![License](https://img.shields.io/github/license/karlredman/EditFrontMatter.svg)](https://github.com/karlredman/EditFrontMatter/blob/master/LICENSE)

# Batch Edit Yaml Front Matter

Edit front matter markdown files with Jinja2 templates.

## Description:

This is a `python3` (v3.5.3+) class/module that can be used for batch processing and<br>
editing front matter in markdown files. Front matter is managed via<br>
[Jinja2](http://jinja.pocoo.org/) template processor.

## Features:

* Add / Update / Delete any front matter fields
* Preserves front matter element order via [oyaml](https://github.com/wimglenn/oyaml)
* Uses [Jinja2](http://jinja.pocoo.org/) Templates for configuration and processing:
  * Use Jinja2 filters for complex processing
  * Incrementally process files with multiple templates
* Uses Exceptions around sensitive areas of code
* Examples for implementation:
  1. [Basic usage](https://karlredman.github.io/EditFrontMatter/examples/example1/readme.html)
  2. [Advanced mulit-pass processor](https://karlredman.github.io/EditFrontMatter/examples/example2/readme.html)
  3. [Recursive directory walker that uses multi-threading to edit files](https://karlredman.github.io/EditFrontMatter/examples/example3/readme.html)
* Documented with [Sphinx](https://www.sphinx-doc.org/en/master/) and [hosted on Github](https://karlredman.github.io/EditFrontMatter)

## Documentation:

* [Project Documentation with examples Page](https://karlredman.github.io/EditFrontMatter/)

## Installation:

```sh
pip install editfrontmatter
```

## Dependencies:

```text
editfrontmatter>=0.0.1
Jinja2>=2.10.1
MarkupSafe>=1.1.1
oyaml>=0.9
PyYAML>=5.1
```

## TL;DR Example Usage:

* Original markdown file with yaml front matter ([example1.md](https://github.com/karlredman/EditFrontMatter/blob/master/examples/data/example1.md))

```md
---
title: "EditFrontMatter Class Example 1"
description: "Edit some fields in this front matter"
catagories: [programming, python, markdown]

deleteme: this will be deleted

tags: [front matter, administration, testing]

# comments and spaces will be eliminated (see docs)

author: "Karl N. Redman"
creatordisplayname: "Karl N. Redman"
creatoremail: "karl.redman@example.com"
date: 2019-05-23T17:43:45-05:00
lastmodifierdisplayname: "Karl N. Redman"
lastmodifieremail: "karl.redman@gmail.com"
lastmod: 2019-05-23T17:43:45-05:00
toc: false
type: "page"
hasMath: false
draft: false
weight: 5
---

# EditFontMatter Class Example 1

Edit several fields of front matter.

## Fields affected in this example:

* toc
  * note: uses local template variable
  * pre: false
  * post: true
* draft:
  * note: uses jinja2 filter (callback)
  * pre: false
  * post: true
* hasMath
  * note: uses program variable
  * pre: true
  * post: false
* stuff:
  * note: uses program variable to create field
  * pre: did not exist
  * post: (list) ['one', 'two', 'three']
* deleteme:
  * note: removed from final result
  * pre: this will be deleted
  * post: N/A
```

* Jinja2 template that will update the front matter data of the source markdown file ([template1.j2](https://github.com/karlredman/EditFrontMatter/blob/master/examples/data/template1.j2))

```jinja
{% set toc = "true" %}

toc: {{ toc }}
draft: {{ false | canPublish }}
hasMath: {{ hasMath }}
stuff: {{ addedVariable }}
```

* Python program to edit the markdown file with the Jinja2 template ([example1.py](https://github.com/karlredman/EditFrontMatter/blob/master/examples/example1/example1.py))

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from editfrontmatter import EditFrontMatter
import os


def canPublish_func(val):
    # do some processing....
    return True


def main():

    # generic path - overridden by env var `TEST_DATA_DIR`
    DATA_PATH = "../data/"

    if "TEST_DATA_DIR" in os.environ:
        DATA_PATH = os.path.abspath(os.environ.get("TEST_DATA_DIR")) + "/"

    # set path to input file
    file_path = os.path.abspath(DATA_PATH + "example1.md")

    # initialize `template_str` with template file content
    template_str = ''.join(open(os.path.abspath(DATA_PATH + "template1.j2"), "r").readlines())
    print(template_str)

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

```


* Final Output:

```md
---
title: EditFrontMatter Class Example 1
description: Edit some fields in this front matter
catagories:
- programming
- python
- markdown
tags:
- front matter
- administration
- testing
author: Karl N. Redman
creatordisplayname: Karl N. Redman
creatoremail: karl.redman@example.com
date: 2019-05-23 22:43:45
lastmodifierdisplayname: Karl N. Redman
lastmodifieremail: karl.redman@gmail.com
lastmod: 2019-05-23 22:43:45
toc: true
type: page
hasMath: false
draft: true
weight: 5
stuff:
- one
- two
- three
---

# EditFontMatter Class Example 1

Edit several fields of front matter.

## Fields affected in this example:

* toc
  * note: uses local template variable
  * pre: false
  * post: true
* draft:
  * note: uses jinja2 filter (callback)
  * pre: false
  * post: true
* hasMath
  * note: uses program variable
  * pre: true
  * post: false
* stuff:
  * note: uses program variable to create field
  * pre: did not exist
  * post: (list) ['one', 'two', 'three']
* deleteme:
  * note: removed from final result
  * pre: this will be deleted
  * post: N/A
```
