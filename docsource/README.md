# Sphinx RTD boilerplate Readme

## Running, Building and Testing

* switch to `python v3.68+`

```
cd <project_root>
pyenv local 3.6.8
```

* if not already, add virtualenv

```
virtualenv venv
# activate the virtual env
. ./venv/bin/activate
```

### Running example apps

* install runtime requirements

```
cd <project_root>
pip install -r requirements.txt
```

* run examples

```
TEST_DATA_DIR="./examples/data/" ./examples/example1/example1.py
TEST_DATA_DIR="./examples/data/" ./examples/example2/example2.py
TEST_DATA_DIR="./examples/data/" ./examples/example3/example3.py
```

### Building documentation

* install build requirements

```
cd <project_root>/docsource
pip install -r requirements.txt
```

* build docs for github pages / review

```
# the path is really not necessary
make clean; TEST_DATA_DIR="../examples/data/" make github
```

* preview the documentation
  * open browser `file://<project_root>/docs/build/index.html`

### Testing documentation examples via `doctest`

* `doctest` will output test results to the `cli`

```
cd <project_root>/docsource
# run doctest (with custom path)
make clean; TEST_DATA_DIR="../examples/data/" make doctest
```
