import os
import inquirer

class CLIOperation:
    def title(self):
        return "<Title here>"

    def description(self):
        return "<Description here>"

    def execute(self, context):
        pass

    def clear(self):
        os.system('clear')

    def add_text(self, text, bold = False, dim = False, yellow = False, red = False, blue = False, green = False):
        format_string = "{}"
        if bold:
            format_string = "\033[1m{}\033[0m"
        if dim:
            format_string = "\033[2m{}\033[0m"
        if yellow:
            format_string = "\033[33m{}\033[0m"
        if red:
            format_string = "\033[31m{}\033[0m"
        if blue:
            format_string = "\033[34m{}\033[0m"
        if green:
            format_string = "\033[32m{}\033[0m"

        #print(format_string.format(text))
        print(text)

    def ask_input(self, text):
        return input(text)

    def choice(self, text, options):
        question = inquirer.List('q',
                                 message = text,
                                 choices = options)
        inquirer.prompt([question])
    
    def show_checkboxes(self, question, options, all_selected = True):
        question = inquirer.Checkbox('q', 
                                     message = question,
                                     choices = sorted(options),
                                     default = options if all_selected else [])
        result = inquirer.prompt([question])
        return result['q']
        
