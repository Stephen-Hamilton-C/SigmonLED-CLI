from simplepyble import Peripheral
from re import split

from controller import Controller
from enums.paletteblending import PaletteBlending
from enums.palettemode import PaletteMode
from enums.palettetype import PaletteType
from parsers.brightness import parse_brightness
from parsers.color import parse_color
from parsers.paletteblending import parse_palette_blending
from parsers.palettedelay import parse_palette_delay
from parsers.palettemode import parse_palette_mode
from parsers.palettestretch import parse_palette_stretch
from parsers.palettetype import parse_palette_type


class CommandParser:
    _controller: Controller

    def __init__(self, device: Peripheral):
        self._controller = Controller(device)

    def color_command(self, split_command: list[str]):
        color: (int, int, int) = parse_color(split_command)
        if color is None: return
        self._controller.set_color(color)

    def brightness_command(self, split_command: list[str]):
        brightness: int = parse_brightness(split_command)
        if brightness is None: return
        self._controller.set_brightness(brightness)

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
        palette: PaletteType = parse_palette_type(split_command)
        if palette is None: return
        self._controller.set_palette_type(palette)

    def palette_blending_command(self, split_command: list[str]):
        palette_blending: PaletteBlending = parse_palette_blending(split_command)
        if palette_blending is None: return
        self._controller.set_palette_blending(palette_blending)

    def palette_delay_command(self, split_command: list[str]):
        palette_delay: int = parse_palette_delay(split_command)
        if palette_delay is None: return
        self._controller.set_palette_delay(palette_delay)

    def palette_mode_command(self, split_command: list[str]):
        palette_mode: PaletteMode = parse_palette_mode(split_command)
        if palette_mode is None: return
        self._controller.set_palette_mode(palette_mode)

    def palette_stretch_command(self, split_command: list[str]):
        palette_stretch: int = parse_palette_stretch(split_command)
        if palette_stretch is None: return
        self._controller.set_palette_stretch(palette_stretch)

    def state_command(self):
        self._controller.display_current_state()

    def listen(self):
        self._controller.hello()
        command: str = ""
        while command != "exit" and self._controller.device.is_connected():
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
            elif self._controller.device.is_connected():
                print("Unknown command.")
