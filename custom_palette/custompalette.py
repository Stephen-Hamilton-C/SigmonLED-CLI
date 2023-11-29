import json
from colour import Color


class CustomPalette:
    name: str = "Untitled"
    _colors: list[Color]

    def __init__(self, name: str, colors: list[Color]):
        if len(colors) > 16:
            raise RuntimeError("Color list cannot be more than 16 colors!")
        elif 16 % len(colors) != 0:
            raise RuntimeError("Color list length must be a factor of 16!")

        self.name = name
        self._colors = colors

    def _build_colors(self) -> list[Color]:
        colors: list[Color] = []
        for i in range(16 // len(self._colors)):
            colors.extend(self._colors)

        return colors

    def build_command_string(self) -> str:
        colors: list[Color] = self._build_colors()
        string: str = ""
        for (i, color) in enumerate(colors):
            string += f"{round(color.red * 255)} {round(color.green * 255)} {round(color.blue * 255)}"
            if i < len(colors) - 1:
                string += " "
        return string

    def build_commands(self) -> list[str]:
        colors: list[Color] = self._build_colors()
        commands: list[str] = []
        for (i, color) in enumerate(colors):
            commands.append(
                f"custom {i} {round(color.red * 255)} {round(color.green * 255)} {round(color.blue * 255)}"
            )

        return commands

    def to_json(self) -> str:
        data = {
            "name": self.name,
            "colors": []
        }
        for color in self._colors:
            data["colors"].append(color.hex)

        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        colors: list[Color] = []
        for color_data in data["colors"]:
            colors.append(Color(color_data))

        return cls(data["name"], colors)
