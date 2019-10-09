"""
This component provides support for WifiBell.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/WifiBell/
"""
import logging
import sys

import voluptuous as vol
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD)

from homeassistant.helpers import config_validation as cv

from .const import *
from .dahuavto_data import DahuaVTOData

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up an Wifi Bell component."""

    try:
        conf = config[DOMAIN]

        name = conf.get(CONF_NAME)
        host = conf.get(CONF_HOST)
        port = conf.get(CONF_PORT, DEFAULT_PORT)
        username = conf.get(CONF_USERNAME)
        password = conf.get(CONF_PASSWORD)

        wifi_bell_data = DahuaVTOData(hass, name, host, port, username, password)

        hass.data[DATA_VTO] = wifi_bell_data

        return True

    except Exception as ex:
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno

        _LOGGER.error(f'Error while initializing Dahua VTO, Exception: {str(ex)}, Line: {line_number}')

        hass.components.persistent_notification.create(
            f'Error: {str(ex)}<br />You will need to restart hass after fixing.',
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID)

        return False
