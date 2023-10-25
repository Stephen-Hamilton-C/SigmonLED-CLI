from simplepyble import Peripheral
from re import split
from time import sleep
from enum import Enum

SERVICE: str = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC: str = "0000ffe1-0000-1000-8000-00805f9b34fb"
MAX_ATTEMPTS: int = 5
MAX_TIMEOUT: float = 5
DELAY: float = 0.1


class State(Enum):
    READY = 0
    AWAITING_RESPONSE = 1


class Commander:
    state: State = State.READY
    response_buffer: str = ""
    last_message: str = ""
    attempts: int = 0
    timer: float = 0
    device: Peripheral

    def __init__(self, device: Peripheral):
        self.device = device
        device.notify(SERVICE, CHARACTERISTIC, self._incoming_data)

    def listen(self):
        command: str = ""
        while command != "exit":
            command = input(">").lower().strip()
            split_command: list[str] = split(r"\s+", command)
            if split_command[0] == "color":
                if len(split_command) < 4:
                    print("Not enough args!")
                else:
                    r: int = int(split_command[1])
                    g: int = int(split_command[2])
                    b: int = int(split_command[3])
                    self._write(f"color {r} {g} {b}")
            elif command == "exit":
                break
            else:
                print("Unknown command.")
            while self.state != State.READY:
                if self.timer > MAX_TIMEOUT:
                    print(f"Command timed out. No response after {MAX_TIMEOUT} seconds.")
                    self._reset()
                    break
                self.timer += DELAY
                sleep(DELAY)

    def _reset(self):
        self.state = State.READY
        self.attempts = 0
        self.timer = 0

    def _incoming_data(self, data: bytes):
        if not data.isascii(): return
        if self.state != State.AWAITING_RESPONSE: return
        for char in data.decode("ascii"):
            self.response_buffer += char
            if char == '\n':
                self._confirm(self.response_buffer)
                self.response_buffer = ""

    def _confirm(self, response: str):
        if response.startswith("verify") and response.strip().endswith(self.last_message):
            if response.strip().endswith(self.last_message):
                self._write("confirm")
            else:
                print(f"Received \"{response}\", which does not match \"{self.last_message}\"")
                self._write(self.last_message)
        elif response.startswith("confirmed"):
            self._reset()
        elif response.startswith("disregard"):
            self._write(self.last_message)

    def _write(self, msg: str):
        if self.attempts > MAX_ATTEMPTS:
            print(f"Failed to send command! Gave up after {self.attempts} times.")

        self.attempts += 1
        self.last_message = msg
        self.state = State.AWAITING_RESPONSE
        self.device.write_command(SERVICE, CHARACTERISTIC, str.encode(f"{self.last_message}\n"))
