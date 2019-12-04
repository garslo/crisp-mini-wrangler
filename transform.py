class Transformer(object):
    def __init__(self, columns, transformations):
        self.__dict__.update(locals())

    def transform_columns(self):
        for transformation in self.transformations:
            self.columns = transformation.transform_columns(self.columns)

    def transform_row(self, row):
        labelled_row = {}
        new_row = [None]*len(self.columns)
        for transformation in self.transformations:
            for (column, index) in self.columns.items():
                if index >= len(row):
                    labelled_row[column] = new_row[index]
                else:
                    labelled_row[column] = row[index]
            transformed_row = transformation.transform_row(labelled_row)
            for column in transformed_row:
                if transformed_row[column] is not None:
                    index = self.columns[column]
                    new_row[index] = transformed_row[column]
        return new_row

    def get(self, row, columns):
        this_row = []
        for column in columns:
            index = self.columns[column]
            this_row.append(row[index])
        return this_row
