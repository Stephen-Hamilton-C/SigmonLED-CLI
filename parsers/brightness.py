def parse_brightness(split_command: list[str]) -> int | None:
    if len(split_command) < 2:
        print("Not enough args!")
        return None

    try:
        brightness: int = int(split_command[1])
        return max(0, min(brightness, 255))
    except ValueError:
        print("Expected an integer for brightness command.")
        return None
