from enums.paletteblending import PaletteBlending


def parse_palette_blending(split_command: list[str]) -> PaletteBlending | None:
    if len(split_command) < 3:
        print("Not enough args!")
        return None

    blending: PaletteBlending
    try:
        blending_int: int = int(split_command[2])
        blending = PaletteBlending(blending_int)
    except ValueError:
        try:
            blending = PaletteBlending[split_command[2].upper()]
        except KeyError:
            print("Invalid blending name")
            return None

    return blending
