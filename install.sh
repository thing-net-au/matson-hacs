#!/bin/bash
# Quick installation script for MATSON Monitor integration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}MATSON Monitor HomeAssistant Integration Installer${NC}"
echo "========================================================"
echo

# Files to install
FILES="__init__.py manifest.json config_flow.py const.py coordinator.py sensor.py strings.json requirements.txt"

# Detect installation method
echo "Select installation method:"
echo "1) Local installation (direct filesystem access)"
echo "2) SSH to Home Assistant OS"
echo "3) Docker container"
echo "4) Show manual instructions"
echo
read -p "Enter choice [1-4]: " choice

case $choice in
  1)
    # Local installation
    read -p "Enter path to HomeAssistant config directory [/config]: " HA_CONFIG
    HA_CONFIG=${HA_CONFIG:-/config}
    
    TARGET_DIR="$HA_CONFIG/custom_components/matson_monitor"
    
    echo -e "${YELLOW}Installing to: $TARGET_DIR${NC}"
    
    # Create directory
    mkdir -p "$TARGET_DIR"
    
    # Copy files
    for file in $FILES; do
      if [ -f "$file" ]; then
        echo "Copying $file..."
        cp "$file" "$TARGET_DIR/"
      else
        echo -e "${RED}Warning: $file not found${NC}"
      fi
    done
    
    echo -e "${GREEN}Installation complete!${NC}"
    echo "Please restart HomeAssistant to load the integration."
    ;;
    
  2)
    # SSH installation
    read -p "Enter HomeAssistant hostname/IP [homeassistant.local]: " HA_HOST
    HA_HOST=${HA_HOST:-homeassistant.local}
    
    read -p "Enter SSH user [root]: " SSH_USER
    SSH_USER=${SSH_USER:-root}
    
    TARGET_DIR="/config/custom_components/matson_monitor"
    
    echo -e "${YELLOW}Installing to: $SSH_USER@$HA_HOST:$TARGET_DIR${NC}"
    
    # Create directory
    ssh "$SSH_USER@$HA_HOST" "mkdir -p $TARGET_DIR"
    
    # Copy files
    for file in $FILES; do
      if [ -f "$file" ]; then
        echo "Copying $file..."
        scp "$file" "$SSH_USER@$HA_HOST:$TARGET_DIR/"
      else
        echo -e "${RED}Warning: $file not found${NC}"
      fi
    done
    
    echo -e "${GREEN}Installation complete!${NC}"
    echo "Please restart HomeAssistant to load the integration."
    echo "Run: ssh $SSH_USER@$HA_HOST 'ha core restart'"
    ;;
    
  3)
    # Docker installation
    read -p "Enter Docker container name [homeassistant]: " CONTAINER
    CONTAINER=${CONTAINER:-homeassistant}
    
    TARGET_DIR="/config/custom_components/matson_monitor"
    
    echo -e "${YELLOW}Installing to Docker container: $CONTAINER${NC}"
    
    # Create directory in container
    docker exec "$CONTAINER" mkdir -p "$TARGET_DIR"
    
    # Copy files
    for file in $FILES; do
      if [ -f "$file" ]; then
        echo "Copying $file..."
        docker cp "$file" "$CONTAINER:$TARGET_DIR/"
      else
        echo -e "${RED}Warning: $file not found${NC}"
      fi
    done
    
    echo -e "${GREEN}Installation complete!${NC}"
    echo "Restarting container..."
    docker restart "$CONTAINER"
    ;;
    
  4)
    # Manual instructions
    echo -e "${YELLOW}Manual Installation Instructions:${NC}"
    echo
    echo "1. Copy these files to /config/custom_components/matson_monitor/:"
    for file in $FILES; do
      echo "   - $file"
    done
    echo
    echo "2. Via Samba Share:"
    echo "   - Connect to \\\\homeassistant.local\\config\\"
    echo "   - Navigate to custom_components/"
    echo "   - Create folder: matson_monitor"
    echo "   - Copy files listed above"
    echo
    echo "3. Via File Editor Add-on:"
    echo "   - Open File Editor in HomeAssistant"
    echo "   - Create folder: custom_components/matson_monitor"
    echo "   - Create/paste each file"
    echo
    echo "4. Restart HomeAssistant"
    echo "5. Add integration: Settings → Devices & Services → Add Integration"
    echo
    echo "See INSTALLATION.md for detailed instructions."
    ;;
    
  *)
    echo -e "${RED}Invalid choice${NC}"
    exit 1
    ;;
esac

echo
echo -e "${GREEN}Next steps:${NC}"
echo "1. Restart HomeAssistant (if not done automatically)"
echo "2. Go to Settings → Devices & Services"
echo "3. Click '+ Add Integration'"
echo "4. Search for 'Matson Monitor'"
echo "5. Select your MATSON Monitor device"
echo "6. Binding will happen automatically"
echo
echo "For troubleshooting, see INSTALLATION.md and README.md"
