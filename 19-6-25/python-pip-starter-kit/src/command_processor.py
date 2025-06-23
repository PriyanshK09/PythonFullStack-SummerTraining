from src.services import MetroService

class CommandProcessor:
    def __init__(self):
        self.__metro_service = MetroService()

    def process_command(self, command_line):
        parts = command_line.strip().split()
        command = parts[0]
        
        if command == "BALANCE":
            self.__metro_service.create_balance(parts[1], parts[2])
        elif command == "CHECK_IN":
            self.__metro_service.check_in(parts[1], parts[2], parts[3])
        elif command == "PRINT_SUMMARY":
            self.__metro_service.generate_summary()