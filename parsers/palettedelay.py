def parse_palette_delay(split_command: list[str]) -> int | None:
    if len(split_command) < 3:
        print("Not enough args!")
        return None

    try:
        delay: int = int(split_command[2])
        return max(0, min(delay, 65535))
    except ValueError:
        print("Expected an integer for delay command.")
        return None
