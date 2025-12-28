"""Constants for the Matson Monitor integration."""

DOMAIN = "matson_monitor"

# BLE Service and Characteristic UUIDs (update these with actual Matson Monitor UUIDs)
MATSON_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
MATSON_CHARACTERISTIC_READ_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
MATSON_CHARACTERISTIC_WRITE_UUID = "0000ffe2-0000-1000-8000-00805f9b34fb"
MATSON_CHARACTERISTIC_NOTIFY_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# Binding configuration
# Update these with actual binding command if known
MATSON_BINDING_CHARACTERISTIC = "0000ffe2-0000-1000-8000-00805f9b34fb"
MATSON_BINDING_COMMAND = b"\x01\x02"  # Placeholder - update with actual binding command

# Update interval
UPDATE_INTERVAL = 30  # seconds

# Device name patterns
DEVICE_NAME_PREFIX = "Matson"
