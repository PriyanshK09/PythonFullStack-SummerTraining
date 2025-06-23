from sys import argv
from src.command_processor import CommandProcessor

class Application:
    def __init__(self):
        self.__command_processor = CommandProcessor()

    def run(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
        for line in lines:
            self.__command_processor.process_command(line)

def main():
    if len(argv) != 2:
        raise Exception("File path not entered")
    
    app = Application()
    app.run(argv[1])

if __name__ == "__main__":
    main()