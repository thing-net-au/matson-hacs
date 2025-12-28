# GitHub Repository Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `matson-assistant` (or your preferred name)
3. Description: `HomeAssistant custom integration for MATSON Monitor via BLE with automatic binding`
4. Visibility: Public (required for HACS)
5. ⚠️ Do NOT initialize with README, .gitignore, or license (already created locally)
6. Click "Create repository"

## Step 2: Push to GitHub

```bash
cd /Users/scobber/source/matson-assistant

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/matson-assistant.git

# Or use SSH:
# git remote add origin git@github.com:YOUR_USERNAME/matson-assistant.git

# Push to GitHub
git push -u origin main
```

## Step 3: Create Release (Required for HACS)

### Via GitHub Web Interface:
1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. Description:
   ```
   Initial release of MATSON Monitor HomeAssistant Integration
   
   Features:
   - Automatic Bluetooth Low Energy device discovery
   - Automatic binding (no pairing required)
   - BLE notification support
   - Dynamic sensor entities
   - Auto-reconnection
   - Config flow for easy setup
   
   Installation via HACS or manual copy to custom_components/
   ```
6. Click "Publish release"

### Via Command Line:
```bash
# Create and push tag
git tag -a v1.0.0 -m "Initial release: MATSON Monitor integration"
git push origin v1.0.0
```

Then create release from tag on GitHub web interface.

## Step 4: Add to HACS

### For Users to Install:

1. Open HomeAssistant
2. Go to HACS → Integrations
3. Click ⋮ (three dots menu) → Custom repositories
4. Add repository URL: `https://github.com/YOUR_USERNAME/matson-assistant`
5. Category: Integration
6. Click "Add"
7. Search for "Matson Monitor"
8. Click "Download"
9. Restart HomeAssistant

### Optional: Submit to HACS Default Repository

To make it available without adding custom repository:

1. Fork https://github.com/hacs/default
2. Edit `integration` file
3. Add your repository URL
4. Submit Pull Request
5. Wait for approval (may take time and requires meeting HACS standards)

## Step 5: Repository Settings (Recommended)

### Topics (for discoverability):
- Go to repository → Settings → About
- Add topics:
  - `homeassistant`
  - `home-assistant`
  - `hacs`
  - `bluetooth`
  - `ble`
  - `matson`
  - `custom-component`
  - `custom-integration`

### Enable Issues:
- Settings → Features → ✓ Issues

### Add Description:
- About section: "HomeAssistant custom integration for MATSON Monitor via BLE"
- Website: Your HomeAssistant URL or documentation link

## Repository Structure (What's Included)

```
matson-assistant/
├── custom_components/
│   └── matson_monitor/          # ← HACS installs this folder
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── sensor.py
│       ├── strings.json
│       └── requirements.txt
├── README.md                     # Main documentation
├── INSTALLATION.md               # Installation guide
├── BINDING_INFO.md               # Binding explanation
├── DISCOVERY_RESULTS.md          # Troubleshooting
├── QUICK_START.md                # Quick reference
├── hacs.json                     # HACS metadata
├── LICENSE                       # MIT License
├── .gitignore                    # Git ignore rules
├── scan_matson.py                # Testing utility
├── test_connection.py            # Testing utility
├── test_binding.py               # Testing utility
└── install.sh                    # Installation script
```

## Verification Checklist

Before pushing, verify:
- [x] `hacs.json` exists in repository root
- [x] `custom_components/matson_monitor/` contains all integration files
- [x] `manifest.json` has correct domain and version
- [x] `README.md` has installation instructions
- [x] LICENSE file exists (MIT)
- [x] Repository is public
- [x] At least one release/tag exists (v1.0.0)

## Quick Commands Reference

```bash
# Check remote
git remote -v

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/matson-assistant.git

# Push to GitHub
git push -u origin main

# Create tag
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0

# Check repository status
git status
git log --oneline

# Update after changes
git add .
git commit -m "Update description"
git push
```

## Next Steps After GitHub Setup

1. ✅ Repository created and pushed
2. ✅ Release v1.0.0 created
3. ✅ Add to HACS in HomeAssistant
4. ✅ Test installation via HACS
5. ⏭️ Test device binding with actual MATSON Monitor
6. ⏭️ Update UUIDs in const.py if needed
7. ⏭️ Create v1.1.0 with device-specific updates

## Support

Users can report issues via:
- GitHub Issues: `https://github.com/YOUR_USERNAME/matson-assistant/issues`
- Discussions: Enable GitHub Discussions for Q&A

## Maintenance

For future updates:
```bash
# Make changes to code
git add custom_components/matson_monitor/
git commit -m "Fix: Description of fix"
git push

# Create new release
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0
# Then create release on GitHub from tag
```

HACS users will be notified of updates automatically!
