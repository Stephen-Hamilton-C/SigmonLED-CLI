def parse_palette_stretch(split_command: list[str]) -> int | None:
    if len(split_command) < 3:
        print("Not enough args!")
        return None

    try:
        stretch: int = int(split_command[2])
        return max(0, min(stretch, 255))
    except ValueError:
        print("Expected an integer for palette stretch command.")
        return None
