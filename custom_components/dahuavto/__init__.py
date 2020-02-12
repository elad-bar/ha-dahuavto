"""
This component provides support for WifiBell.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/WifiBell/
"""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD)
from homeassistant.core import HomeAssistant

from .const import *
from .dahuavto_data import DahuaVTOData

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Spotify from a config entry."""
    _LOGGER.debug(f"Starting async_setup_entry of {DOMAIN}")
    entry_data = entry.data

    name = entry_data.get(CONF_NAME)
    host = entry_data.get(CONF_HOST)
    port = entry_data.get(CONF_PORT, DEFAULT_PORT)
    username = entry_data.get(CONF_USERNAME)
    password = entry_data.get(CONF_PASSWORD)

    vto = DahuaVTOData(hass, name, host, port, username, password, entry)

    await vto.initialize()

    hass.data[DATA_VTO] = vto

    return True


async def reload_entry(hass, config_entry):
    """Reload HACS."""
    await async_unload_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Spotify config entry."""
    _LOGGER.debug(f"Starting async_unload_entry of {DOMAIN}")

    # Unload entities for this entry/device.
    await hass.config_entries.async_forward_entry_unload(entry, DOMAIN)

    # Cleanup
    del hass.data[DATA_VTO][entry.entry_id]
    if not hass.data[DATA_VTO]:
        del hass.data[DATA_VTO]

    return True
