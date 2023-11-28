from enum import Enum

from version import Version


class Mode(Enum):
    COLOR = 0
    PALETTE = 1


class PaletteType(Enum):
    RAINBOW = 0
    RAINBOW_STRIPE = 1
    PARTY = 2
    OCEAN = 3
    LAVA = 4
    FOREST = 5
    CUSTOM = 6


class PaletteBlending(Enum):
    NOBLEND = 0
    LINEARBLEND = 1
    LINEARBLEND_NOWRAP = 2


class PaletteMode(Enum):
    STATIC = 0
    SCROLLING = 1
    SOLID = 2


class ArduinoState:
    version: Version
    color: (int, int, int)
    mode: Mode
    brightness: int
    paletteType: PaletteType
    paletteDelay: int
    paletteStretch: int
    paletteMode: PaletteMode
    paletteBlending: PaletteBlending

    def __init__(self, response: str):
        split_response = response.split(" ")
        self.version = Version(split_response[0])

        color_split = split_response[1].split(",")
        self.color = (color_split[0], color_split[1], color_split[2])
        self.mode = Mode(int(split_response[2]))
        self.brightness = int(split_response[3])
        self.paletteType = PaletteType(int(split_response[4]))
        self.paletteDelay = int(split_response[5])
        self.paletteStretch = int(split_response[6])
        self.paletteMode = PaletteMode(int(split_response[7]))
        self.paletteBlending = PaletteBlending(int(split_response[8]))

    def __str__(self) -> str:
        return f"""Arduino Status:
          Version: {str(self.version)}
          Color: {str(self.color)}
          Mode: {self.mode.name}
          Brightness: {str(self.brightness)}
          Palette: {self.paletteType.name}
          Palette Delay: {str(self.paletteDelay)}
          Palette Stretch: {str(self.paletteStretch)}
          Palette Mode: {self.paletteMode.name}
          Palette Blending: {self.paletteBlending.name}"""
