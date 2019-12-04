from transform.operations import *
from transform.transformer import Transformer
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--data-file", default="data.csv", help="csv file containing data to transform")
parser.add_argument("--output-file", default="out.dat", help="raw dump of transformed rows in python-ish syntax")
parser.add_argument("--spec-file", default="spec.py", help="file containing transformation spec")
args = parser.parse_args()

with open(args.spec_file, "r") as fh:
    data = eval(compile(fh.read(), args.spec_file, "eval"))

out_file = open(args.output_file, "w")

def dump_row(row):
    out_file.write(str(row))
    out_file.write("\n")

transformer = Transformer(data["column_names"], data["transformations"])
transformer.transform_columns()

with open(args.data_file, "rb") as fh:
    reader = csv.reader(fh)
    for row in reader:
        try:
            transformed = transformer.transform_row(row)
            dump_row(transformer.get(transformed, data["output_columns"]))
        except Exception as e:
            print "Could not transform row={} reason='{}'".format(str(row), str(e))

out_file.close()
