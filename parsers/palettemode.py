from enums.palettemode import PaletteMode


def parse_palette_mode(split_command: list[str]) -> PaletteMode | None:
    if len(split_command) < 3:
        print("Not enough args!")
        return None

    mode: PaletteMode
    try:
        mode_int: int = int(split_command[2])
        mode = PaletteMode(mode_int)
    except ValueError:
        try:
            mode = PaletteMode[split_command[2].upper()]
        except KeyError:
            print("Invalid mode name")
            return None

    return mode
