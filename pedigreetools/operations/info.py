from pedigreetools.utils.cli import CLIOperation

class InfoOperation(CLIOperation):
    def title(self):
        return "Pedigree Info"

    def description(self):
        return "See information about loaded dataset"

    def execute(self, context):
        self.add_text("Number of pedigrees in dataset: {}".format(len(context.dataset.pedigrees)), green = True)
        self.add_text("")
        
        for pedigree in context.dataset.pedigrees:
            self.add_text("Pedigree {} with {} individuals".format(pedigree.identifier, len(pedigree.nodes)))
            self.add_text("")

        self.ask_input("Press return to continue")

        return True