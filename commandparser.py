from simplepyble import Peripheral
from re import split

from arduinostate import PaletteType
from controller import Controller
from parsers.color import parse_color


class CommandParser:
    _controller: Controller

    def __init__(self, device: Peripheral):
        self._controller = Controller(device)

    def color_command(self, split_command: list[str]):
        color: (int, int, int) = parse_color(split_command)
        if color is None: return
        self._controller.set_color(color)

    def brightness_command(self, split_command: list[str]):
        pass

    def palette_command(self, split_command: list[str]):
        subcommand: str = split_command[1]
        if subcommand == "type":
            self.palette_type_command(split_command)
        elif subcommand == "blend":
            self.palette_blending_command(split_command)
        elif subcommand == "delay":
            self.palette_delay_command(split_command)
        elif subcommand == "mode":
            self.palette_mode_command(split_command)
        elif subcommand == "stretch":
            self.palette_stretch_command(split_command)
        else:
            print("Unknown palette subcommand.")

    def palette_type_command(self, split_command: list[str]):
        palette: PaletteType
        try:
            palette_num: int = int(split_command[2])
            palette = PaletteType(palette_num)
            return
        except ValueError:
            # Not an integer input, try string instead
            palette = PaletteType[split_command[2].upper()]
        self._controller.set_palette_type(palette)

    def palette_blending_command(self, split_command: list[str]):
        pass

    def palette_delay_command(self, split_command: list[str]):
        pass

    def palette_mode_command(self, split_command: list[str]):
        pass

    def palette_stretch_command(self, split_command: list[str]):
        pass

    def state_command(self):
        self._controller.display_current_state()

    def listen(self):
        self._controller.hello()
        command: str = ""
        while command != "exit":
            command = input(">").lower().strip()
            split_command: list[str] = split(r"\s+", command)
            command_name = split_command[0]
            if command_name == "color":
                self.color_command(split_command)
            elif command_name == "palette":
                self.palette_command(split_command)
            elif command_name == "state":
                self.state_command()
            elif command_name == "brightness":
                self.brightness_command(split_command)
            elif command_name == "exit":
                break
            else:
                print("Unknown command.")
