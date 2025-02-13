import voluptuous as vol

from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.helpers import config_validation as cv

CONF_SHARED_SECRET = "shared_secret"
CONF_ID_MAP = "id_map"
CONF_LIST_ID = "list_id"
CONF_TIMESERIES_ID = "timeseries_id"
CONF_TASK_ID = "task_id"
RTM_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_SHARED_SECRET): cv.string,
    }
)

RTM_TOKEN_SCHEMA = vol.Schema(
    {
        vol.Required("dummy_field"): cv.string,
    }
)
DOMAIN = "remember_the_milk"
CONFIG_FILE_NAME = ".remember_the_milk.conf"
SERVICE_CREATE_TASK = "create_task"
SERVICE_COMPLETE_TASK = "complete_task"
DEFAULT_NAME = DOMAIN
