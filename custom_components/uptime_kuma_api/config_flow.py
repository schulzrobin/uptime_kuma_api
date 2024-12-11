import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_API_URL, CONF_API_TOKEN

class UptimeKumaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Uptime Kuma."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Test API connection
            api_url = user_input[CONF_API_URL]
            api_token = user_input[CONF_API_TOKEN]

            if await self._test_api(api_url, api_token):
                return self.async_create_entry(title="Uptime Kuma", data=user_input)
            else:
                errors["base"] = "cannot_connect"

        # Define the form schema
        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_URL): str,
                vol.Required(CONF_API_TOKEN): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def _test_api(self, api_url: str, api_token: str) -> bool:
        """Test the connection to the Uptime Kuma API."""
        try:
            # Simulate an API call to verify credentials
            headers = {"Authorization": f"Bearer {api_token}"}
            async with self.hass.helpers.aiohttp_client.async_get_clientsession().get(
                api_url, headers=headers
            ) as response:
                if response.status == 200:
                    return True
        except Exception:  # noqa
            pass
        return False