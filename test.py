import unittest
from operations import *
from transform import *
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
        self.initial_columns = {"foo":0, "baz":1}

    def test_we_can_do_column_transformations(self):
        transformations = [Rename("foo", "bar"), Rename("baz", "zip")]
        transformer = Transformer(self.initial_columns, [], transformations)
        transformer.transform_columns()
        self.assertEqual(
            transformer.columns,
            {"bar": 0, "zip": 1}
        )

    def test_we_can_do_row_transformations(self):
        transformations = [NewColumn("new", None, "new value")]
        transformer = Transformer(
            self.initial_columns,
            [[1, 2], [3, 4]],
            transformations
        )
        transformer.transform_columns()
        transformer.transform_rows()
        self.assertEqual(
            transformer.rows,
            [[1, 2, "new value"], [3, 4, "new value"]],
        )

    def test_crisp_transformation(self):
        transformations = [
            Rename("Order Number", "OrderID"),
            NewColumn("OrderDate", ["Year", "Month", "Day"], "{}-{}-{}"),
            ParseSimpleDatetime("OrderDate"),
            Rename("Product Number", "ProductId"),
            Rename("Product Name", "ProductName"),
            Rename("Count", "Quantity"),
            NewColumn("Unit", None, "kg")
        ]

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

        rows = [
            ["1", "2019", "12", "2", "443", "Food Thing", "88", "asdjkfd", "al;ksdfj"],
            ["2", "2019", "12", "5", "444", "Food Thing 2", "884", "asdjkfd", "al;ksdfj"]
        ]

        transformer = Transformer(columns, rows, transformations)
        transformer.transform_columns()
        result = []
        for row in rows:
            result.append(transformer.transform_row(row))

        # row = transformer.get(row, columns=["OrderID", "OrderDate", "ProductId", "ProductName", "Quantity", "Unit"])



if __name__ == "__main__":
    unittest.main()
