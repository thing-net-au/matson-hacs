"""DataUpdateCoordinator for Matson Monitor."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from bleak import BleakClient, BleakError
from bleak.backends.device import BLEDevice

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, MATSON_SERVICE_UUID, MATSON_CHARACTERISTIC_READ_UUID, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class MatsonDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Matson Monitor data."""

    def __init__(self, hass: HomeAssistant, ble_device: BLEDevice) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._ble_device = ble_device
        self._client: BleakClient | None = None
        self._expected_disconnect = False
        self._is_bound = False

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the Matson Monitor."""
        try:
            if self._client is None or not self._client.is_connected:
                await self._connect()
            
            data = await self._read_data()
            return data
            
        except (BleakError, Exception) as err:
            _LOGGER.error("Error communicating with device: %s", err)
            if self._client and self._client.is_connected:
                await self._disconnect()
            raise UpdateFailed(f"Error communicating with device: {err}") from err

    async def _connect(self) -> None:
        """Connect to the device."""
        _LOGGER.info("Connecting to %s", self._ble_device.address)
        
        self._expected_disconnect = False
        self._client = BleakClient(
            self._ble_device,
            disconnected_callback=self._on_disconnect,
            timeout=30.0,
        )
        
        await self._client.connect()
        _LOGGER.info("Connected to %s", self._ble_device.address)
        
        # Wait for connection to stabilize
        import asyncio
        await asyncio.sleep(1)
        
        # Verify still connected
        if not self._client.is_connected:
            raise BleakError("Device disconnected immediately after connection")
        
        # Perform binding if not already bound
        if not self._is_bound:
            _LOGGER.info("Performing binding for %s", self._ble_device.address)
            await self._perform_binding()
            self._is_bound = True
            _LOGGER.info("Binding completed for %s", self._ble_device.address)

    async def _disconnect(self) -> None:
        """Disconnect from the device."""
        if self._client and self._client.is_connected:
            self._expected_disconnect = True
            await self._client.disconnect()
            _LOGGER.debug("Disconnected from %s", self._ble_device.address)

    @callback
    def _on_disconnect(self, client: BleakClient) -> None:
        """Handle device disconnect."""
        if self._expected_disconnect:
            _LOGGER.debug("Expected disconnect from %s", self._ble_device.address)
            return
        
        _LOGGER.warning("Unexpected disconnect from %s", self._ble_device.address)
        self._client = None

    async def _read_data(self) -> dict[str, Any]:
        """Read data from the Matson Monitor."""
        import asyncio
        
        if not self._client or not self._client.is_connected:
            _LOGGER.warning("Not connected to device, attempting reconnection...")
            raise UpdateFailed("Not connected to device")
        
        data: dict[str, Any] = {}
        
        try:
            # Read all services and characteristics
            services = self._client.services
            
            for service in services:
                _LOGGER.debug("Service: %s", service.uuid)
                
                for char in service.characteristics:
                    _LOGGER.debug("  Characteristic: %s (Properties: %s)", 
                                char.uuid, char.properties)
                    
                    if "read" in char.properties:
                        try:
                            # Check connection before each read
                            if not self._client.is_connected:
                                _LOGGER.warning("Lost connection during data read")
                                raise UpdateFailed("Connection lost during read")
                            
                            value = await self._client.read_gatt_char(char.uuid)
                            data[char.uuid] = value
                            _LOGGER.debug("    Read value: %s", value.hex())
                            await asyncio.sleep(0.1)  # Small delay between reads
                        except Exception as err:
                            _LOGGER.debug("    Could not read %s: %s", char.uuid, err)
            
            # Parse the data based on Matson Monitor protocol
            parsed_data = self._parse_data(data)
            
            return parsed_data
            
        except Exception as err:
            _LOGGER.error("Error reading data: %s", err)
            raise UpdateFailed(f"Error reading data: {err}") from err

    def _parse_data(self, raw_data: dict[str, bytes]) -> dict[str, Any]:
        """Parse raw data from the device."""
        parsed: dict[str, Any] = {
            "raw_data": {uuid: value.hex() for uuid, value in raw_data.items()},
            "rssi": self._ble_device.rssi if hasattr(self._ble_device, 'rssi') else None,
        }
        
        # Add parsing logic specific to Matson Monitor data format
        # This is a placeholder - update with actual protocol parsing
        for uuid, value in raw_data.items():
            if len(value) > 0:
                # Example: Parse as integers, strings, etc. based on the protocol
                try:
                    # Try to decode as UTF-8 string
                    parsed[f"data_{uuid.split('-')[0]}"] = value.decode('utf-8').strip('\x00')
                except UnicodeDecodeError:
                    # If not a string, store as hex
                    parsed[f"data_{uuid.split('-')[0]}"] = value.hex()
        
        return parsed

    async def async_write_data(self, characteristic_uuid: str, data: bytes) -> None:
        """Write data to a characteristic."""
        if not self._client or not self._client.is_connected:
            await self._connect()
        
        try:
            await self._client.write_gatt_char(characteristic_uuid, data)
            _LOGGER.debug("Wrote data to %s: %s", characteristic_uuid, data.hex())
        except Exception as err:
            _LOGGER.error("Error writing data: %s", err)
            raise

    async def _perform_binding(self) -> None:
        """Perform binding with the Matson Monitor device."""
        import asyncio
        
        _LOGGER.info("Starting binding procedure with Matson Monitor")
        
        try:
            # Wait a moment for device to be ready
            await asyncio.sleep(0.5)
            
            # Check if still connected
            if not self._client.is_connected:
                _LOGGER.error("Device disconnected before binding could start")
                raise BleakError("Device disconnected during binding setup")
            
            # Discover services
            _LOGGER.debug("Discovering services...")
            services = self._client.services
            _LOGGER.info("Found %d services", len(services))
            
            # Enable notifications on notify-capable characteristics
            notifications_enabled = 0
            for service in services:
                _LOGGER.debug("Service: %s", service.uuid)
                for char in service.characteristics:
                    if "notify" in char.properties or "indicate" in char.properties:
                        _LOGGER.info("Enabling notifications on %s", char.uuid)
                        try:
                            await self._client.start_notify(char.uuid, self._notification_handler)
                            await asyncio.sleep(0.2)  # Small delay between notifications
                            notifications_enabled += 1
                            _LOGGER.info("✓ Notifications enabled on %s", char.uuid)
                        except Exception as err:
                            _LOGGER.warning("Could not enable notifications on %s: %s", char.uuid, err)
            
            _LOGGER.info("Enabled notifications on %d characteristics", notifications_enabled)
            
            # Give device time to process binding
            await asyncio.sleep(1)
            
            # Verify still connected after binding
            if not self._client.is_connected:
                _LOGGER.error("Device disconnected during binding")
                raise BleakError("Device disconnected during binding")
            
            _LOGGER.info("✓ Binding completed successfully")
            
        except Exception as err:
            _LOGGER.error("✗ Error during binding: %s", err)
            raise
    
    @callback
    def _notification_handler(self, sender: int, data: bytearray) -> None:
        """Handle BLE notifications from the device."""
        _LOGGER.debug("Notification from handle %s: %s", sender, data.hex())
        # Handle notifications and update data as needed
        # This will be called when the device sends notifications

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        await self._disconnect()
