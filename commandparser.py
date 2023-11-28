from simplepyble import Peripheral
from re import split
from controller import Controller
from parsers.color import parse_color


class CommandParser:
    _controller: Controller

    def __init__(self, device: Peripheral):
        self._controller = Controller(device)

    def listen(self):
        self._controller.hello()
        command: str = ""
        while command != "exit":
            command = input(">").lower().strip()
            split_command: list[str] = split(r"\s+", command)
            command_name = split_command[0]
            if command_name == "color":
                color: (int, int, int) = parse_color(split_command)
                if color is None: return
                self._controller.color(color)
            elif command_name == "state":
                self._controller.display_current_state()
            elif command_name == "exit":
                break
            else:
                print("Unknown command.")
