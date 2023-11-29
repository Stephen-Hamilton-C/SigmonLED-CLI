from simplepyble import Peripheral, Service, Adapter
from commandparser import CommandParser
import signal

commander: CommandParser


def device_filter(device: Peripheral) -> bool:
    service: Service
    for service in device.services():
        if service.uuid() == "0000ffe0-0000-1000-8000-00805f9b34fb":
            return True
    return False


def disconnect(sig=None, frame=None):
    print("exit")
    print("Disconnecting...")
    device.disconnect()
    print("Goodbye!")


def on_disconnected():
    print()
    print("Lost connection to device. Press enter to exit.")
    exit(1)


def select_device(device_list: list[Peripheral]) -> Peripheral | None:
    # Exit if no devices found
    if len(device_list) == 0:
        print("No devices to connect to!")
        return None

    choice: int = -1
    if len(device_list) > 1:
        # List devices to user
        i: int
        device: Peripheral
        for (i, device) in enumerate(sigmonled_devices):
            print(f"[{i}]: \"{device.identifier()}\" -- {device.address()}")

        # Get decision from user
        choice = int(input("Select a device to connect to: "))
        while choice < 0 or choice >= len(device_list):
            try:
                choice = int(input(f"Invalid selection. Selection must be between 0 - {len(device_list) - 1}: "))
            except ValueError:
                choice = -1
    else:
        choice = 0

    return device_list[choice]


if __name__ == '__main__':
    signal.signal(signal.SIGINT, disconnect)

    if not Adapter.bluetooth_enabled():
        print("Bluetooth is not enabled!")
        exit(1)

    adapters: list[Adapter] = Adapter.get_adapters()
    if len(adapters) == 0:
        print("No Bluetooth adapters found!")
        exit(1)

    adapter: Adapter = adapters[0]
    existing_devices: list[Peripheral] = list(filter(device_filter, adapter.get_paired_peripherals()))
    print(f"Paired: {adapter.get_paired_peripherals()}")

    device: Peripheral
    if len(existing_devices) > 0:
        # List existing devices and connect to selection
        device = select_device(existing_devices)
    else:
        # Scan for 3000 milliseconds
        print("Scanning for SigmonLED devices...")
        adapter.scan_for(2000)

        # Scan complete. Filter devices...
        devices: list[Peripheral] = adapter.scan_get_results()
        sigmonled_devices: list[Peripheral] = list(filter(device_filter, devices))

        device = select_device(sigmonled_devices)

    if device is None: exit(1)

    device.set_callback_on_disconnected(on_disconnected)

    # Connect to selected device
    print(f"Connecting to \"{device.identifier()}\" -- {device.address()}...")
    device.connect()
    if not device.is_connected():
        print("Failed to connect to device!")
        exit(1)

    print("Connected.")

    # Pass to command parser
    commander = CommandParser(device)
    try:
        commander.listen()
        disconnect()
    except UnicodeDecodeError:
        # Likely KeyboardInterrupt, just ignore
        pass
    except ValueError:
        # Likely lost connection to device, just ignore
        pass
