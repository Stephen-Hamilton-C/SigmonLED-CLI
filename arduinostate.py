from enums.mode import Mode
from enums.paletteblending import PaletteBlending
from enums.palettemode import PaletteMode
from enums.palettetype import PaletteType
from version import Version


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
