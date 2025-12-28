"""Sensor platform for Matson Monitor integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MatsonDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class MatsonSensorEntityDescription(SensorEntityDescription):
    """Describes Matson sensor entity."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None


SENSORS: tuple[MatsonSensorEntityDescription, ...] = (
    MatsonSensorEntityDescription(
        key="rssi",
        name="Signal Strength",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("rssi"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Matson Monitor sensors."""
    coordinator: MatsonDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        MatsonSensorEntity(coordinator, entry, description)
        for description in SENSORS
    ]
    
    # Add dynamic sensors based on discovered characteristics
    if coordinator.data:
        for key in coordinator.data.keys():
            if key not in ["rssi", "raw_data"] and not any(s.key == key for s in SENSORS):
                entities.append(
                    MatsonSensorEntity(
                        coordinator,
                        entry,
                        MatsonSensorEntityDescription(
                            key=key,
                            name=key.replace("_", " ").title(),
                            value_fn=lambda data, k=key: data.get(k),
                        ),
                    )
                )
    
    async_add_entities(entities)


class MatsonSensorEntity(CoordinatorEntity[MatsonDataUpdateCoordinator], SensorEntity):
    """Representation of a Matson Monitor sensor."""

    entity_description: MatsonSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MatsonDataUpdateCoordinator,
        entry: ConfigEntry,
        description: MatsonSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.unique_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id)},
            name=entry.title,
            manufacturer="Matson",
            model="Monitor",
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return self.coordinator.data.get(self.entity_description.key)
