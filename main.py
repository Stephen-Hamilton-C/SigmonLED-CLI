from simplepyble import Peripheral, Service, Adapter
from commander import Commander


def device_filter(device: Peripheral) -> bool:
    service: Service
    for service in device.services():
        if service.uuid() == "0000ffe0-0000-1000-8000-00805f9b34fb":
            return True
    return False

if __name__ == '__main__':
    if not Adapter.bluetooth_enabled():
        print("Bluetooth is not enabled!")
        exit(1)

    adapters: list[Adapter] = Adapter.get_adapters()
    if len(adapters) == 0:
        print("No Bluetooth adapters found!")
        exit(1)

    adapter: Adapter = adapters[0]

    # Scan for 3000 milliseconds
    print("Scanning for SigmonLED devices...")
    adapter.scan_for(2000)

    # Scan complete. Filter devices...
    devices: list[Peripheral] = adapter.scan_get_results()
    sigmonled_devices: list[Peripheral] = list(filter(device_filter, devices))

    # Exit if no devices found
    if len(sigmonled_devices) == 0:
        print("No devices to connect to!")
        exit(1)

    choice: int
    if len(sigmonled_devices) > 1:
        # List devices to user
        i: int
        device: Peripheral
        for (i, device) in enumerate(sigmonled_devices):
            print(f"[{i}]: \"{device.identifier()}\" -- {device.address()}")

        # Get decision from user
        choice = int(input("Select a device to connect to: "))
    else:
        choice = 0

    device = sigmonled_devices[choice]

    # Connect to selected device
    print(f"Connecting to \"{device.identifier()}\" -- {device.address()}...")
    device.connect()
    print("Connected.")

    # Pass to command parser
    commander = Commander(device)
    commander.listen()

    print("Disconnecting...")
    device.disconnect()
    print("Goodbye!")