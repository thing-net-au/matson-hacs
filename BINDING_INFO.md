# MATSON Monitor Binding Process

## What is Binding?

The MATSON Monitor uses **binding** instead of traditional Bluetooth pairing. This is an application-level authorization process, not an OS-level security feature.

### Binding vs Pairing

| Feature | Pairing | Binding |
|---------|---------|---------|
| Level | Operating System | Application |
| Security | PIN/encryption | Session authorization |
| Visibility | Shows in OS Bluetooth settings | Invisible to OS |
| Process | User interaction required | Automatic in app |
| Persistence | Survives reboots | May require refresh |

## How Binding Works

1. **BLE Connection**: App connects to device via Bluetooth Low Energy
2. **Service Discovery**: App discovers available GATT services and characteristics
3. **Enable Notifications**: App enables notifications on specific characteristics
4. **Optional Command**: Some devices require a binding command to be sent
5. **Session Active**: Device now sends data via notifications

## MATSON Monitor Binding

The HomeAssistant integration automatically handles binding:

### On First Connection:
```python
# coordinator.py _perform_binding() method
1. Connect to device
2. Discover all services/characteristics
3. Enable notifications on all notify-capable characteristics
4. Send binding command (if configured)
5. Register notification handler
```

### Notification Handler:
```python
def _notification_handler(sender: int, data: bytearray):
    # Receives real-time data from device
    # Updates sensor values immediately
```

## Testing Binding

Use the included test script to verify binding:

```bash
python test_binding.py
```

This will:
- Connect to the MATSON Monitor
- Enable notifications on all characteristics
- Display any received notifications
- Show the binding process in detail

## Customizing Binding

If your device requires a specific binding command:

### 1. Update const.py:
```python
MATSON_BINDING_CHARACTERISTIC = "your-uuid-here"
MATSON_BINDING_COMMAND = b"\xAA\xBB\xCC"  # Your command bytes
```

### 2. Update coordinator.py _perform_binding():
```python
async def _perform_binding(self) -> None:
    # Enable notifications
    await self._client.start_notify(
        MATSON_CHARACTERISTIC_NOTIFY_UUID,
        self._notification_handler
    )
    
    # Send binding command
    await self._client.write_gatt_char(
        MATSON_BINDING_CHARACTERISTIC,
        MATSON_BINDING_COMMAND
    )
```

## Troubleshooting Binding

### Device Won't Connect
- **Close other apps**: Only one app can bind at a time
- **Wake device**: May be in sleep mode
- **Power cycle**: Reset the device completely

### Notifications Not Received
- **Check UUID**: Ensure correct notification characteristic UUID
- **Verify properties**: Characteristic must support "notify" or "indicate"
- **Check logs**: Look for notification handler calls in HA logs

### Binding Lost After Disconnect
- **Normal behavior**: Some devices require re-binding
- **Auto-handled**: Integration re-binds on reconnection
- **Check _is_bound flag**: Tracks binding state

## Official App Comparison

The official MATSON app performs the same binding:
1. Connects via BLE
2. Enables notifications
3. May send authorization command
4. Receives data via notifications

Our integration replicates this process automatically.

## Debug Logging

Enable debug logging in HomeAssistant:

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.matson_monitor: debug
    bleak: debug
```

Look for:
- `"Performing binding with Matson Monitor"`
- `"Notifications enabled on {uuid}"`
- `"Notification from handle {handle}: {data}"`

## Advanced: Packet Capture

To reverse-engineer the binding protocol:

### On macOS:
1. Enable HCI logging (requires developer tools)
2. Capture packets while official app connects
3. Analyze binding sequence

### On Linux:
```bash
# Capture BLE packets
sudo btmon > ble_capture.log

# In another terminal
python test_binding.py

# Analyze the log for binding commands
```

### On Android:
1. Enable "Bluetooth HCI snoop log" in Developer Options
2. Connect with official app
3. Pull and analyze /sdcard/btsnoop_hci.log with Wireshark

## References

- BLE GATT Specification: [Bluetooth.org](https://www.bluetooth.com/specifications/gatt/)
- Bleak Documentation: [GitHub](https://github.com/hbldh/bleak)
- HomeAssistant Bluetooth: [Docs](https://www.home-assistant.io/integrations/bluetooth/)
