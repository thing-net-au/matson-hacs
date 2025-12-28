# Matson Monitor HomeAssistant Integration

This is a custom HomeAssistant integration for connecting to Matson Monitor devices via Bluetooth Low Energy (BLE) with automatic binding support.

## Features

- **Automatic Discovery**: Automatically discovers Matson Monitor devices via Bluetooth
- **BLE Connection**: Connects to the device using the Bleak library
- **Automatic Binding**: Handles device binding (not pairing) automatically
- **Notification Support**: Enables BLE notifications for real-time data updates
- **Service Exposure**: Exposes all readable BLE characteristics as sensors
- **Signal Strength**: Monitors RSSI (signal strength)
- **Auto Reconnection**: Automatically reconnects if the connection is lost

## Installation

### HACS (Recommended)

1. Open HACS in HomeAssistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart HomeAssistant

### Manual Installation

1. Copy the `matson_monitor` folder to your HomeAssistant `custom_components` directory
2. Restart HomeAssistant

## Configuration

### Via UI (Recommended)

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Matson Monitor"
4. Select your device from the list
5. Click "Submit"

The integration will automatically discover Matson Monitor devices advertising via Bluetooth.

### Via Bluetooth Discovery

The integration supports automatic discovery. When a Matson Monitor device is detected, HomeAssistant will notify you and allow you to set it up. The binding process happens automatically on first connection.

## Binding vs Pairing

The MATSON Monitor uses **binding** rather than traditional Bluetooth pairing:

- **Pairing** = OS-level security (PIN codes, system-level encryption)
- **Binding** = Application-level authorization (enabling notifications, device session)

The integration automatically performs binding by:
1. Enabling notifications on all notify-capable BLE characteristics
2. Sending binding commands if required by the device
3. Maintaining the binding session across reconnections

No manual pairing is required.

## Usage

After setup, the integration will create:

- **Sensor entities** for each readable BLE characteristic
- **RSSI sensor** for signal strength monitoring
- **Device entry** in the Devices page

## BLE Service UUIDs

The integration uses the following default UUIDs (update in `const.py` if your device uses different UUIDs):

- Service UUID: `0000ffe0-0000-1000-8000-00805f9b34fb`
- Read Characteristic: `0000ffe1-0000-1000-8000-00805f9b34fb`
- Write Characteristic: `0000ffe2-0000-1000-8000-00805f9b34fb`

## Customization

### Update Interval

The default update interval is 30 seconds. You can change this in `const.py`:

```python
UPDATE_INTERVAL = 30  # seconds
```

### Data Parsing

The integration includes a basic data parser in `coordinator.py`. You'll need to customize the `_parse_data()` method based on your specific Matson Monitor protocol.

## Scanning for Your Device

To scan for Matson Monitor BLE devices and discover their services/characteristics, you can use:

### On macOS/Linux:
```bash
# Install bleak
pip install bleak

# Run the scanner script (see below)
python scan_matson.py
```

### Scanner Script

Create a file called `scan_matson.py`:

```python
import asyncio
from bleak import BleakScanner, BleakClient

async def scan_devices():
    print("Scanning for Matson devices...")
    devices = await BleakScanner.discover(timeout=10.0)
    
    matson_devices = [d for d in devices if d.name and "Matson" in d.name]
    
    if not matson_devices:
        print("No Matson devices found!")
        return
    
    for device in matson_devices:
        print(f"\nFound: {device.name} ({device.address})")
        print(f"RSSI: {device.rssi} dBm")
        
        try:
            async with BleakClient(device.address) as client:
                print(f"Connected to {device.name}")
                
                for service in client.services:
                    print(f"\nService: {service.uuid}")
                    print(f"  Description: {service.description}")
                    
                    for char in service.characteristics:
                        print(f"  Characteristic: {char.uuid}")
                        print(f"    Properties: {char.properties}")
                        print(f"    Description: {char.description}")
                        
                        if "read" in char.properties:
                            try:
                                value = await client.read_gatt_char(char.uuid)
                                print(f"    Value: {value.hex()} ({value})")
                            except Exception as e:
                                print(f"    Could not read: {e}")
        except Exception as e:
            print(f"Error connecting to {device.name}: {e}")

if __name__ == "__main__":
    asyncio.run(scan_devices())
```

## Troubleshooting

### Device Not Found
- Ensure the device is powered on and in range
- Check that Bluetooth is enabled on your HomeAssistant host
- Try restarting the Bluetooth service

### Connection Issues
- Check the RSSI sensor - weak signal can cause connection problems
- Ensure no other app is connected to the device
- Try restarting the integration

### Debug Logging

Add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.matson_monitor: debug
    bleak: debug
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
