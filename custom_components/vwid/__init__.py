from .const import DOMAIN
from homeassistant.helpers.discovery import async_load_platform
from homeassistant import config_entries, core

async def async_setup(hass, config):
# 	hass.async_add_job(async_load_platform(hass, 'sensor', DOMAIN, {}, config))
	return True
	
	
async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the setup to the sensor platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

