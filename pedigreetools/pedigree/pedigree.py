from .node import Node

class Pedigree:
    def __init__(self, identifier, individuals):
        self.identifier = identifier
        self.nodes = self.__construct_nodes_from_individuals(individuals)

    def get_nodes(self):
        for node in self.nodes:
            yield node

    def get_individuals(self):
        for node in self.nodes:
            yield node.individual

    def find(self, individual_id):
        return self.__traverse(lambda node: node.individual.identifier == individual_id)

    def contains_relative_for(self, individual):
        def find_relative(node):
            for child in node.children:
                if (child.individual.identifier == individual.identifier or
                    child.individual.identifier == individual.mother_identifier or
                    child.individual.identifier == individual.father_identifier):
                    return True

            # individual contains no info about children, so find other by parents
            return (node.individual.identifier == individual.identifier or 
                    node.individual.father_identifier == individual.identifier or 
                    node.individual.mother_identifier == individual.identifier or
                    node.individual.identifier == individual.father_identifier or
                    node.individual.identifier == individual.mother_identifier)

        return self.__traverse(find_relative)            

    def show(self):
        root_nodes = self.__collect(lambda node: node.father is None and node.mother is None)

        def inner_show(node, idx = 0):
            spaces = " " * idx
            if idx > 0:
                spaces = spaces + "-> "

            print("{} {} (mother {}, father {})".format(spaces, node.individual.identifier, node.individual.mother_identifier, node.individual.father_identifier))

            for child in node.children:
                inner_show(child, idx + 1)

        for node in root_nodes:
            inner_show(node)

    def add_relative(self, individual):
        self.nodes.append(Node(individual, None, None))

        self.__resolve_relations()

    def __collect(self, condition):
        result = []

        for node in self.nodes:
            if condition(node):
                result.append(node)

        return result

    def __traverse(self, condition, nodes = None):
        nodes = nodes if nodes else self.nodes

        for node in nodes:
            if condition(node):
                return node

        return None

    def __construct_nodes_from_individuals(self, individuals):
        nodes = list(map(lambda individual: Node(individual, None, None), individuals))

        for first in nodes:
            for second in nodes:
                if first.father is None:
                    if second.individual.identifier == first.individual.father_identifier:
                        # new child gets added by father id
                        second.children.append(first)
                        first.father = second

                if first.mother is None:
                    if second.individual.identifier == first.individual.mother_identifier:
                        # new child gets added by mother id
                        second.children.append(first)
                        first.mother = second
                
                for child in second.children:
                    if child.father is None:
                        if child.individual.father_identifier == first.individual.identifier:
                            # new father gets added
                            node.children.append(child)
                            child.father = first

                    if child.mother is None:
                        if child.individual.mother_identifier == first.individual.identifier:
                            # new mother gets added
                            first.children.append(child)
                            child.mother = first

        return nodes
            
