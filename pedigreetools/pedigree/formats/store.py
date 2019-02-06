from enum import Enum

class Store:
    class Column(Enum):
        FAMILY_ID = 1
        INDIVIDUAL_ID = 2
        FATHER_ID = 3
        MOTHER_ID = 4
        SEX = 5

    @staticmethod
    def default_column_names():
        return []

    def __init__(self, filename):
        self.filename = filename

    def open(self):
        pass

    def close(self):
        pass

    def get_fieldnames(self):
        return []

    def number_of_families(self):
        return -1

    def get_all_families(self):
        return []

    def number_of_individuals(self):
        return -1

    def get_all_individuals(self, family_identifier):
        return []

    def get_individual(self, index):
        return None

    def set_individuals(self, individual):
        pass