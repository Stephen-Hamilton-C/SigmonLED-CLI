from enums.palettetype import PaletteType


def parse_palette_type(split_command: list[str]) -> PaletteType:
    try:
        palette_num: int = int(split_command[2])
        return PaletteType(palette_num)
    except ValueError:
        # Not an integer input, try string instead
        return PaletteType[split_command[2].upper()]
