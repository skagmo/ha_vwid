from .libvwid import vwid
import asyncio
import logging
import aiohttp
import voluptuous as vol
from datetime import timedelta
from typing import Any, Callable, Dict, Optional
from homeassistant import config_entries, core
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    ENTITY_ID_FORMAT,
    SensorDeviceClass
)
from homeassistant.const import (
    ATTR_NAME,
    CONF_NAME,
    CONF_PASSWORD
)
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType
)
from .const import (
    DOMAIN,
    CONF_VIN
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=10)

async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    session = async_get_clientsession(hass)
    api = vwid(session)
    api.set_credentials(config[CONF_NAME], config[CONF_PASSWORD])
    api.set_vin(config[CONF_VIN])
    api.set_jobs(['charging','climatisation'])
    sensor = VwidSensor(api)
    async_add_entities([sensor], update_before_add=True)

class VwidSensor(Entity):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self._name = 'State of charge'
        self._state = None
        self._available = True
        self.attrs = {'vin': self.api.vin}
        #self.attrs: Dict[str, Any] = {ATTR_PATH: self.repo}
        self.entity_id = ENTITY_ID_FORMAT.format(self.api.vin + '_soc')
        
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return (self.api.vin + '_soc')

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self):
        return self._state
        
    @property
    def device_class(self):
        return SensorDeviceClass.BATTERY
        
    @property
    def unit_of_measurement(self):
        return '%'

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    async def async_update(self):
        data = await self.api.get_status()
        
        if not data:
            self._available = False
            _LOGGER.exception("Error retrieving data")
            return
            
        try:
            # Add state of charge as value
            self._state = int(data['charging']['batteryStatus']['value']['currentSOC_pct'])
        except KeyError:
            self._available = False
            _LOGGER.exception(f"Missing keys in data: {data}")
            return
            
        self._available = True
        
        # For now, just flatten tree structure and add parameters as attributes
        # Data structure is 4 levels deep
        # Todo: Recursive function to flatten structure
        for key1 in data.keys():
            for key2 in data[key1].keys():
                for key3 in data[key1][key2].keys():
                    for key4 in data[key1][key2][key3].keys():
                        value = data[key1][key2][key3][key4]
                        # Skip timestamps, dictionaries and lists
                        if (type(value) in [dict, list]) or ("Timestamp" in key4):
                            continue
                        # Convert mix of camelcase and snakecase to just camelcase
                        key_camelcase = ''.join((x[:1].upper() + x[1:]) for x in key4.split('_'))
                        self.attrs[key_camelcase] = value

