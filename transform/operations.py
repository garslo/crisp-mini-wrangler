from datetime import datetime
from decimal import Decimal


class Rename(object):
    def __init__(self, from_name, to_name):
        self.__dict__.update(locals())

    def transform_columns(self, columns):
        columns[self.to_name] = columns[self.from_name]
        del(columns[self.from_name])
        return columns

    def transform_row(self, data):
        return {self.to_name: data[self.to_name]}


class Parse(object):
    def __init__(self, column, parser, parser_name):
        self.__dict__.update(locals())

    def transform_columns(self, columns):
        return columns

    def transform_row(self, row):
        try:
            if row[self.column] is None:
                return {}
            return {self.column: self.parser(row[self.column])}
        except:
            raise Exception("expected to parse {} as {}".format(row[self.column], self.parser_name))


class ParseDatetime(Parse):
    def __init__(self, column, date_format):
        self.date_format = date_format
        super(ParseDatetime, self).__init__(column, self.parse, "datetime")

    def parse(self, value):
        return datetime.strptime(value, self.date_format)


class ParseSimpleDatetime(ParseDatetime):
    def __init__(self, column):
        super(ParseSimpleDatetime, self).__init__(column, "%Y-%m-%d")


class ParseInt(Parse):
    def __init__(self, column):
        super(ParseInt, self).__init__(column, int, "int")


# Python's decimal.Decimal is equivalent to BigDecimal
class ParseBigDecimal(ParseInt):
    def __init__(self, column):
        super(ParseInt, self).__init__(column, Decimal, "big_decimal")


# just parse using the identity function
class ParseString(Parse):
    def __init__(self, column):
        super(ParseString, self).__init__(column, lambda x: x, "string")


class NewColumn(object):
    def __init__(self, name, from_columns, value_format):
        self.__dict__.update(locals())

    def transform_columns(self, columns):
        columns[self.name] = len(columns)
        return columns

    def transform_row(self, row):
        if self.from_columns is None or len(self.from_columns) <= 0:
             value = self.value_format
        else:
            args = []
            for column in self.from_columns:
                args.append(row[column])
            value = self.value_format.format(*args)
        return {self.name: value}
