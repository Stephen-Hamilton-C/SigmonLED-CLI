from colour import Color
import appdirs
import os

from custom_palette.custompalette import CustomPalette


class PaletteManager:
    _data_dir: str = appdirs.user_data_dir("sigmonled-cli", False)

    def palette_creator(self):
        print("Palette Creator")
        print("------------------------------")

        print("Enter 16 colors, or enter \"Done\" when finished with colors")
        print("Note that number of colors must be 1, 2, 4, 8, or 16.")
        colors: list[Color] = []
        while len(colors) < 16:
            next_color = input(f"Enter the color for color {len(colors)+1} as a hex code (#12abef): ")

            if next_color.lower().strip().startswith("done"):
                if 16 % len(colors) != 0:
                    print("Number of colors must be 1, 2, 4, 8, or 16!")
                else:
                    break
            else:
                colors.append(Color(next_color))
                # TODO: Catch possible error and print message

        palette_name: str = input("Enter a name for this new palette: ")
        palette: CustomPalette = CustomPalette(palette_name, colors)
        palette_data: str = palette.to_json()
        palette_path: str = os.path.join(self._data_dir, palette_name+".json")

        os.makedirs(self._data_dir, exist_ok=True)
        with open(palette_path, "w") as palette_file:
            palette_file.write(palette_data)

        print(f"Created palette {palette_name}")

    def select_palette(self) -> CustomPalette | None:
        palettes: list[CustomPalette] = self._load_palettes()
        if len(palettes) == 0:
            print("No palettes created yet!")
            return None

        selected_palette: CustomPalette
        if len(palettes) == 1:
            selected_palette = palettes[0]
        else:
            for (i, palette) in enumerate(palettes):
                print(f"[{i}]: {palette.name}")

            choice: int
            try:
                choice = int(input("Select palette to send to device: "))
            except ValueError:
                choice = -1

            while choice < 0 or choice >= len(palettes):
                try:
                    choice = int(input(f"Invalid selection. Selection must be between 0 - {len(palettes) - 1}: "))
                except ValueError:
                    choice = -1
            selected_palette = palettes[choice]

        return selected_palette

    def _load_palettes(self) -> list[CustomPalette]:
        palettes: list[CustomPalette] = []
        files: list[str] = os.listdir(self._data_dir)

        for file in files:
            file_path: str = os.path.join(self._data_dir, file)
            if os.path.isfile(file_path) and file.endswith(".json"):
                with open(file_path, "r") as palette_file:
                    lines: list[str] = palette_file.readlines()
                    data = '\n'.join(lines)
                    palettes.append(CustomPalette.from_json(data))

        return palettes
