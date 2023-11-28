from simplepyble import Peripheral
from enum import Enum
from time import sleep

from arduinostate import ArduinoState

SERVICE: str = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC: str = "0000ffe1-0000-1000-8000-00805f9b34fb"
MAX_ATTEMPTS: int = 5
MAX_TIMEOUT: float = 5
DELAY: float = 0.1


class CommandState(Enum):
    READY = 0
    AWAITING_RESPONSE = 1
    AWAITING_HELLO = 2


class Controller:
    command_state: CommandState = CommandState.READY
    response_buffer: str = ""
    last_message: str = ""
    attempts: int = 0
    timer: float = 0
    device: Peripheral
    state_on_reset: CommandState = CommandState.READY
    arduino_state: ArduinoState
    last_command_success: bool = False

    def __init__(self, device: Peripheral):
        self.device = device
        device.notify(SERVICE, CHARACTERISTIC, self._incoming_data)

    def _block_until_ready(self):
        while self.command_state != CommandState.READY:
            if self.timer > MAX_TIMEOUT:
                print(f"Command timed out. No response after {MAX_TIMEOUT} seconds.")
                self.last_command_success = False
                self._reset()
                break
            self.timer += DELAY
            sleep(DELAY)

    def _reset(self):
        self.command_state = self.state_on_reset
        self.attempts = 0
        self.timer = 0
        self.state_on_reset = CommandState.READY

    def _incoming_data(self, data: bytes):
        if not data.isascii(): return
        if self.command_state == CommandState.READY: return
        for char in data.decode("ascii"):
            self.response_buffer += char
            if char == '\n':
                if self.command_state == CommandState.AWAITING_RESPONSE:
                    self._confirm_response(self.response_buffer)
                elif self.command_state == CommandState.AWAITING_HELLO:
                    self._hello_response(self.response_buffer)
                self.response_buffer = ""

    def _confirm_response(self, response: str):
        if response.startswith("verify") and response.strip().endswith(self.last_message):
            if response.strip().endswith(self.last_message):
                self._write("confirm")
            else:
                print(f"Received \"{response}\", which does not match \"{self.last_message}\"")
                self._write(self.last_message)
        elif response.startswith("confirmed"):
            self._reset()
            self.last_command_success = True
        elif response.startswith("disregard"):
            self._write(self.last_message)

    def _write(self, msg: str):
        if self.attempts > MAX_ATTEMPTS:
            self.state_on_reset = CommandState.READY
            self.last_command_success = False
            print(f"Failed to send command! Gave up after {self.attempts} times.")
            self._reset()
            return

        self.attempts += 1
        self.last_message = msg
        self.command_state = CommandState.AWAITING_RESPONSE
        self.device.write_command(SERVICE, CHARACTERISTIC, str.encode(f"{self.last_message}\n"))

    def _hello_response(self, response: str):
        self.arduino_state = ArduinoState(response)
        self._reset()

    # Commands
    def color(self, rgb: (int, int, int)):
        self._write(f"color {rgb[0]} {rgb[1]} {rgb[2]}")
        self._block_until_ready()
        if self.last_command_success:
            self.arduino_state.color = rgb

    def hello(self):
        self.state_on_reset = CommandState.AWAITING_HELLO
        self._write(f"hello")
        self._block_until_ready()

    def display_current_state(self):
        print(str(self.arduino_state))
