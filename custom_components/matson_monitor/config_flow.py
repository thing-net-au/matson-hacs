"""Config flow for Matson Monitor integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import bluetooth
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MatsonMonitorConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Matson Monitor."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        _LOGGER.info(
            "Auto-discovered Matson Monitor via Bluetooth: %s (%s)", 
            discovery_info.name, 
            discovery_info.address
        )
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        
        self._discovery_info = discovery_info
        
        # Automatically create entry without user confirmation
        return self.async_create_entry(
            title=discovery_info.name or f"Matson Monitor {discovery_info.address[-5:]}",
            data={},
        )



    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step to pick discovered device."""
        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            discovery_info = self._discovered_devices[address]
            
            return self.async_create_entry(
                title=discovery_info.name or address,
                data={},
            )
        
        current_addresses = self._async_current_ids()
        discovered_devices = await bluetooth.async_discovered_service_info(self.hass)
        
        self._discovered_devices = {
            service_info.address: service_info
            for service_info in discovered_devices
            if service_info.address not in current_addresses
            and service_info.name
            and (service_info.name.startswith("Matson") or service_info.name.startswith("MATSON"))
        }
        
        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): vol.In(
                        {
                            address: f"{service_info.name} ({address})"
                            for address, service_info in self._discovered_devices.items()
                        }
                    )
                }
            ),
        )


import voluptuous as vol
