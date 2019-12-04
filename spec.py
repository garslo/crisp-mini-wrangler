{
    "column_names": [
        "Order Number",
        "Year",
        "Month",
        "Day",
        "Product Number",
        "Product Name",
        "Count",
        "Extra Col1",
        "Extra Col2"
    ],

    "output_columns": [
        "OrderID",
        "OrderDate",
        "ProductId",
        "ProductName",
        "Quantity",
        "Unit"
    ],

    "transformations": [
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
}
