import sys
import os

class CLI:
    class Context:
        pass

    def __init__(self):
        self.context = CLI.Context()

    def run(self, operations = None):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        self.__execute_operations(operations)

    def __execute_operations(self, operations):
        if operations is None:
            return

        for operation in operations:
            operation.cli = self
            if operation.execute(self.context) == False:
                print("Operation {} failed".format(operation))
                sys.exit(0)

            operation.cli = None
            print("")

        self.run()
