# MATSON Monitor - Automatic Discovery

## ✅ Automatic Discovery is ENABLED!

Your MATSON Monitor integration now **automatically discovers and adds devices** without any user interaction!

## How It Works

### 1. Background Scanning
HomeAssistant continuously scans for Bluetooth devices in the background.

### 2. Pattern Matching
The integration looks for devices with names matching:
- `Matson*` (any name starting with "Matson")
- `MATSON*` (any name starting with "MATSON")

This is configured in `manifest.json`:
```json
"bluetooth": [
  {
    "local_name": "Matson*"
  },
  {
    "local_name": "MATSON*"
  }
]
```

### 3. Automatic Addition
When a matching device is found:
1. ✅ Device is **automatically discovered**
2. ✅ Entry is **created automatically** (no confirmation needed)
3. ✅ Device appears in **Devices & Services**
4. ✅ Binding happens **automatically**
5. ✅ Sensors are **created automatically**

### 4. Notification
You'll see a notification in HomeAssistant:
> "New device discovered: MATSON Monitor"

Click "Configure" or it will configure itself automatically!

## What Gets Created

When a MATSON Monitor is discovered, HomeAssistant automatically creates:

- **Device Entry**: Shows in Devices & Services
- **Sensors**: 
  - Signal Strength (RSSI)
  - Additional sensors from device data
- **Binding**: Automatic BLE binding (no pairing needed)

## Discovery Process Flow

```
Bluetooth Scan
    ↓
Device Found: "MATSON Monitor"
    ↓
Check: Already configured?
    ↓ No
Create config entry automatically
    ↓
Connect & Bind
    ↓
Create sensors
    ↓
Device ready! ✅
```

## Behavior Changes in v1.0.1

### Before (v1.0.0):
- Device discovered
- **User had to confirm** "Do you want to add this device?"
- User clicks "Submit"
- Device added

### Now (v1.0.1):
- Device discovered
- **Automatically added** (no user interaction)
- Notification shown
- Device ready immediately ✅

## Multiple Devices

The integration supports **multiple MATSON Monitors**:

- Each device is identified by its Bluetooth address
- Each gets its own entry in Devices & Services
- Each has independent sensors
- Each maintains its own binding

Example:
- MATSON Monitor (Kitchen) - AA:BB:CC:DD:EE:01
- MATSON Monitor (Garage) - AA:BB:CC:DD:EE:02
- MATSON Monitor (RV) - AA:BB:CC:DD:EE:03

All discovered and added automatically!

## Manual Addition

You can still manually add devices:

1. Go to **Settings → Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"Matson Monitor"**
4. Select from list of discovered devices
5. Click "Submit"

This is useful if:
- Auto-discovery notification was dismissed
- You want to review devices before adding
- Device was out of range during initial scan

## Discovery Requirements

For automatic discovery to work:

### ✅ HomeAssistant Requirements:
- Bluetooth integration enabled
- Bluetooth adapter detected
- Bluetooth permissions granted

### ✅ Device Requirements:
- MATSON Monitor powered on
- Bluetooth enabled on device
- In range of HomeAssistant's Bluetooth adapter
- Name starts with "Matson" or "MATSON"
- Not already configured

### ✅ Integration Requirements:
- MATSON Monitor integration installed
- Version 1.0.1 or higher

## Troubleshooting Discovery

### Device Not Auto-Discovered

**Check Bluetooth:**
```
Settings → System → Hardware
Look for Bluetooth adapter
```

**Check Logs:**
```
Settings → System → Logs
Search for: "matson_monitor"
Look for: "Auto-discovered Matson Monitor"
```

**Enable Debug Logging:**
```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.matson_monitor: debug
    homeassistant.components.bluetooth: debug
```

**Manually Trigger Discovery:**
1. Restart HomeAssistant
2. Go to Settings → Devices & Services
3. Click "+ Add Integration"
4. Search "Matson Monitor"
5. Should show discovered devices

### Device Shows But Won't Connect

This is different from discovery - the device is found but binding fails:

- Close official MATSON app
- Wake up the device
- Power cycle the device
- Check MATSON Monitor is not connected to another device

See BINDING_INFO.md for binding troubleshooting.

### Multiple Discovery Notifications

If you see multiple notifications for the same device:
- This is normal if the device reconnects
- HomeAssistant will recognize it's already configured
- No duplicate entries will be created
- Safe to dismiss extra notifications

## Discovery Logs

When a device is discovered, you'll see in logs:

```
[custom_components.matson_monitor.config_flow] Auto-discovered Matson Monitor via Bluetooth: MATSON Monitor (52375622-4547-E20B-B992-FD703C98FE5E)
[homeassistant.config_entries] Setting up matson_monitor.52375622-4547-E20B-B992-FD703C98FE5E
[custom_components.matson_monitor] Setting up Matson Monitor integration
[custom_components.matson_monitor.coordinator] Connecting to 52375622-4547-E20B-B992-FD703C98FE5E
[custom_components.matson_monitor.coordinator] Connected to 52375622-4547-E20B-B992-FD703C98FE5E
[custom_components.matson_monitor.coordinator] Performing binding with Matson Monitor
[custom_components.matson_monitor.coordinator] Binding completed successfully
```

## Disabling Auto-Discovery

If you want to disable automatic discovery (not recommended):

### Option 1: Ignore Discovery
- When notification appears, click "Ignore"
- Device will not be added
- Notification won't appear again for this device

### Option 2: Disable Integration
- Settings → Devices & Services
- Find "Matson Monitor" integration
- Click "..." → Disable
- No new devices will be discovered

### Option 3: Remove Integration
- Uninstall the integration completely
- No devices will be discovered or monitored

## Testing Discovery

To test if discovery is working:

1. **Ensure device is on and in range**
2. **Check Bluetooth is working:**
   ```
   Settings → System → Hardware → Bluetooth
   ```
3. **Restart HomeAssistant**
4. **Check notifications** (bell icon, top right)
5. **Check logs** for "Auto-discovered Matson Monitor"

You can also use the test script:
```bash
cd /Users/scobber/source/matson-assistant
source venv/bin/activate
python scan_matson.py
```

This shows if the device is visible via Bluetooth.

## Advanced: Discovery Internals

The integration uses HomeAssistant's Bluetooth integration:

1. **manifest.json** declares Bluetooth matcher:
   - Matches any device with local_name "Matson*" or "MATSON*"

2. **config_flow.py** handles discovery:
   - `async_step_bluetooth()` called when device matches
   - Creates config entry automatically
   - No user confirmation needed

3. **__init__.py** sets up the device:
   - Creates coordinator
   - Connects and binds
   - Creates sensors

All automatic! 🚀

## Summary

- ✅ **Fully automatic** discovery and setup
- ✅ **No user interaction** required
- ✅ **Multiple devices** supported
- ✅ **Binding automatic** on discovery
- ✅ **Sensors created** automatically
- ✅ **Works in background** continuously

Just power on your MATSON Monitor and it will appear in HomeAssistant! 🎉

---

**Version:** 1.0.1  
**Feature:** Automatic discovery and setup  
**User Action Required:** None! ✨
