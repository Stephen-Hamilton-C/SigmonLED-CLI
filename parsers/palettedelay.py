def parse_palette_delay(split_command: list[str]) -> int:
    delay: int
    return max(0, min(delay, 65535))
