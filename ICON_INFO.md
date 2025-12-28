# MATSON Monitor Integration Icons

## Icon Created! ✅

The integration now has custom icons designed specifically for MATSON Monitor.

## Icon Design

### Visual Elements:
- 🔋 **Battery**: Green gradient showing charge monitoring
- 📶 **Bluetooth Symbol**: Blue gradient for BLE connectivity
- 📡 **Signal Waves**: Orange waves indicating monitoring/communication
- 🎨 **Modern Design**: Gradient fills and rounded corners

### Color Scheme:
- **Green (#4CAF50)**: Battery/Power monitoring
- **Blue (#03A9F4)**: Bluetooth connectivity
- **Orange (#FF9800)**: Active monitoring/alerts
- **Dark background**: For depth and contrast

## Files Created

### 1. `icon.svg` (Integration Icon)
- Location: `custom_components/matson_monitor/icon.svg`
- Size: 24x24 viewBox, scales to any size
- Used in: Devices & Services, Integration cards

### 2. `logo.svg` (Brand Logo)
- Location: `custom_components/matson_monitor/logo.svg`
- Size: 200x200
- Used in: HACS store, Documentation

## How It Appears in HomeAssistant

### Devices & Services Page:
```
┌──────────────────────────┐
│  [Icon]  Matson Monitor  │
│  1 device                │
└──────────────────────────┘
```

### Device Card:
```
┌────────────────────┐
│  [Icon]            │
│  MATSON Monitor    │
│  Connected         │
│  Signal: -65 dBm   │
└────────────────────┘
```

### Integration Card:
```
┌────────────────────┐
│  [Icon] Matson     │
│       Monitor      │
│  Configure         │
└────────────────────┘
```

## Icon Usage

HomeAssistant automatically uses the icon when:
- ✅ `icon.svg` exists in integration directory
- ✅ File is valid SVG
- ✅ ViewBox is defined
- ✅ Uses relative coordinates

The icon will appear:
- Settings → Devices & Services
- Device pages
- Entity cards
- HACS integration list
- Integration badges

## Alternative: Material Design Icon

If you prefer to use a Material Design Icon instead, edit `manifest.json`:

```json
{
  "domain": "matson_monitor",
  "name": "Matson Monitor",
  "icon": "mdi:battery-bluetooth",
  ...
}
```

Available MDI options:
- `mdi:battery-bluetooth` - Battery with Bluetooth
- `mdi:battery-monitor` - Battery monitoring
- `mdi:car-battery` - Automotive battery
- `mdi:battery-charging-wireless` - Wireless charging
- `mdi:gauge` - Gauge/monitoring
- `mdi:monitor-dashboard` - Dashboard monitoring

## Customization

To customize the icon colors, edit the `<defs>` section in `icon.svg`:

```svg
<!-- Change battery color -->
<stop offset="0%" style="stop-color:#YOUR_COLOR"/>

<!-- Change Bluetooth color -->
<stop offset="0%" style="stop-color:#YOUR_COLOR"/>

<!-- Change signal wave color -->
stroke="#YOUR_COLOR"
```

Common color schemes:
- **Dark Mode**: #03A9F4 (blue), #4CAF50 (green)
- **Light Mode**: #1976D2 (dark blue), #388E3C (dark green)
- **Orange Theme**: #FF6F00, #FF9800, #FFA726
- **Purple Theme**: #7B1FA2, #9C27B0, #BA68C8

## Technical Details

### SVG Format:
- Version: SVG 1.1
- ViewBox: 0 0 24 24 (integration), 0 0 200 200 (logo)
- No external dependencies
- Inline gradients
- Compatible with all browsers

### Color Format:
- Hex colors: `#RRGGBB`
- Opacity: 0.0 to 1.0
- Gradients: Linear, defined in `<defs>`

### Rendering:
- Scales infinitely without quality loss
- Renders in light and dark themes
- Adapts to theme colors via `currentColor` (optional)

## Preview

To preview the icon:

### Method 1: Browser
Open `icon.svg` directly in a web browser

### Method 2: HomeAssistant
1. Install the integration
2. Go to Settings → Devices & Services
3. Look for Matson Monitor with the custom icon

### Method 3: SVG Viewer
Use any SVG viewer or editor:
- VS Code (with SVG extension)
- Inkscape
- Adobe Illustrator
- Online: https://www.svgviewer.dev/

## Future Enhancements

Possible icon variations:
- **Charging state**: Add lightning bolt
- **Low battery**: Red color scheme
- **Disconnected**: Grayed out
- **Multiple devices**: Add badge with count

These could be dynamic based on device state!

## Icon License

The icon design is part of the integration and follows the same MIT license.

---

**Icon Design:** Custom SVG  
**Colors:** Green (battery), Blue (bluetooth), Orange (monitoring)  
**Size:** Scalable vector (SVG)  
**Location:** `custom_components/matson_monitor/`
