
import sys
from datetime import datetime
import logging

import requests
from requests.auth import HTTPBasicAuth

from homeassistant.const import (STATE_ON, STATE_OFF)
from homeassistant.helpers.event import async_call_later, async_track_time_interval
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.util import slugify

from .const import *

REQUIREMENTS = ['aiohttp']

_LOGGER = logging.getLogger(__name__)


class DahuaVTOData(object):
    """The Class for handling the data retrieval."""

    def __init__(self, hass, name, host, port, username, password, config_entry):
        """Initialize the data object."""
        self._name = name
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self._attributes = {}
        self._is_ringing = False
        self._hass = hass

        self._auth = None
        self._connected = False
        self._updating = False
        self._stopped = False
        self._unavailable = False

        self._base_url = None
        self._data = {}
        self._config_entry = config_entry
        self._remove_async_track_time = None

    async def initialize(self):
        self._auth = requests.auth.HTTPDigestAuth(self._username, self._password)

        self._base_url = f"http://{self._host}:{self._port}"

        self.update_system_information()

        setup = self._hass.config_entries.async_forward_entry_setup

        self._hass.async_create_task(setup(self._config_entry, DOMAIN_BINARY_SENSOR))

        async_call_later(self._hass, 5, self.async_finalize)

    async def async_finalize(self, event_time):
        _LOGGER.debug(f"async_finalize called at {event_time}")

        await self.async_update(event_time)

        self._hass.services.async_register(DOMAIN, 'open', self.vto_open_gate)

        self._remove_async_track_time = async_track_time_interval(self._hass, self.async_update, SCAN_INTERVAL)

    async def async_remove(self):
        _LOGGER.debug(f"async_remove called")

        self._hass.services.async_remove(DOMAIN, 'open')

        if self._remove_async_track_time is not None:
            self._remove_async_track_time()

    async def async_update(self, event_time):
        _LOGGER.debug(f"async_update called at {event_time}")

        if self._updating:
            return

        self._updating = True
        self.update_video_talk_log()

        async_dispatcher_send(self._hass, SIGNAL_UPDATE_VTO)

        self._updating = False

    def vto_http_request(self, command):
        connected = False
        result = None

        try:

            url = f"{self._base_url}{command}"

            response = requests.get(url, timeout=5, auth=self._auth)

            if response.status_code > 400:
                response.raise_for_status()
            if response.status_code == 400:
                _LOGGER.info(f"VTO Request to {command} failed due to Bad Request")

            result = response.text
            connected = True

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'VTO Request to {command} failed, Error: {str(ex)}, Line: {line_number}')

        self._connected = connected

        return result

    def update_system_information(self):
        try:
            content = self.vto_http_request(SYSTEM_INFO_URL)
            attributes = {}

            if content is not None:
                lines = content.split('\n')

                for item in lines:
                    data_item_arr = item.split('=')
                    if len(data_item_arr) > 1:
                        data_key = data_item_arr[0]
                        data_value = data_item_arr[1]

                        attributes[data_key] = data_value

            self._attributes = attributes

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to update VTO system information, Error: {ex}, Line: {line_number}')

    def update_video_talk_log(self):
        try:
            content = self.vto_http_request(VIDEO_TALK_LOG_URL)
            last_ring = None
            last_ring_data = None

            if content is not None:
                self.parse(content)

                current_time = datetime.now()

                for key in self._data:
                    item = self._data[key]

                    create_time = int(item.get("CreateTime", 0))

                    create_date_time = datetime.utcfromtimestamp(create_time)
                    item["CreatedDate"] = create_date_time

                    delta_seconds = (current_time - create_date_time).total_seconds()

                    self._is_ringing = delta_seconds < RING_TIME

                    if last_ring is None or create_date_time > last_ring:
                        last_ring = create_date_time
                        last_ring_data = item

                    log_message = f'Current time: {current_time}, Last ring: {create_date_time},' \
                                  f' Delta:{delta_seconds}'

                    if self._is_ringing:
                        self._hass.bus.fire(f"{DOMAIN}_ring", item)

                        _LOGGER.info(f'update - Ringing, {log_message}')
                    else:
                        _LOGGER.debug(f'update - {log_message}')

                self._attributes[ATTR_LAST_RING] = last_ring
                self._attributes[ATTR_LAST_UPDATE] = current_time

                for key in last_ring_data:
                    self._attributes[key] = last_ring_data[key]

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to update VTO talk log, Error: {ex}, Line: {line_number}')

    def vto_open_gate(self, service_data):
        try:
            self.vto_http_request(OPEN_GATE_URL)
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to open gate, Error: {ex}, Line: {line_number}')

    def parse(self, content):
        lines = content.split('\n')
        for item in lines:
            call_data = item.split('.')

            if len(call_data) > 1:
                call_key = call_data[0]
                call_item = call_data[1]

                cleaned_call_key = call_key.replace("records[", "").replace("]", "")
                call_data_item = call_item.split('=')
                call_data_property = call_data_item[0]
                call_data_value = call_data_item[1]

                data_item = self._data.get(cleaned_call_key, {})
                data_item[call_data_property] = call_data_value

                self._data[cleaned_call_key] = data_item

        for key in self._data:
            item = self._data[key]

            create_time = int(item.get("CreateTime", 0))

            item["CreateDateTime"] = datetime.fromtimestamp(create_time)

    def get_attributes(self, device_class):
        attributes = {}
        for key in self._attributes:
            attributes[key] = self._attributes[key]

        attributes["device_class"] = SENSOR_TYPES[device_class]

        return attributes

    def get_sensor_data(self, sensor_type):
        state = self._is_ringing if sensor_type == SENSOR_TYPE_RING else self._connected
        icon = ICONS[sensor_type][state]

        entity = {
            ENTITY_NAME: f"{self._name} {sensor_type}",
            ENTITY_STATE: state,
            ENTITY_ATTRIBUTES: self.get_attributes(sensor_type),
            ENTITY_MODEL: self._attributes.get("deviceType", DEFAULT_NAME),
            ENTITY_ICON: icon
        }

        return entity
