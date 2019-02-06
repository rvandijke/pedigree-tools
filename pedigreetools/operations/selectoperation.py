from pedigreetools.utils.cli import CLIOperation
from .quit import QuitOperation

class SelectOperation(CLIOperation):
    def __init__(self, operations):
        self.operations = operations

    def execute(self, context):
        self.add_text("Select an operation to execute", bold = True)
        self.add_text("")

        choice_index = -1

        while choice_index < 0 or choice_index >= len(self.operations):
            for index in range(0, len(self.operations)):
                operation = self.operations[index]
                self.add_text("{}) {}".format(index + 1, operation.title()), bold = True, yellow = True)
                self.add_text(operation.description(), dim = True)
                self.add_text("")

            result = self.ask_input("Which operation do you want to perform: ").strip()

            if result == 'q':
                QuitOperation().execute(context)
                return

            result = ''.join(filter(lambda x: x.isdigit(), result))
            if len(result) > 0:
                choice_index = int(result) - 1
            else:
                choice_index = -1

            self.clear()

        context.operation = self.operations[choice_index]
