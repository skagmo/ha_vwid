from homeassistant import config_entries, core
from .const import (DOMAIN, CONF_VIN)
from homeassistant.const import (CONF_NAME, CONF_PASSWORD)
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from typing import Any, Dict, Optional

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_VIN): cv.string,
    }
)

class VwidConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            self.data = user_input
            return self.async_create_entry(title="Volkswagen ID custom", data=self.data)

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )
