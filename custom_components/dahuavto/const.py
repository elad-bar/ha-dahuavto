from datetime import timedelta

VERSION = '1.0.3'

DOMAIN = 'dahuavto'
DATA_VTO = 'data_{0}'.format(DOMAIN)
SIGNAL_UPDATE_VTO = '{0}_update'.format(DOMAIN)
DEFAULT_NAME = 'Dahua VTO'
BASE_URL = 'http://{0}:{1}/{2}'
DEFAULT_DEVICE_CLASS_DEFAULT = 'NONE'
DEFAULT_DEVICE_CLASS_CONNECTIVITY = 'Connectivity'
DEFAULT_PORT = 80

SENSOR_TYPE_RING = 'Ring'
SENSOR_TYPE_AVAILABLE = 'Available'

SENSOR_TYPES = {
    SENSOR_TYPE_RING: DEFAULT_DEVICE_CLASS_DEFAULT,
    SENSOR_TYPE_AVAILABLE: DEFAULT_DEVICE_CLASS_CONNECTIVITY
}

NOTIFICATION_ID = '{0}_notification'.format(DOMAIN)
NOTIFICATION_TITLE = '{0} Setup'.format(DEFAULT_NAME)

RING_TIME = 10

ATTR_LAST_RING = 'Last Ring'
ATTR_LAST_UPDATE = 'Last Update'

OPEN_GATE_URL = '/cgi-bin/accessControl.cgi?action=openDoor&channel=1&UserID=101&Type=Remote'
VIDEO_TALK_LOG_URL = '/cgi-bin/recordFinder.cgi?action=find&name=VideoTalkLog'
SYSTEM_INFO_URL = '/cgi-bin/magicBox.cgi?action=getSystemInfo'

BINARY_SENSOR_ENTITY_ID = 'binary_sensor.{}_{}'

SCAN_INTERVAL = timedelta(seconds=5)
