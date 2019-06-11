# EditFrontMatter: Example 3 Readme

Example 3 is a multi threaded program that recursively walks a directory structure and edits the front matter in each valid file found (based on file extension).

While it might seem a bit silly for a file I/O program to use multiple threads, this example demonstrates the thread worthiness of the module.  In addition, this example provides a basic skeleton for situations where one might use a database to provide data for the front matter or make remote calls to a server for file content -in which case threading makes sense.

Admittedly, this example is a bit long and non modularized. It was a conscious decision to provide a top down, non modularized, code base to make it easier to follow the code logic.

The documentation for the program can be found [here](https://karlredman.github.io/EditFrontMatter/examples/example3/example3.html).

## Program flow:

* Walk directory trees from an inclusion list and gatherers paths of files to edit
* Ignore directories from an exclusion list
* Creates one thread per file being edited (up to `max_threads`)
* Edits the contents of each file
* Throws exceptions or prints error messages as needed
* reports back to the user

## Constraints:

* Will edit files that:
  * contain valid yaml but no content
  * contain valid yaml with content
* Won't edit files that:
  * are empty
  * contain invalid yaml
    * that does not start on first line
    * that is missing a begenning or ending section delimiter
    * that is missing yaml
* (Constraints can be overridden as needed)

## Running the program:

* install dependencies

* run from anywhere with the environment variable:
```
TEST_DATA_DIR="./data/" example3/example3.py
```

* Note: The example program does not alter files by default

## Example Input / Output

The example input can be found in the [example data structure directory](https://github.com/karlredman/EditFrontMatter/tree/master/examples/data/example_dir_structure). The input files represent the various success and failure conditions of the EditFrontMatter module.

* File definitions:
  * example3.md
    * Success: Standard file similar to example1.md
  * example3a.md
    * Error: empty file
  * example3b.md
    * Error: file with content but no yaml
  * example3c.md
    * Success: with yaml but no content
  * example3d.md
    * Error: with no yaml end delimiter
  * example3e.md
    * Error: yaml section not at top of file

* Directory structure:

```sh
example_dir_structure/
├── a
│   ├── b
│   │   ├── b1
│   │   │   ├── example3d.md
│   │   │   └── example3.md
│   │   ├── b2
│   │   │   ├── example3e.md
│   │   │   └── example3.md
│   │   └── example3.md
│   ├── c
│   │   ├── b
│   │   │   ├── b1
│   │   │   │   └── example3.md
│   │   │   ├── b2
│   │   │   │   ├── example3d.md
│   │   │   │   └── example3.md
│   │   │   └── example3.md
│   │   ├── c1
│   │   │   ├── example3c.md
│   │   │   └── example3.md
│   │   ├── c2
│   │   │   ├── example3b.md
│   │   │   └── example3.md
│   │   └── example3.md
│   ├── example3a.md
│   └── example3.md
├── example3a.md
├── example3b.md
├── example3c.md
├── example3d.md
├── example3e.md
└── example3.md
```

* Output Example:

```sh
$ TEST_DATA_DIR="../data/" ./example3.py
Error (exception): @Derived_EditFrontMatter.__init__(): /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3d.md
Error: No source yaml: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3e.md
Error: No source data: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3a.md
Error: No source yaml: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3b.md
Error: No source data: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/example3a.md
Error (exception): @Derived_EditFrontMatter.__init__(): /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/b/b1/example3d.md
Error: No source yaml: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/b/b2/example3e.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/b/example3.md
Error: No source yaml: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/c/c2/example3b.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/b/b2/example3e.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3d.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/example3.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3a.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/b/b1/example3.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3b.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/c/c1/example3c.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/example3a.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/b/b1/example3d.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3c.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/c/c1/example3.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/c/example3.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/b/b2/example3.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/c/c2/example3.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/example3e.md
processed: /home/karl/Scratch/EditFrontMatter/examples/data/example_dir_structure/a/c/c2/example3b.md
number of files: 18
number processed: 10
done.
```
