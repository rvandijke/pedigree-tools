import sys
from pedigreetools.utils.cli import CLIOperation

class QuitOperation(CLIOperation):
    def title(self):
        return "Quit Program"

    def description(self):
        return "Quits program. Warning: Any unsaved changes will be lost!"

    def execute(self, context):
        self.add_text("Bye bye!", green = True)
        sys.exit(0)

        return True