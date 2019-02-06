import os.path
from pedigreetools.utils.cli import CLIOperation
from pedigreetools.pedigree import DataSet

class SaveFileOperation(CLIOperation):
    def title(self):
        return "Save File"

    def description(self):
        return "Saves the dataset that you performed operations on to a new file."

    def execute(self, context):
        path = self.ask_input("Please enter a file path to save the dataset: ")

        while os.path.exists(path):
            path = self.ask_input("That file already exists. Please specify another file: ")

        context.dataset.save(path)

        self.ask_input("File {} saved, press return to continue".format(path))

        return True