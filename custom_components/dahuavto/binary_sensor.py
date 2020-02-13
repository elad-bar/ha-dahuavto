"""
Support for Blue Iris binary sensors.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.blueiris/
"""
import sys
import logging
from typing import Optional

from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from homeassistant.helpers.entity import Entity

from custom_components.dahuavto import DahuaVTOData
from .const import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the HP Printer Binary Sensor."""
    _LOGGER.debug(f"Starting async_setup_entry")

    try:
        vto = hass.data[DATA_VTO]

        entity_available = VTOBinarySensor(hass, vto, SENSOR_TYPE_RING)
        entity_ring = VTOBinarySensor(hass, vto, SENSOR_TYPE_AVAILABLE)

        async_add_devices([entity_available, entity_ring], True)
    except Exception as ex:
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno

        _LOGGER.error(f"Failed to load BlueIris Binary Sensors, error: {ex}, line: {line_number}")


class VTOBinarySensor(Entity):
    """Representation a binary sensor that is updated by MQTT."""

    def __init__(self, hass, vto: DahuaVTOData, sensor_type):
        """Initialize the HP Printer Binary Sensor."""
        self._hass = hass
        self._vto = vto
        self._sensor_type = sensor_type
        self._binary_sensor = self._vto.get_sensor_data(self._sensor_type)
        self._remove_dispatcher = None

    @property
    def unique_id(self) -> Optional[str]:
        """Return the name of the node."""
        return f"{DEFAULT_NAME}-{DOMAIN}-{self.name}"

    @property
    def device_info(self):
        return {
            "identifiers": {
                (DOMAIN, self.unique_id)
            },
            "name": self.name,
            "manufacturer": MANUFACTURER,
            ENTITY_MODEL: self._binary_sensor.get(ENTITY_MODEL)
        }

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return self._binary_sensor.get(ENTITY_NAME)

    @property
    def icon(self) -> Optional[str]:
        """Return the icon of the sensor."""
        return self._binary_sensor.get(ENTITY_ICON)

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self._binary_sensor.get(ENTITY_STATE, False))

    @property
    def state(self):
        """Return the state of the binary sensor."""
        return STATE_ON if self.is_on else STATE_OFF

    @property
    def device_state_attributes(self):
        """Return true if the binary sensor is on."""
        return self._binary_sensor.get(ENTITY_ATTRIBUTES)

    async def async_added_to_hass(self):
        """Register callbacks."""
        self._remove_dispatcher = async_dispatcher_connect(self._hass, SIGNAL_UPDATE_VTO, self.update_data)

    async def async_will_remove_from_hass(self) -> None:
        if self._remove_dispatcher is not None:
            self._remove_dispatcher()

    @callback
    def update_data(self):
        _LOGGER.debug(f"update_data: {self.name} | {self.unique_id}")

        self._binary_sensor = self._vto.get_sensor_data(self._sensor_type)

        self.async_schedule_update_ha_state(True)
