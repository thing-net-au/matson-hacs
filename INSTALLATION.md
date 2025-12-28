# MATSON Monitor - HomeAssistant Installation Guide

There are several ways to install this custom integration into HomeAssistant:

## Option 1: Manual Installation (Recommended for Testing)

### Step-by-Step:

1. **Locate your HomeAssistant configuration directory**
   - For Home Assistant OS/Supervised: `/config/`
   - For Docker: Your mapped config volume (usually `/home/homeassistant/.homeassistant/`)
   - For Core installation: `~/.homeassistant/`

2. **Create the custom_components directory** (if it doesn't exist)
   ```bash
   mkdir -p /config/custom_components
   ```

3. **Copy the integration files**
   ```bash
   # From this directory, copy everything to HA
   cp -r /Users/scobber/source/matson-assistant /config/custom_components/matson_monitor
   ```

   **Or manually via File Editor:**
   - Create folder: `/config/custom_components/matson_monitor/`
   - Copy all `.py`, `.json` files into this folder
   - Do NOT copy test scripts, docs, or venv folder

4. **Verify the structure**
   ```
   /config/
   └── custom_components/
       └── matson_monitor/
           ├── __init__.py
           ├── manifest.json
           ├── config_flow.py
           ├── const.py
           ├── coordinator.py
           ├── sensor.py
           ├── strings.json
           └── requirements.txt
   ```

5. **Restart HomeAssistant**
   - Settings → System → Restart
   - Or: `ha core restart` (from SSH)

6. **Add the integration**
   - Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Matson Monitor"
   - Follow the setup wizard

### Access Methods:

**Via SSH/Terminal:**
```bash
# SSH into your Home Assistant
ssh root@homeassistant.local

# Navigate to config
cd /config

# Create directory
mkdir -p custom_components/matson_monitor

# Use File Editor or Samba share to copy files
```

**Via Samba Share:**
1. Connect to `\\homeassistant.local\config\` (Windows)
2. Or `smb://homeassistant.local/config/` (Mac)
3. Navigate to `custom_components/`
4. Create folder `matson_monitor`
5. Copy all integration files

**Via File Editor Add-on:**
1. Install "File Editor" add-on (if not already)
2. Open File Editor
3. Create folder structure
4. Copy/paste each file content manually

**Via Studio Code Server:**
1. Install "Studio Code Server" add-on
2. Open VS Code in browser
3. Navigate to `/config/custom_components/`
4. Upload/create files

---

## Option 2: HACS (Recommended for Long-term)

HACS (Home Assistant Community Store) is the preferred method for custom integrations.

### Prerequisites:
- HACS must be installed in your HomeAssistant
- Integration must be published to a GitHub repository

### Installation Steps:

1. **First, create a GitHub repository**
   ```bash
   # Initialize git in the integration directory
   cd /Users/scobber/source/matson-assistant
   git init
   git add __init__.py manifest.json config_flow.py const.py coordinator.py sensor.py strings.json requirements.txt
   git commit -m "Initial commit: MATSON Monitor integration"
   
   # Create GitHub repo and push
   # (Follow GitHub instructions)
   ```

2. **Add to HACS**
   - Open HomeAssistant → HACS → Integrations
   - Click three dots (top right) → Custom repositories
   - Add your GitHub repository URL
   - Category: "Integration"
   - Click "Add"

3. **Install via HACS**
   - Search for "Matson Monitor" in HACS
   - Click "Download"
   - Restart HomeAssistant

4. **Configure**
   - Settings → Devices & Services → Add Integration
   - Search for "Matson Monitor"

### HACS Benefits:
- ✅ Easy updates
- ✅ Version management
- ✅ Community visibility
- ✅ Automatic dependency handling

---

## Option 3: Docker Volume Mount (for Docker installations)

If running HomeAssistant in Docker:

### Method A: Copy into running container
```bash
# Copy files into container
docker cp /Users/scobber/source/matson-assistant \
  homeassistant:/config/custom_components/matson_monitor

# Restart container
docker restart homeassistant
```

### Method B: Volume mount (before starting container)
```bash
# In your docker-compose.yml or run command
volumes:
  - /path/to/config:/config
  
# Then copy files to /path/to/config/custom_components/matson_monitor/
cp -r /Users/scobber/source/matson-assistant \
  /path/to/config/custom_components/matson_monitor
```

---

## Option 4: Git Clone (Advanced)

For development or auto-updates:

```bash
# SSH into Home Assistant
ssh root@homeassistant.local

# Navigate to custom_components
cd /config/custom_components

# Clone the repository (once you've created it)
git clone https://github.com/yourusername/matson-monitor.git matson_monitor

# To update later
cd /config/custom_components/matson_monitor
git pull
```

---

## Option 5: Automation Script

Create a script to automate installation:

```bash
#!/bin/bash
# install_matson.sh

# Configuration
HA_HOST="homeassistant.local"
HA_CONFIG="/config"
SOURCE_DIR="/Users/scobber/source/matson-assistant"

# Files to copy
FILES="__init__.py manifest.json config_flow.py const.py coordinator.py sensor.py strings.json requirements.txt"

echo "Installing MATSON Monitor integration to HomeAssistant..."

# Create directory
ssh root@$HA_HOST "mkdir -p $HA_CONFIG/custom_components/matson_monitor"

# Copy files
for file in $FILES; do
    echo "Copying $file..."
    scp "$SOURCE_DIR/$file" root@$HA_HOST:$HA_CONFIG/custom_components/matson_monitor/
done

echo "Installation complete! Please restart HomeAssistant."
```

Run with:
```bash
chmod +x install_matson.sh
./install_matson.sh
```

---

## Verification

After installation, verify the integration is recognized:

1. **Check logs for errors**
   - Settings → System → Logs
   - Look for "matson_monitor" entries

2. **Verify integration appears**
   - Settings → Devices & Services → Add Integration
   - Search for "Matson" - should appear in results

3. **Check custom_components**
   ```bash
   # Via SSH
   ls -la /config/custom_components/matson_monitor/
   
   # Should show all integration files
   ```

---

## Quick Reference: File Checklist

Files **REQUIRED** in HomeAssistant:
- ✅ `__init__.py`
- ✅ `manifest.json`
- ✅ `config_flow.py`
- ✅ `const.py`
- ✅ `coordinator.py`
- ✅ `sensor.py`
- ✅ `strings.json`
- ✅ `requirements.txt`

Files **NOT NEEDED** in HomeAssistant:
- ❌ `scan_matson.py` (testing only)
- ❌ `test_connection.py` (testing only)
- ❌ `test_binding.py` (testing only)
- ❌ `README.md` (documentation)
- ❌ `DISCOVERY_RESULTS.md` (documentation)
- ❌ `BINDING_INFO.md` (documentation)
- ❌ `venv/` (virtual environment)

---

## Recommended Path by Setup Type

| HomeAssistant Type | Recommended Method | Access Method |
|-------------------|-------------------|---------------|
| Home Assistant OS | Manual (Samba/File Editor) | Samba Share or File Editor Add-on |
| Supervised | Manual (SSH) | SSH + terminal |
| Container (Docker) | Volume Mount or docker cp | Docker commands |
| Core (Python venv) | Manual (direct copy) | Direct filesystem access |
| Development | Git Clone or symlink | Direct access |

---

## Common Issues

### "Integration not found"
- ✅ Check folder name is exactly `matson_monitor` (underscore, not hyphen)
- ✅ Verify all required files are present
- ✅ Restart HomeAssistant after copying files

### "Invalid manifest"
- ✅ Check `manifest.json` is valid JSON
- ✅ Ensure no extra commas or syntax errors

### "Import failed"
- ✅ Check logs for specific error
- ✅ Verify `bleak` dependency installs correctly
- ✅ Check Python version compatibility (3.11+)

### "Bluetooth not available"
- ✅ Ensure Bluetooth integration is enabled in HA
- ✅ Check Bluetooth adapter is recognized
- ✅ Verify Bluetooth permissions

---

## Next Steps After Installation

1. **Restart HomeAssistant**
2. **Check logs** for any errors
3. **Add Integration**: Settings → Devices & Services → Add Integration
4. **Search** for "Matson Monitor"
5. **Select device** from discovered list
6. **Binding happens automatically**
7. **Sensors appear** in your dashboard

---

## Support

If installation issues occur:
- Check HomeAssistant logs: Settings → System → Logs
- Enable debug logging: See README.md
- Verify file permissions (should be readable by HA user)
- Ensure all files are copied correctly

For development/testing, keep the test scripts in your local directory:
- Use `test_binding.py` to verify device connectivity
- Update `const.py` with discovered UUIDs
- Test locally before deploying to HomeAssistant
