from enum import Enum

from version import Version


class Mode(Enum):
    COLOR = 0
    PALETTE = 1

    def __str__(self):
        default_str: str = super.__str__(self)
        mode_len = len("<Mode.")
        return default_str[mode_len:-4]


class PaletteType(Enum):
    RAINBOW = 0
    RAINBOW_STRIPE = 1
    PARTY = 2
    OCEAN = 3
    LAVA = 4
    FOREST = 5
    CUSTOM = 6

    def __str__(self):
        default_str: str = super.__str__(self)
        palette_type_len = len("<PaletteType.")
        return default_str[palette_type_len:-4]


class PaletteBlending(Enum):
    NOBLEND = 0
    LINEARBLEND = 1
    LINEARBLEND_NOWRAP = 2

    def __str__(self):
        default_str: str = super.__str__(self)
        palette_blending_len = len("<PaletteBlending.")
        return default_str[palette_blending_len:-4]


class ArduinoState:
    version: Version
    color: (int, int, int)
    mode: Mode
    brightness: int
    paletteType: PaletteType
    paletteDelay: int
    paletteStretch: int
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
        self.paletteBlending = PaletteBlending(int(split_response[7]))

    def __str__(self) -> str:
        return f"""Arduino Status:
          Version: {str(self.version)}
          Color: {str(self.color)}
          Mode: {str(self.mode)}
          Brightness: {str(self.brightness)}
          Palette: {str(self.paletteType)}
          Palette Delay: {str(self.paletteDelay)}
          Palette Stretch: {str(self.paletteStretch)}
          Palette Blending: {str(self.paletteBlending)}"""