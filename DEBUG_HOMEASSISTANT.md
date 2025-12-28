# Debugging Config Flow 500 Error

You're getting: **"Config flow could not be loaded: 500 Internal Server Error"**

This means HomeAssistant is hitting an error when trying to import the config flow.

## Step 1: Check HomeAssistant Logs

### Via UI:
1. Settings → System → Logs
2. Click "Load Full Home Assistant Log"
3. Search for: `matson_monitor`
4. Look for error messages

### Via Command Line:
```bash
# View recent logs
tail -100 /config/home-assistant.log | grep matson

# Or full log
cat /config/home-assistant.log | grep -A 5 -B 5 matson_monitor
```

## Step 2: Common Issues

### Issue 1: Cached Old Version
HomeAssistant may be using cached Python files.

**Fix:**
```bash
# SSH into HomeAssistant
cd /config/custom_components/matson_monitor
rm -rf __pycache__/
# Then restart HA
```

### Issue 2: Files Not Updated
HACS might not have updated all files.

**Fix:**
1. HACS → Integrations
2. Find "Matson Monitor"
3. Click ⋮ → Redownload
4. Restart HomeAssistant

OR manually:
```bash
cd /config/custom_components
rm -rf matson_monitor
# Re-download from GitHub
```

### Issue 3: Python Version
Integration requires Python 3.11+

**Check:**
```bash
python3 --version
```

### Issue 4: Dependencies Missing
The integration needs `bleak`.

**Fix:**
Usually auto-installed, but check:
```bash
pip list | grep bleak
```

## Step 3: Fresh Install

Try a completely fresh installation:

```bash
# SSH into HomeAssistant
cd /config/custom_components

# Backup old version
mv matson_monitor matson_monitor.backup

# Download fresh copy
cd /config/custom_components
git clone https://github.com/thing-net-au/matson-hacs.git
cp -r matson-hacs/custom_components/matson_monitor .
rm -rf matson-hacs

# Restart HomeAssistant
ha core restart
```

## Step 4: Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.matson_monitor: debug
    homeassistant.config_entries: debug
    homeassistant.loader: debug
```

Restart and check logs again.

## Step 5: Verify File Contents

Check the config_flow.py file on your HomeAssistant:

```bash
head -20 /config/custom_components/matson_monitor/config_flow.py
```

Should show:
```python
"""Config flow for Matson Monitor integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components import bluetooth
...
```

If `import voluptuous as vol` is NOT on line 7, the file wasn't updated!

## Step 6: Check GitHub Version

Verify the GitHub repo has the fix:
https://github.com/thing-net-au/matson-hacs/blob/main/custom_components/matson_monitor/config_flow.py

Line 7 should be: `import voluptuous as vol`

## Step 7: Manual File Update

If HACS isn't updating, manually copy the file:

```bash
# Download latest config_flow.py
curl -o /config/custom_components/matson_monitor/config_flow.py \
  https://raw.githubusercontent.com/thing-net-au/matson-hacs/main/custom_components/matson_monitor/config_flow.py

# Restart
ha core restart
```

## Quick Fix Commands

Try these in order:

```bash
# 1. Clear cache
cd /config/custom_components/matson_monitor
rm -rf __pycache__/
ha core restart

# 2. Redownload via HACS
# (Use UI: HACS → Matson Monitor → Redownload)

# 3. Manual update
curl -o /config/custom_components/matson_monitor/config_flow.py \
  https://raw.githubusercontent.com/thing-net-au/matson-hacs/main/custom_components/matson_monitor/config_flow.py
ha core restart

# 4. Fresh install
cd /config/custom_components
rm -rf matson_monitor
# Then reinstall via HACS
```

## Expected Log Output (When Working)

When config flow loads successfully, you should see:
```
[homeassistant.loader] Loaded matson_monitor from custom_components.matson_monitor
[custom_components.matson_monitor] Setting up Matson Monitor integration
```

## Still Not Working?

Share these details:
1. HomeAssistant version
2. Full error from logs (Settings → System → Logs)
3. Output of: `ls -la /config/custom_components/matson_monitor/`
4. Output of: `head -10 /config/custom_components/matson_monitor/config_flow.py`

---

**Most Common Fix:** Clear `__pycache__` and restart HomeAssistant!
