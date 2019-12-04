class Transformer(object):
    def __init__(self, column_names, transformations):
        self.transformations = transformations
        self.num_columns = len(column_names)
        self.columns = dict(zip(column_names, range(0, self.num_columns)))

    def transform_columns(self):
        for transformation in self.transformations:
            self.columns = transformation.transform_columns(self.columns)

    def transform_row(self, row):
        row = row[:self.num_columns]
        if len(row) < self.num_columns:
            raise Exception("row does not have enough columns")
        labelled_row = {}
        new_row = [None]*len(self.columns)
        for transformation in self.transformations:
            for (column, index) in self.columns.items():
                if index >= len(row):
                    labelled_row[column] = new_row[index]
                else:
                    labelled_row[column] = row[index]
            delta = transformation.transform_row(labelled_row)
            for column in delta:
                index = self.columns[column]
                new_row[index] = delta[column]
        return new_row

    def get(self, row, columns):
        this_row = []
        for column in columns:
            index = self.columns[column]
            this_row.append(row[index])
        return this_row
