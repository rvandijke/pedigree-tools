from pedigreetools import pedigree
from pedigreetools.utils.cli import CLIOperation

class DeriveYOBsOperation(CLIOperation):
    class Rule:
        def __init__(self, title, f):
            self.title = title
            self.f = f

    def __init__(self, calculate_everything = False):
        CLIOperation.__init__(self)
        self.calculate_everything = calculate_everything

    def title(self):
        if self.calculate_everything:
            return "Derive YOBs (Calculate Everything)"
        
        return "Derive YOBs"

    def description(self):
        if self.calculate_everything:
            return "Derive Unknown Year of Births, fill in all the blanks"

        return "Derive Unknown Years of Births"

    def execute(self, context):
        rules = self.__rules()
        pedigrees = context.dataset.pedigrees

        for pedigree in pedigrees:
            self.add_text("------------------------------------")
            attributes = self.__get_diag_attributes(pedigree)
            self.add_text("Found the following diagnose attributes for {}".format(pedigree.identifier))
            self.add_text(",".join(attributes), red = True)

            def should_consider_node(node):
                if self.calculate_everything:
                    return True
                
                for attribute in attributes:
                    if node.individual.get_attribute(attribute) != "0":
                        return True

                return False

            count = self.__count_missing_yobs(pedigree, should_consider_node)
            self.add_text("")
            self.add_text("Family {} has {} missing yobs".format(pedigree.identifier, str(count)))
            self.add_text("Deriving YOBs for {}".format(pedigree.identifier))

            derived_yobs = dict()
            iteration_count = 0

            while True:
                iteration_count = iteration_count + 1
                count = self.__count_missing_yobs(pedigree, should_consider_node)
                yobs = self.__derive_yobs(pedigree, rules, should_consider_node)

                self.__merge_yobs(yobs, pedigree, iteration_count)
                new_count = self.__count_missing_yobs(pedigree, should_consider_node)

                derived_yobs.update(yobs)

                if count == new_count or new_count == 0:
                    for (identifier, yob) in derived_yobs.items():
                        self.add_text("Derived YOB {} for individual {}".format(yob[0], identifier))

                    self.add_text("Done! Family {} now has {} missing yobs".format(pedigree.identifier, str(new_count)), green = True)
                    self.add_text("")
                    break

        self.ask_input("Press return to continue")
        return True

    def __get_diag_attributes(self, pedigree):
        attributes = pedigree.nodes[0].individual.get_attribute_names()

        return sorted(list(filter(lambda attribute: attribute.startswith("diag"), attributes)))

    def __count_missing_yobs(self, pedigree, condition):
        count = 0

        for node in pedigree.nodes:
            if condition(node) and node.individual.has_attribute("Yob") and node.get_yob() is None:
                count = count + 1

        return count

    def __derive_yobs(self, pedigree, rules, condition = None):
        yobs = dict()

        for node in pedigree.nodes:
            if condition(node) and node.get_yob() is None:
                result = self.__derive_yob(node, rules)

                if result:
                    yobs[node.individual.identifier] = result

        return yobs

    def __merge_yobs(self, yobs, pedigree, iteration_count = 1):
        for node in pedigree.nodes:
            if node.individual.identifier in yobs:
                result = yobs[node.individual.identifier]
                if result:
                    (yob, rule, description) = result

                    current_iteration_count = int(node.individual.YobDerived) if node.individual.has_attribute("YobDerived") else 0

                    if iteration_count >= current_iteration_count:
                        node.individual.Yob = yob
                        node.individual.YobDerivedHow = rule.title
                        node.individual.YobDerivedDescription = description
                        node.individual.YobDerived = str(iteration_count)
            else:
                current_iteration_count = int(node.individual.YobDerived) if node.individual.has_attribute("YobDerived") else 0

                if current_iteration_count == 0:
                    node.individual.YobDerived = str(0)
                    node.individual.YobDerivedHow = ""
                    node.individual.YobDerivedDescription = ""

    def __rules(self):
        rules = [
            DeriveYOBsOperation.Rule("By siblings", self.__by_siblings),
            DeriveYOBsOperation.Rule("By oldest child (mother side)", self.__by_oldest_child),
            DeriveYOBsOperation.Rule("By mother", self.__by_mother),
            DeriveYOBsOperation.Rule("By father", self.__by_father),
            DeriveYOBsOperation.Rule("By grand parents", self.__by_grand_parents),
            DeriveYOBsOperation.Rule("By oldest grand child", self.__by_oldest_grand_child),
            DeriveYOBsOperation.Rule("By cousins", self.__by_cousins),
            DeriveYOBsOperation.Rule("By generations", self.__by_generations)
        ]
        return rules

    def __derive_yob(self, node, rules):
        for rule in rules:
            result = rule.f(node)

            if result:
                (yob, description) = result
                return tuple((str(yob), rule, description))

        return None

    def __by_siblings(self, node):
        # 1. als yob broers/zussen bekend (zelfde MothID), dan gemiddelde yob van broers/zussen
        siblings = list(node.mother.children) if node.mother else []

        if not siblings or len(siblings) == 0:
            return None

        siblings.remove(node)

        yob = 0
        count = 0

        siblings_considered = set()
        for sibling in siblings:
            sibling_yob = sibling.get_yob() if sibling.get_yob() else None
            if sibling_yob:
                siblings_considered.add(sibling)
                yob = yob + sibling_yob
                count = count + 1

        if count > 0:
            yob = yob / count
            sibling_ids = list(map(lambda n: n.individual.identifier, siblings_considered))
            description = "By siblings, siblings used: {}".format(",".join(sibling_ids))
            return tuple((int(yob), description))

        return None

    def __by_mother(self, node):
        # 2. als yob moeder bekend, yob moeder + 25

        if node.mother is None:
            return None

        yob = node.mother.get_yob() if node.mother.get_yob() else None

        description = "By mother {} + 25".format(node.mother.individual.identifier)
        return tuple((yob + 25, description)) if yob else None

    def __by_oldest_child(self, node):
        # 3. als yob kind bekend, yob (oudste) kind - 25
        
        oldest = pedigree.Node.get_oldest(node.children)

        if oldest is None:
            return None

        description = "By oldest child {} - 25".format(oldest.individual.identifier)
        return tuple((oldest.get_yob() - 25, description)) if oldest.get_yob() else None

    def __by_father(self, node):
        # 4. als yob vader bekend, yob vader +25
        if node.father is None:
            return None

        yob = node.father.get_yob() if node.father.get_yob() else None

        description = "By father {} + 25".format(node.father.individual.identifier)
        return tuple((yob + 25, description)) if yob else None

    def __by_grand_parents(self, node):
        # 5. als yob grootouders bekend yob grootouders + 50

        grand_mother = node.mother.mother if node.mother else None
        if grand_mother:
            yob = grand_mother.get_yob()

            if yob:
                description = "By grand mother {} + 50".format(grand_mother.individual.identifier)
                return tuple((yob + 50, description))

        grand_father = node.father.father if node.father else None
        if grand_father:
            yob = grand_father.get_yob()

            if yob:
                description = "By grand father {} + 50".format(grand_father.individual.identifier)
                return tuple((yob + 50, description))

        return None

    def __by_oldest_grand_child(self, node):
        # 6. als yob kleinkinderen bekend, yob (oudste) kleinkind - 50
        children = list(node.children)
        oldest = pedigree.Node.get_oldest(children)

        grand_children = []

        if oldest is None:
            grand_children = pedigree.Node.get_children(children)
        else:
            grand_children = pedigree.Node.get_children([oldest])

        oldest_grand_child = pedigree.Node.get_oldest(grand_children)

        if oldest_grand_child is None:
            return None

        description = "By oldest grand child {} - 50".format(oldest_grand_child.individual.identifier)
        return tuple((oldest_grand_child.get_yob() - 50, description)) if oldest_grand_child.get_yob() else None

    def __by_cousins(self, node):
        # 7. als yob neven/nichten bekend*, gemiddelde yob neven/nichten
        cousins = node.get_cousins()

        sum_yob = 0
        count = 0

        cousins_considered = set()
        for cousin in cousins:
            yob = cousin.get_yob()

            if yob:
                cousins_considered.add(cousin)
                sum_yob = sum_yob + yob
                count = count + 1
        
        if count > 0:
            cousin_ids = list(map(lambda n: n.individual.identifier, cousins_considered))
            description = "Cousins: {}".format(",".join(cousin_ids))
            return tuple((int(sum_yob / count), description))

        return None

    def __by_generations(self, node):
        # bekijk eerst generatie boven, pak alle bekende yobs en neem daar gemiddelde van, indien niks, ga dan laag
        # naar beneden. ga zo door de lagen totdat een yob gevonden is

        older_nodes = [node]
        younger_nodes = [node]

        iteration_count = 0

        while len(older_nodes) > 0 or len(younger_nodes) > 0:
            iteration_count = iteration_count + 1
            older_generation = set()
            
            for node in older_nodes:
                older_generation.update(node.get_parents())
                older_generation.update(node.get_parents_siblings())

            older_nodes = list(older_generation)
            older_generation_with_yob = list(filter(lambda node: node.get_yob() is not None, older_nodes))
            yobs = list(map(lambda node: node.get_yob(), older_generation_with_yob))

            if len(yobs) > 0:
                yob = sum(yobs) / len(yobs)
                generation_ids = list(map(lambda n: n.individual.identifier, older_generation_with_yob))
                description = "By older generation, {} levels above, identifiers: {}".format(iteration_count, ",".join(generation_ids))
                return tuple((int(yob) + (iteration_count * 25), description))

            younger_generation = set()

            for node in younger_nodes:
                younger_generation.update(list(node.children))

            siblings = set()
            for node in younger_generation:
                siblings.update(node.get_siblings())

            younger_generation.update(siblings)

            younger_nodes = list(younger_generation)
            younger_generation_with_yob = list(filter(lambda node: node.get_yob() is not None, younger_nodes))
            yobs = list(map(lambda node: node.get_yob(), younger_generation_with_yob))

            if len(yobs) > 0:
                yob = sum(yobs) / len(yobs)
                generation_ids = list(map(lambda n: n.individual.identifier, younger_generation_with_yob))
                description = "By younger generation, {} levels below, identifiers: {}".format(iteration_count, ",".join(generation_ids))
                return tuple((int(yob) - (iteration_count * 25), description))

        return None
