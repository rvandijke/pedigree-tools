class Node:
    def __init__(self, individual, father, mother, children = None):
        self.individual = individual
        self.father = father
        self.mother = mother
        self.children = children if children else []

    def get_yob(self):
        if self.individual is None:
            return None

        try:
            yob = int(float(self.individual.Yob))
        except:
            print("Cannot convert {} for individual {} of family {} to a float".format(self.individual.Yob, self.individual.identifier, self.individual.family_identifier))
            return 0
            
        return yob if yob > 0 else None

    @staticmethod
    def get_oldest(nodes):
        if len(nodes) == 0:
            return None

        oldest = None
        oldest_yob = 5000
        for node in nodes:
            yob = node.get_yob()
            if yob is None:
                # found node with unknown Yob, skip this one
                continue

            if yob < oldest_yob:
                oldest = node
                oldest_yob = yob
            
        return oldest

    @staticmethod
    def get_children(nodes):
        children = []

        for node in nodes:
            children = children + node.children

        return list(children)

    def get_parents(self):
        parents = []
        if self.father:
            parents.append(self.father)
        if self.mother:
            parents.append(self.mother)

        return parents

    def get_grand_parents(self):
        parents = self.get_parents()
        grand_parents = []

        for parent in parents:
            grand_parents = grand_parents + parent.get_parents()

        return grand_parents

    def get_parents_siblings(self):
        parents = self.get_parents()
        grand_parents = self.get_grand_parents()

        if len(grand_parents) == 0 or len(parents) == 0:
            return []

        parents_siblings = set()
        for grand_parent in grand_parents:
            parents_siblings.update(grand_parent.children)

        if len(parents_siblings) == 0:
            return []
        
        for parent in parents:
            if parent in parents_siblings:
                parents_siblings.remove(parent)

        return list(parents_siblings)

    def get_siblings(self):
        children = list(self.children)

        parents = set()
        for child in children:
            parents.update(child.get_parents())

        if self in parents:
            parents.remove(self)

        siblings = set()
        for parent in parents:
            for parent in parent.get_parents():
                siblings.update(parent.children)

        return list(siblings)

    def get_cousins(self):
        parents_siblings = self.get_parents_siblings()

        if len(parents_siblings) == 0:
            return []

        cousins = set()
        for parent_sibling in parents_siblings:
            cousins.update(parent_sibling.children)

        return list(cousins)

