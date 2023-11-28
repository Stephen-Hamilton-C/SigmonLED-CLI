def parse_brightness(split_command: list[str]) -> int:
    brightness: int
    return max(0, min(brightness, 255))
