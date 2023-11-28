class Version:
    major: int
    minor: int
    patch: int

    def __init__(self, version_str: str):
        version_split = version_str.split(".")
        self.major = int(version_split[0])
        self.minor = int(version_split[1])
        self.patch = int(version_split[2])

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
