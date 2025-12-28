# MATSON Monitor - Quick Start Guide

## 5 Installation Options

### 🚀 Option 1: Automated Script (Easiest)
```bash
./install.sh
```
Choose your installation method and follow prompts.

---

### 📁 Option 2: Manual Copy (Most Common)

**For Home Assistant OS (via Samba):**
1. Connect to `\\homeassistant.local\config\` (Windows) or `smb://homeassistant.local/config/` (Mac)
2. Navigate to `custom_components/` (create if needed)
3. Create folder: `matson_monitor`
4. Copy these 8 files:
   - `__init__.py`
   - `manifest.json`
   - `config_flow.py`
   - `const.py`
   - `coordinator.py`
   - `sensor.py`
   - `strings.json`
   - `requirements.txt`
5. Restart HomeAssistant

---

### 🔧 Option 3: SSH Installation
```bash
# SSH into Home Assistant
ssh root@homeassistant.local

# Create directory
mkdir -p /config/custom_components/matson_monitor

# Exit and copy files from your computer
scp __init__.py manifest.json config_flow.py const.py coordinator.py sensor.py strings.json requirements.txt \
    root@homeassistant.local:/config/custom_components/matson_monitor/

# Restart HA
ssh root@homeassistant.local 'ha core restart'
```

---

### 🐳 Option 4: Docker Container
```bash
# Copy files into container
docker cp __init__.py homeassistant:/config/custom_components/matson_monitor/
docker cp manifest.json homeassistant:/config/custom_components/matson_monitor/
docker cp config_flow.py homeassistant:/config/custom_components/matson_monitor/
docker cp const.py homeassistant:/config/custom_components/matson_monitor/
docker cp coordinator.py homeassistant:/config/custom_components/matson_monitor/
docker cp sensor.py homeassistant:/config/custom_components/matson_monitor/
docker cp strings.json homeassistant:/config/custom_components/matson_monitor/
docker cp requirements.txt homeassistant:/config/custom_components/matson_monitor/

# Restart container
docker restart homeassistant
```

---

### 📦 Option 5: HACS (Best for Updates)

**Prerequisites:** Create a GitHub repository first

1. Push integration to GitHub
2. Open HACS → Integrations
3. Click ⋮ (menu) → Custom repositories
4. Add your GitHub URL
5. Category: Integration
6. Download and install
7. Restart HomeAssistant

---

## After Installation

### 1. Add Integration
1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"Matson Monitor"**
4. Select your device from the list

### 2. Binding Happens Automatically
- No pairing code needed
- No manual Bluetooth pairing
- Integration handles it automatically

### 3. Sensors Appear
After successful binding, you'll see:
- Signal Strength (RSSI)
- Device-specific sensors (once data is parsed)

---

## Before First Connection

### Test Your Device Connection:
```bash
# Activate virtual environment
source venv/bin/activate

# Run binding test
python test_binding.py
```

This will:
- ✅ Connect to MATSON Monitor
- ✅ Enable notifications
- ✅ Show available services/characteristics
- ✅ Display received data

### Update UUIDs (if needed):
Edit `const.py` with actual UUIDs from test results.

---

## Troubleshooting

### Integration Not Found
- ✅ Check folder name is exactly `matson_monitor` (underscore!)
- ✅ Verify all 8 files are present
- ✅ Restart HomeAssistant

### Can't Connect to Device
- ✅ Close official MATSON app
- ✅ Wake up device (press button)
- ✅ Ensure Bluetooth is enabled in HA

### No Sensors Appear
- ✅ Check HA logs for errors
- ✅ Verify device is bound (check logs for "binding")
- ✅ May need to customize data parsing

---

## File Checklist

**Required in HomeAssistant:**
- [x] `__init__.py`
- [x] `manifest.json`
- [x] `config_flow.py`
- [x] `const.py`
- [x] `coordinator.py`
- [x] `sensor.py`
- [x] `strings.json`
- [x] `requirements.txt`

**NOT needed (testing/docs only):**
- [ ] `scan_matson.py`
- [ ] `test_connection.py`
- [ ] `test_binding.py`
- [ ] `*.md` files
- [ ] `venv/`

---

## Quick Reference

| Task | Command/Action |
|------|---------------|
| Install | Run `./install.sh` or copy files manually |
| Restart HA | Settings → System → Restart |
| Add Integration | Settings → Devices & Services → Add |
| View Logs | Settings → System → Logs |
| Test Device | `python test_binding.py` |
| Enable Debug | Add to `configuration.yaml`, see README |

---

## Getting Help

- 📖 **Full Installation Guide:** `INSTALLATION.md`
- 🔗 **Binding Information:** `BINDING_INFO.md`
- 🐛 **Troubleshooting:** `DISCOVERY_RESULTS.md`
- 📚 **Complete Documentation:** `README.md`

---

## What's Next?

1. **Install** the integration (choose option above)
2. **Restart** HomeAssistant
3. **Add** the integration via UI
4. **Wait** for automatic binding
5. **Customize** sensors as needed
6. **Enjoy** your MATSON Monitor in HomeAssistant! 🎉
