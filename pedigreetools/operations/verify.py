import pedigreetools.pedigree
from pedigreetools.utils.cli import CLIOperation
import sys

class VerifyOperation(CLIOperation):
    def title(self):
        return "Verify Pedigrees"

    def description(self):
        return "Verify if a pedigree file is correct"

    def execute(self, context):
        pedigrees = context.dataset.pedigrees

        self.log_file = open("log.txt", "w+")

        for pedigree in pedigrees:
            self.__write_log("Checking family {}".format(pedigree.identifier))

            for node in pedigree.nodes:
                self.__verify(node)

            self.__write_log("------")

        self.log_file.close()
        self.ask_input("Please return to continue")

    def __write_log(self, entry):
        print(entry)
        self.log_file.write(entry)
        self.log_file.write("\n")

    def __verify(self, node):
        self.__write_log("Verifying individual {}".format(node.individual.identifier))

        def concat(nodes):
            return ",".join(list(map(lambda node: node.individual.identifier, nodes)))

        try:
            self.__write_log("Getting parents")
            self.__write_log(concat(node.get_parents()))

            self.__write_log("Getting children")
            self.__write_log(concat(node.children))

            self.__write_log("Getting grand parents")
            self.__write_log(concat(node.get_grand_parents()))

            self.__write_log("Getting cousins")
            self.__write_log(concat(node.get_cousins()))
        except:
            self.__write_log("Unexpected error: {}".format(sys.exc_info()[0]))

        parents = node.get_parents()
        parent_ids = ",".join(list(map(lambda parent: parent.individual.identifier, parents)))
        self.__write_log("Found parents '{}'".format(parent_ids))

        if node.mother:
            self.__write_log("Has mother '{}'".format(node.mother.individual.identifier))

            if node.mother in parents:
                self.__write_log("Mother found correctly in parents")
            else:
                self.__write_log("Mother not found in parents")
        else:
            self.__write_log("Has no mother")

        if node.father:
            self.__write_log("Has father {}".format(node.father.individual.identifier))

            if node.father in parents:
                self.__write_log("Father found correctly in parents")
            else:
                self.__write_log("Father not found in parents")
        else:
            self.__write_log("Has no father")
            
        for child in node.children:
            self.__write_log("Has child {}".format(child.individual.identifier))

        grand_parents = node.get_grand_parents()
        grand_parent_ids = ",".join(list(map(lambda gp: gp.individual.identifier, grand_parents)))
        self.__write_log("Found grand parents '{}'".format(grand_parent_ids))

        #parent_siblings = set()
        #for grand_parent in grand_parents:
        #    parent_siblings.update(grand_parent.children)
