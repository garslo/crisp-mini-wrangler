from operations import *
from transform import Transformer
import argparse
import csv


columns = {
    "Order Number": 0,
    "Year": 1,
    "Month": 2,
    "Day": 3,
    "Product Number": 4,
    "Product Name": 5,
    "Count": 6,
    "Extra Col1": 7,
    "Extra Col2": 8
}

transformations = [
    Rename(
        from_name="Order Number",
        to_name="OrderID"
    ),
    ParseInt(
        column="OrderID"
    ),
    NewColumn(
        name="OrderDate",
        from_columns=["Year", "Month", "Day"],
        value_format="{}-{}-{}"
    ),
    ParseSimpleDatetime(
        column="OrderDate"
    ),
    Rename(
        from_name="Product Number",
        to_name="ProductId"
    ),
    Rename(
        from_name="Product Name",
        to_name="ProductName"
    ),
    Rename(
        from_name="Count",
        to_name="Quantity"
    ),
    NewColumn(
        name="Unit",
        from_columns=None,
        value_format="kg"
    )
]

transformer = Transformer(columns, transformations)

transformer.transform_columns()

parser = argparse.ArgumentParser()
parser.add_argument("--data-file", default="data.csv", help="csv file containing data to transform")

args = parser.parse_args()
with open(args.data_file, "rb") as fh:
    reader = csv.reader(fh)
    for row in reader:
        transformed = transformer.transform_row(row)
        print transformer.get(transformed, ["OrderID", "OrderDate", "ProductId", "ProductName", "Quantity", "Unit"])
