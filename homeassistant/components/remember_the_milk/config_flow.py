from typing import Any

from rtmapi import Rtm

from homeassistant.components.remember_the_milk import DOMAIN, RTM_SCHEMA
from homeassistant.components.remember_the_milk.const import (
    CONF_SHARED_SECRET,
    RTM_TOKEN_SCHEMA,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY, CONF_NAME


class RememberTheMilkConfigFlow(ConfigFlow, domain=DOMAIN):
    def __init__(self) -> None:
        self.data = {}
        self._rtm_api = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=RTM_SCHEMA, errors={}
            )

        self.data["name"] = user_input[CONF_NAME]
        api_key = self.data["api_key"] = user_input[CONF_API_KEY]
        shared_secret = self.data["shared_secret"] = user_input[CONF_SHARED_SECRET]

        self._rtm_api = Rtm(
            api_key=api_key, shared_secret=shared_secret, perms="delete", token=None
        )
        url, frob = await self.hass.async_add_executor_job(
            self._rtm_api.authenticate_desktop
        )

        # TODO: catch RtmRequestFailedException: Request rtm.auth.getFrob failed. Status: 100, reason: Invalid API Key.
        #  -> show error in api_key field and reshow input form

        self.data["frob"] = frob
        self.data["url"] = url

        return self.async_show_form(
            step_id="token",
            last_step=True,
            data_schema=RTM_TOKEN_SCHEMA,
            # Showing an arbitrary field just so we can show the url in the error field is very silly but the best I could ind
            errors={
                "dummy_field": f"Please visit {url} and come back here to complete the configuration."
            },
        )

    async def async_step_token(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        def get_token():
            self._rtm_api.retrieve_token(self.data["frob"])

        await self.hass.async_add_executor_job(get_token)

        # TODO: if get_token failed, token will be None. should we go back to the user step or reshow the token step?

        token = self._rtm_api.token
        self.data["token"] = token

        # Is this ok?
        return self.async_create_entry(title=self.data["name"], data=self.data)
