from simplepyble import Peripheral
from enum import Enum
from time import sleep

from arduinostate import ArduinoState
from enums.paletteblending import PaletteBlending
from enums.palettemode import PaletteMode
from enums.palettetype import PaletteType
from custom_palette.custompalette import CustomPalette

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

    def _block_until_ready(self, hello_update=False):
        while self.command_state != CommandState.READY:
            if self.timer > MAX_TIMEOUT:
                self.last_command_success = False
                self._reset()
                break
            self.timer += DELAY
            sleep(DELAY)

        if not hello_update and self.last_command_success:
            self.hello()

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
        buffer = msg[:16]
        msg = msg[16:]
        while len(buffer) > 0:
            self.device.write_command(SERVICE, CHARACTERISTIC, str.encode(buffer))
            buffer = msg[:16]
            msg = msg[16:]
        self.device.write_command(SERVICE, CHARACTERISTIC, str.encode("\n"))

    def _hello_response(self, response: str):
        self._reset()
        self.arduino_state = ArduinoState(response)

    # Commands
    def set_color(self, rgb: (int, int, int)):
        self._write(f"color {rgb[0]} {rgb[1]} {rgb[2]}")
        self._block_until_ready()

    def set_palette_type(self, palette: PaletteType):
        if palette is None: return
        palette_int: int = palette.value
        self._write(f"palette {palette_int}")
        self._block_until_ready()

    def set_palette_blending(self, blending: PaletteBlending):
        if blending is None: return
        blending_int: int = blending.value
        self._write(f"blend {blending_int}")
        self._block_until_ready()

    def set_brightness(self, brightness: int):
        brightness = max(0, min(brightness, 255))
        self._write(f"bright {brightness}")
        self._block_until_ready()

    def set_palette_delay(self, delay: int):
        self._write(f"delay {delay}")
        self._block_until_ready()

    def set_palette_mode(self, palette_mode: PaletteMode):
        palette_mode_int: int = palette_mode.value
        self._write(f"pmode {palette_mode_int}")
        self._block_until_ready()

    def set_palette_stretch(self, stretch: int):
        self._write(f"stretch {stretch}")
        self._block_until_ready()

    def send_palette(self, custom_palette: CustomPalette):
        palette_commands: list[str] = custom_palette.build_commands()
        for (i, command) in enumerate(palette_commands):
            percentage: int = round((float(i) / len(palette_commands)) * 100)
            print(f"{percentage}%...", end="")

            self._write(command)
            self._block_until_ready(i < len(palette_commands) - 1)
            if not self.last_command_success: break

        self.set_palette_type(PaletteType.CUSTOM)

    def hello(self):
        self.state_on_reset = CommandState.AWAITING_HELLO
        self._write(f"hello")
        self._block_until_ready(True)

    def display_current_state(self):
        print(str(self.arduino_state))
