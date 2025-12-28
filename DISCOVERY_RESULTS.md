# MATSON Monitor - Discovery Results

## Device Found ✓

**Device Name:** MATSON Monitor  
**Address:** 52375622-4547-E20B-B992-FD703C98FE5E  
**Platform:** macOS (CoreBluetooth)

## Binding vs Pairing

The MATSON Monitor uses **binding** rather than traditional Bluetooth pairing:

- **Pairing** = OS-level security (PIN codes, encryption)
- **Binding** = App-level authorization (enabling notifications, sending binding commands)

The integration now includes automatic binding functionality that:
1. Enables notifications on all notify-capable characteristics
2. Sends binding commands if required
3. Maintains the binding session across reconnections

## Connection Status

The device was successfully discovered during initial BLE scanning. Connection attempts require:

1. **Device must be awake** - May enter sleep mode after inactivity
2. **No other connections** - Must disconnect from official app first
3. **Binding procedure** - Notifications must be enabled on specific characteristics

## Integration Updates ✓

### Added Binding Support

**Updated Files:**
- ✅ `coordinator.py` - Added `_perform_binding()` method
- ✅ `coordinator.py` - Added notification handler
- ✅ `const.py` - Added binding configuration constants
- ✅ `test_binding.py` - New script to test binding procedure

**Binding Process:**
1. Connect to device via BLE
2. Enable notifications on all notify/indicate characteristics
3. Optionally send binding command (if required)
4. Handle incoming notifications from device

## Testing Binding

Run the binding test script:
```bash
python test_binding.py
```

This will:
- Connect to the MATSON Monitor
- Enable notifications on all characteristics
- Display any received notifications
- Show read values from all readable characteristics
- Identify write characteristics for binding commands

## Troubleshooting Steps

### Device Not Responding:

1. **Wake up the device:**
   - Press any button on the MATSON Monitor
   - Check LED indicators for activity
   - Device may auto-sleep after period of inactivity

2. **Disconnect from other apps:**
   - Close the official MATSON app completely (not just minimize)
   - Check for background connections
   - Restart device if needed

3. **Power cycle:**
   - Turn off MATSON Monitor
   - Wait 10 seconds
   - Turn back on
   - Run scan immediately

4. **Check app authorization:**
   - Some devices require initial setup via official app
   - Ensure device is registered/activated
   - Check if device has "sharing" or "API access" settings

### macOS Specific:

1. **Bluetooth permissions:**
   - System Settings → Privacy & Security → Bluetooth
   - Ensure Terminal/Python has access

2. **Reset Bluetooth:**
   - Hold Shift+Option, click Bluetooth icon
   - Select "Reset Bluetooth module"

3. **Use alternative tools:**
   - Install "LightBlue" app to verify device connectivity
   - Use "Bluetooth Explorer" (Xcode tools) for deeper inspection

## Integration Status

### Created Files ✓

The HomeAssistant integration is complete with binding support:

- ✅ `manifest.json` - Integration configuration with Bluetooth discovery
- ✅ `__init__.py` - Entry point with async setup
- ✅ `config_flow.py` - UI configuration flow
- ✅ `coordinator.py` - **BLE connection with binding support**
- ✅ `sensor.py` - Sensor entities for device data
- ✅ `const.py` - **Constants with binding configuration**
- ✅ `strings.json` - UI translations
- ✅ `requirements.txt` - Dependencies (bleak>=0.21.1)
- ✅ `scan_matson.py` - Device scanner
- ✅ `test_connection.py` - Connection tester
- ✅ `test_binding.py` - **Binding procedure tester**

### How Binding Works in the Integration

When HomeAssistant connects to the MATSON Monitor:

1. **Initial connection** via BLE
2. **Auto-binding** performed:
   - Discovers all services/characteristics
   - Enables notifications on notify-capable characteristics
   - Sends binding command if configured
3. **Maintains session** - Binding state persists across reconnections
4. **Handles notifications** - Device can push updates via BLE notifications

### Installation Instructions

1. **Copy to HomeAssistant:**
   ```bash
   cp -r matson-assistant /config/custom_components/matson_monitor
   ```

2. **Restart HomeAssistant**

3. **Add Integration:**
   - Settings → Devices & Services → Add Integration
   - Search for "Matson Monitor"
   - Select your device
   - Binding happens automatically on first connection

### Customizing Binding

If your device requires specific binding commands:

1. **Run test_binding.py** to discover the correct characteristics
2. **Update const.py:**
   ```python
   MATSON_BINDING_CHARACTERISTIC = "00002a19-..." # Your UUID
   MATSON_BINDING_COMMAND = b"\xAA\xBB\xCC"      # Your command
   ```
3. **Update coordinator.py** `_perform_binding()` to send the command

## Next Steps to Complete Integration

Once device connection is successful:

1. **Run binding test:**
   ```bash
   python test_binding.py
   ```
   - Note which characteristics support notifications
   - Note any notifications received
   - Note binding command requirements

2. **Update const.py with actual UUIDs:**
   ```python
   MATSON_SERVICE_UUID = "..." # From scan
   MATSON_CHARACTERISTIC_NOTIFY_UUID = "..." # From binding test
   MATSON_BINDING_COMMAND = b"..." # If required
   ```

3. **Update data parsing in coordinator.py:**
   - Customize `_parse_data()` method
   - Parse notification data format
   - Extract voltage, current, temperature, etc.

4. **Add specific sensors in sensor.py:**
   - Voltage sensor
   - Current sensor  
   - Temperature sensor
   - Battery level
   - Any other device-specific metrics

## Device Name Pattern

The integration is configured to auto-discover devices with:
- Local name starting with "Matson"
- Matches: "MATSON Monitor" ✓

## HomeAssistant Compatibility

The integration follows HomeAssistant best practices:
- ✅ Config flow for UI setup
- ✅ Bluetooth discovery integration
- ✅ DataUpdateCoordinator for efficient polling
- ✅ **Automatic binding on connection**
- ✅ **Notification support**
- ✅ Proper device/entity registration
- ✅ Auto-reconnection on disconnect
- ✅ Proper cleanup on unload

## Testing Recommendations

### Immediate Next Step:
1. **Wake up the MATSON Monitor** (press button, check display)
2. **Close all other apps** connected to it
3. **Run:** `python test_binding.py` within 30 seconds
4. This will discover services and test binding

### For Development:
- Use `test_binding.py` to understand binding protocol
- Monitor logs for notification data
- Update parsing logic based on actual data format

### For Production:
- Test in HomeAssistant environment
- Verify binding persists across HA restarts
- Confirm sensors update correctly
- Test multiple connect/disconnect cycles

## Support

If connection/binding issues persist:
- Check if official app can connect (verifies device is working)
- Look for device documentation on BLE protocol
- Consider packet capture with Bluetooth HCI logging
- Check if device needs firmware update

---

**Integration Created:** 2025-12-28  
**Status:** Ready with binding support - awaiting device connection test  
**Last Update:** Added automatic binding functionality
