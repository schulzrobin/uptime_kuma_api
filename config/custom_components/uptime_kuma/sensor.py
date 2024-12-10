import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME

from .const import DOMAIN, CONF_API_URL, CONF_API_TOKEN

def fetch_monitors(api_url, api_token):
    """Fetch monitor data from the Uptime Kuma API."""
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(f"{api_url}", headers=headers)
    response.raise_for_status()
    return response.json()

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Uptime Kuma sensors based on a config entry."""
    api_url = config_entry.data[CONF_API_URL]
    api_token = config_entry.data[CONF_API_TOKEN]

    # Fetch monitor data
    monitors = fetch_monitors(api_url, api_token)

    # Create a sensor for each monitor
    entities = []
    for monitor in monitors:
        entities.append(UptimeKumaSensor(monitor))
    async_add_entities(entities, update_before_add=True)

class UptimeKumaSensor(SensorEntity):
    """Representation of an Uptime Kuma monitor as a sensor."""

    def __init__(self, monitor):
        """Initialize the sensor."""
        self._id = monitor["id"]
        self._name = monitor["name"]
        self._state = monitor["status"]
        self._attributes = {
            "url": monitor["url"],
            "type": monitor["type"],
            "interval": monitor["interval"],
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Uptime Kuma: {self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return self._attributes