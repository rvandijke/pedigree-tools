from enum import Enum
from collections import OrderedDict

class Sex(Enum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2

class Individual(object):
    def __init__(self, identifier, family_identifier, father_identifier, mother_identifier, sex, attributes = None):
        self.identifier = identifier
        self.family_identifier = family_identifier
        self.father_identifier = father_identifier
        self.mother_identifier = mother_identifier
        self.sex = sex

        # TODO: Preserve attribute order
        self.attributes = attributes if attributes else OrderedDict()

    def get_attribute_names(self):
        return self.attributes.keys()

    def has_attribute(self, attribute):
        return attribute in self.get_attribute_names()

    def get_attribute(self, name):
        return self.attributes[name]

    def __getattr__(self, name):
        return self.get_attribute(name)

    def __setattr__(self, name, value):
        reserved = ["identifier", "family_identifier", "father_identifier", "mother_identifier", "sex", "attributes"]

        if name in reserved:
            object.__setattr__(self, name, value)
        else:
            attributes = self.attributes
            attributes[name] = value
            object.__setattr__(self, "attributes", attributes)

    def set_attribute(self, name, value):
        self.attributes[name] = value

    def __str__(self):
        return "Individual {} (father {}, mother {})".format(self.identifier, self.father_identifier, self.mother_identifier)
