from datetime import datetime


class Rename(object):
    def __init__(self, from_name, to_name):
        self.__dict__.update(locals())

    def transform_columns(self, columns):
        columns[self.to_name] = columns[self.from_name]
        del(columns[self.from_name])
        return columns

    def transform_row(self, data):
        return data


class Parse(object):
    def __init__(self, column, parser):
        self.__dict__.update(locals())

    def transform_columns(self, columns):
        return columns

    def transform_row(self, row):
        try:
            row[self.column] = self.parser(row[self.column])
            return row
        except Exception as e:
            return row


class ParseDatetime(Parse):
    def __init__(self, column, date_format):
        self.date_format = date_format
        super(ParseDatetime, self).__init__(column, self.parse)

    def parse(self, value):
        return datetime.strptime(value, self.date_format)


class ParseSimpleDatetime(ParseDatetime):
    def __init__(self, column):
        super(ParseSimpleDatetime, self).__init__(column, "%Y-%m-%d")


class ParseInt(Parse):
    def __init__(self, column):
        super(ParseInt, self).__init__(column, int)


class NewColumn(object):
    def __init__(self, name, from_columns, value_format):
        self.__dict__.update(locals())

    def transform_columns(self, columns):
        columns[self.name] = len(columns)
        return columns

    def transform_row(self, row):
        if self.from_columns is None or len(self.from_columns) <= 0:
            row[self.name] = self.value_format
        else:
            args = []
            for column in self.from_columns:
                args.append(row[column])
            row[self.name] = self.value_format.format(*args)
        return row
