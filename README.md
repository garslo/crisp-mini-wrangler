<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Quickstart](#quickstart)
- [Data and Transformation Specification](#data-and-transformation-specification)
- [Brief Architectural Overview](#brief-architectural-overview)
    - [Data and Transformation Specification](#data-and-transformation-specification-1)
    - [Data Transformations](#data-transformations)
    - [Running and Collecting](#running-and-collecting)

<!-- markdown-toc end -->


# Quickstart

To transform `data.csv` with the default specifications found in
`spec.py`, simply run

```
$ python main.py
```

the transformed results will exist in `out.dat`.

In more detail:

```
$ python --version
Python 2.7.10
$ python -m unittest -v test
test_column_gets_added (test.TestNewColumn) ... ok
test_rows_get_values_added_to_new_columns (test.TestNewColumn) ... ok
test_we_can_use_other_column_values_to_format_new_column (test.TestNewColumn) ... ok
test_we_can_parse_ints (test.TestParse) ... ok
test_we_can_parse_simple_dates (test.TestParse) ... ok
test_column_gets_renamed (test.TestRename) ... ok
test_crisp_transformation (test.TestTransformer) ... ok
test_we_can_do_column_transformations (test.TestTransformer) ... ok
test_we_can_do_row_transformations (test.TestTransformer) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.003s

OK
$ python main.py -h
usage: main.py [-h] [--data-file DATA_FILE] [--output-file OUTPUT_FILE] [--spec-file SPEC_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --data-file DATA_FILE
                        csv file containing data to transform (default: data.csv)
  --output-file OUTPUT_FILE
                        raw dump of transformed rows in python-ish syntax (default: out.dat)
  --spec-file SPEC_FILE
                        file containing transformation spec (default: spec.py)
$ python main.py --data-file ./data.csv --spec-file ./spec.py
Could not transform row=['lkdsjaf'] reason='row does not have enough columns'
Could not transform row=['1001', '2017', '1c', '12', 'P-10002', 'Iceberg lettuce', '500.00', 'Lorem', 'Ipsum'] reason='expected to parse 2017-1c-12 as datetime'
Could not transform row=[] reason='row does not have enough columns'
Could not transform row=['1001', '2017', '12', '12', 'P-10002', 'Iceberg lettuce', '500.004f', 'Lorem', 'Ipsum'] reason='expected to parse 500.004f as big_decimal'
$ cat out.dat
[1000, datetime.datetime(2018, 1, 1, 0, 0), 'P-10001', 'Arugola', Decimal('5'), 'kg']
[1001, datetime.datetime(2017, 12, 12, 0, 0), 'P-10002', 'Iceberg lettuce', Decimal('500.00'), 'kg']
```

This application has no external dependencies.

# Data and Transformation Specification

The file given by `--spec-file` contains a python-syntax dictionary
that outlines the data columns (`column_names`), transformations on
them (`transformations`), and desired output columns
(`output_columns`). See `spec.py` for an example.

The available transformations are:

- `Rename(from_name, to_name)`
- `ParseSimpleDatetime(column)`
- `ParseInt(column)`
- `ParseBigDecimal(column)`
- `ParseString(column)`
- `NewColumn(name, from_columns, value_format)`

Of those, the only transformation requiring explanation is
`NewColumn`. `from_columns` must be a list of column names (or empty
or `None`) the column's values will be derived from, and
`value_format` is a position-based format suitable for passing into
the
[`format()`](https://docs.python.org/2.7/library/functions.html#format)
method.

# Brief Architectural Overview

## Data and Transformation Specification

The data and desired transformations on them are described in a
python-based DSL. It's a bit clever and brings with it all that
entails. I would use yaml or json for a more robust solution, however
the former requires external dependencies and the latter is more
verbose than I wanted.

## Data Transformations

Each transformation is implemented by its own class in
`transformations/operations.py`. Each transformation can operate on
the dataset's columns, rows, or both.

The set of transformations is orchestrated by the `Transformer` class
found in `transformations/transfomer.py`. I'm not completely happy
with the `transform_row()` method as it creates a dummy `new_row`
filled with `None`s. These `Nones` tend to pop up in annoying
spots. In a real project I would like to tidy this up.

## Running and Collecting

Once the metadata and transformations are gathered we process the
rows. We do this line-by-line to prevent out-of-memory issues when/if
the dataset is enormous.

A line that can't be processed gets turned into an exception. The very
top-level loop in `main.py` is responsible for capturing and logging
this exception/bad row. In a more robust solution we'd handle the
problem inside the `Transformer`, perhaps shuffling the invalid lines
into a file somewhere.

The end-use of this transformed data is unspecified and so we simply
dump it out into a file as a sequence of python lists.
