def parse_color(args: list[str]) -> (int, int, int):
    if len(args) == 2 and len(args[1]) == 7 and args[1].startswith("#"):
        # Hexadecimal parsing
        # #123456
        r_hex: str = args[1][1:3]
        g_hex: str = args[1][3:5]
        b_hex: str = args[1][5:]
        r: int = int(r_hex, 16)
        g: int = int(g_hex, 16)
        b: int = int(b_hex, 16)
        return r, g, b

    if len(args) < 4:
        print("Not enough args!")
        return None
    r: int = int(args[1])
    g: int = int(args[2])
    b: int = int(args[3])
    return r, g, b
