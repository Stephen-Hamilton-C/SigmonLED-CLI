from enums.palettetype import PaletteType


def parse_palette_type(split_command: list[str]) -> PaletteType | None:
    if len(split_command) < 3:
        print("Not enough args!")
        return None

    palette_type: PaletteType
    try:
        type_int: int = int(split_command[2])
        palette_type = PaletteType(type_int)
    except ValueError:
        try:
            palette_type = PaletteType[split_command[2].upper()]
        except KeyError:
            print("Invalid type name")
            return None

    return palette_type
