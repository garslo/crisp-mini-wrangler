class Rename(object):
    def __init__(self, from_name, to_name):
        self.__dict__.update(locals())

    def transform_columns(self, columns):
        columns[self.to_name] = columns[self.from_name]
        # del(columns[self.from_name])
        return columns

    def transform_row(self, data):
        return data
