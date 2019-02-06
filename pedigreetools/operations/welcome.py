from pedigreetools.utils.cli import CLIOperation

class WelcomeOperation(CLIOperation):
    def execute(self, context):
        self.add_text("Pedigree tools v0.1 for Merel", bold = True)