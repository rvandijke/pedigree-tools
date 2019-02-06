from .store import Store
from ..models import Individual
from ..models import Sex
import csv
import os.path
from collections import OrderedDict

class CSV(Store):
    @staticmethod
    def default_column_names():
        return {
            Store.Column.FAMILY_ID: "FID",
            Store.Column.INDIVIDUAL_ID: "IndivID",
            Store.Column.FATHER_ID: "FathID",
            Store.Column.MOTHER_ID: "MothID",
            Store.Column.SEX: "Sex 1=m / 2=v"
        }

    def __init__(self, filename, column_names = None):
        self.column_names = column_names if column_names else CSV.default_column_names()
        self.filename = filename

        if os.path.isfile(filename):
            fieldnames = self.get_fieldnames()
            self.individuals = list(map(lambda row: self.__deserialize(row, fieldnames.copy()), self.__get_all_rows()))
            self.individuals = list(filter(lambda individual: len(individual.identifier) > 0, self.individuals))

    def get_fieldnames(self):
        file = open(self.filename, "r", encoding="utf-8-sig")
        dialect = self._get_dialect_from_file(file)
        fieldnames = list(filter(lambda fieldname: len(fieldname) > 0, csv.DictReader(file, dialect=dialect).fieldnames))
        file.close()

        return fieldnames + ["original_row"]

    def _get_dialect_from_file(self, file):
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(file.read(1024))
        file.seek(0)

        return dialect

    def number_of_families(self):
        return len(self.get_all_families())

    def get_all_families(self):
        families = OrderedDict()

        for individual in self.individuals:
            families[individual.family_identifier] = "0"

        return families.keys()

    def number_of_individuals(self):
        return len(self.individuals)

    def get_all_individuals(self, family_identifier):
        individuals = []
        for individual in self.individuals:
            if individual.family_identifier == family_identifier:
                individuals.append(individual)
                
        return individuals

    def get_individual(self, index):
        return [individual for idx, individual in enumerate(self.individuals) if idx == index][0]

    def set_individuals(self, individuals):
        self.individuals = sorted(individuals, key=lambda k: k.get_attribute("original_row"))

        if len(individuals) == 0:
            ## TODO, clear file
            return

        fieldnames = [
            self.column_names[Store.Column.FAMILY_ID],
            self.column_names[Store.Column.INDIVIDUAL_ID],
            self.column_names[Store.Column.FATHER_ID],
            self.column_names[Store.Column.MOTHER_ID],
            self.column_names[Store.Column.SEX]
        ]

        fieldnames = fieldnames + list(individuals[0].get_attribute_names())
        
        if "original_row" in fieldnames:
            fieldnames.remove("original_row")

        file = open(self.filename, "w", encoding="utf-8-sig")

        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()

        rows = map(lambda individual: self.__serialize(individual), self.individuals)
        writer.writerows(rows)
        file.close()

    def __get_all_rows(self):
        file = open(self.filename, "r", encoding="utf-8-sig")

        dialect = self._get_dialect_from_file(file)
        reader = csv.DictReader(file, dialect=dialect)
        rows = list(reader)

        i = 2
        for row in rows:
            row["original_row"] = i
            i = i + 1

        file.close()
        return rows
        
    def __deserialize(self, row, fieldnames):
        # filter empty keys out
        row = {key:value for (key, value) in row.items() if key}

        identifier = row[self.column_names[Store.Column.INDIVIDUAL_ID]]
        family_identifier = row[self.column_names[Store.Column.FAMILY_ID]]
        father_identifier = row[self.column_names[Store.Column.FATHER_ID]]
        mother_identifier = row[self.column_names[Store.Column.MOTHER_ID]]
        sex = row[self.column_names[Store.Column.SEX]]

        if sex == "1":
            sex = Sex.MALE
        elif sex == "2":
            sex = Sex.FEMALE
        else:
            sex = Sex.UNKNOWN

        for key, value in self.column_names.items():
            fieldnames.remove(value)

        attributes = OrderedDict()
        for key in fieldnames:
            attributes[key] = row[key]

        individual = Individual(
            identifier,
            family_identifier,
            father_identifier,
            mother_identifier,
            sex,
            attributes
        )

        return individual

    def __serialize(self, individual):
        data = dict()
        data[self.column_names[Store.Column.FAMILY_ID]] = individual.family_identifier
        data[self.column_names[Store.Column.INDIVIDUAL_ID]] = individual.identifier
        data[self.column_names[Store.Column.FATHER_ID]] = individual.father_identifier
        data[self.column_names[Store.Column.MOTHER_ID]] = individual.mother_identifier

        sex = "0"
        if individual.sex == Sex.MALE:
            sex = "1"
        if individual.sex == Sex.FEMALE:
            sex = "2"

        data[self.column_names[Store.Column.SEX]] = sex

        data.update(individual.attributes)
        del data["original_row"]

        return data
