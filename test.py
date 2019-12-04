import unittest
from transform.operations import *
from transform.transformer import *
from datetime import datetime


class TestRename(unittest.TestCase):
    def setUp(self):
        self.initial_columns = {"foo":0, "baz":1}

    def test_column_gets_renamed(self):
        rename = Rename("foo", "bar")
        result = rename.transform_columns({"foo":0, "baz":1})
        self.assertTrue("bar" in result)
        self.assertTrue("foo" not in result)
        self.assertEqual(self.initial_columns["foo"], result["bar"])


class TestNewColumn(unittest.TestCase):
    def setUp(self):
        self.initial_columns = {"foo":0, "baz":1}

    def test_column_gets_added(self):
        new_column = NewColumn("new_column", None, "constant")
        result = new_column.transform_columns(self.initial_columns)
        self.assertTrue("new_column" in result)

    def test_rows_get_values_added_to_new_columns(self):
        new_column = NewColumn("new_column", None, "constant")
        row = {
            "foo": "first",
            "baz": "second"
        }
        new_row = new_column.transform_row(row)
        self.assertEqual(new_row["new_column"], "constant")

    def test_we_can_use_other_column_values_to_format_new_column(self):
        new_column = NewColumn("new_column", ["foo", "baz"], "foo={} baz={}")
        row = {
            "foo": "first",
            "baz": "second"
        }
        new_row = new_column.transform_row(row)
        self.assertEqual(new_row["new_column"], "foo=first baz=second")


class TestParse(unittest.TestCase):
    def setUp(self):
        self.initial_columns = {"foo":0, "baz":1}

    def test_we_can_parse_ints(self):
        parse_int = ParseInt("foo")
        row = {
            "foo": "1",
            "baz": "second"
        }
        new_row = parse_int.transform_row(row)
        self.assertEqual(new_row["foo"], 1)


    def test_we_can_parse_simple_dates(self):
        parse_date = ParseSimpleDatetime("foo")
        row = {
            "foo": "2019-12-3",
            "baz": "second"
        }
        new_row = parse_date.transform_row(row)
        self.assertEqual(new_row["foo"], datetime(2019, 12, 3, 0, 0))


class TestTransformer(unittest.TestCase):
    def setUp(self):
        self.initial_columns = ["foo", "baz"]

    def test_we_can_do_column_transformations(self):
        transformations = [Rename("foo", "bar"), Rename("baz", "zip")]
        transformer = Transformer(self.initial_columns, transformations)
        transformer.transform_columns()
        self.assertEqual(
            transformer.columns,
            {"bar": 0, "zip": 1}
        )

    def test_we_can_do_row_transformations(self):
        transformations = [NewColumn("new", ["foo", "baz"], "{} {} new value")]
        transformer = Transformer(
            self.initial_columns,
            transformations
        )
        transformer.transform_columns()
        row = transformer.transform_row([1,2])
        self.assertEqual(row[2], "1 2 new value")

    def test_crisp_transformation(self):
        transformations = [
            Rename("Order Number", "OrderID"),
            ParseInt("OrderID"),
            NewColumn("OrderDate", ["Year", "Month", "Day"], "{}-{}-{}"),
            ParseSimpleDatetime("OrderDate"),
            Rename("Product Number", "ProductId"),
            ParseString("ProductId"),
            Rename("Product Name", "ProductName"),
            Rename("Count", "Quantity"),
            ParseBigDecimal("Quantity"),
            NewColumn("Unit", None, "kg")
        ]

        columns = [
            "Order Number",
            "Year",
            "Month",
            "Day",
            "Product Number",
            "Product Name",
            "Count",
            "Extra Col1",
            "Extra Col2"
        ]

        columns_we_want = [
            "OrderID",
            "OrderDate",
            "ProductId",
            "ProductName",
            "Quantity",
            "Unit"
        ]

        rows = [
            ["1000","2018","1","1","P-10001","Arugola","5","250.50","Lorem","Ipsum",""],
            ["1001","2017","12","12","P-10002","Iceberg lettuce","500.00","Lorem","Ipsum"]
        ]

        transformer = Transformer(columns, transformations)
        transformer.transform_columns()
        result = []

        transformed = transformer.transform_row(rows[0])
        result = transformer.get(transformed, columns_we_want)
        self.assertEqual(
            result,
            [1000, datetime(2018, 1, 1, 0, 0), 'P-10001', 'Arugola', Decimal('5'), 'kg']
        )

        transformed = transformer.transform_row(rows[1])
        result = transformer.get(transformed, columns_we_want)
        self.assertEqual(
            result,
            [1001, datetime(2017, 12, 12, 0, 0), 'P-10002', 'Iceberg lettuce', Decimal('500.00'), 'kg']
        )


if __name__ == "__main__":
    unittest.main()
