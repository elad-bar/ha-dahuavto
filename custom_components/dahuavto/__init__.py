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


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload = hass.config_entries.async_forward_entry_unload

    await hass.data[DATA_VTO].async_remove()

    hass.async_create_task(unload(entry, DOMAIN_BINARY_SENSOR))

    del hass.data[DATA_VTO]

    return True


async def async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
    """Triggered by config entry options updates."""
    hass.data[DATA_VTO].options = entry.options
