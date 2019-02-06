import os.path
from pedigreetools.utils.cli import CLIOperation
from pedigreetools.pedigree import DataSet

class SpecifyFileOperation(CLIOperation):
    def title(self):
        return "Specify File"

    def execute(self, context):
        path = self.ask_input("Please enter a file path to load a pedigree: ").strip().replace('\ ', ' ')
        path = os.path.normpath(path)
        path = os.path.expanduser(path)

        while not os.path.exists(path) or path == ".":
            path = self.ask_input("No file exists at that location. Please enter a valid file path: ").strip().replace('\ ', ' ')
            path = os.path.normpath(path)
            path = os.path.expanduser(path)

        context.filename = path
        context.dataset = DataSet(context.filename)

        return True
