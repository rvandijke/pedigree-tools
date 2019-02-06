from .formats import CSV
from .pedigree import Pedigree

class DataSet:
    def __init__(self, filename, format = CSV):
        self.filename = filename
        self.store = format(filename)
        self.pedigrees = self.__construct_pedigrees()

    def __construct_pedigrees(self):
        pedigrees = []

        for family_identifier in self.store.get_all_families():
            individuals = list(self.store.get_all_individuals(family_identifier))
            pedigrees.append(Pedigree(family_identifier, individuals))

        return pedigrees            

    def __find_pedigree(self, identifier, pedigree = None):
        pedigrees = pedigrees if pedigrees is not None else self.pedigrees

        for pedigree in pedigrees:
            if pedigree.identifier == identifier:
                return pedigree

        return None

    def save(self, filename = None):
        store = type(self.store)(filename) if filename else self.store

        individuals = []

        for pedigree in self.pedigrees:
            individuals = individuals + list(map(lambda node: node.individual, pedigree.nodes))

        store.set_individuals(individuals)
