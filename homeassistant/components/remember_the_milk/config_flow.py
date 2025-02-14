from typing import Any

from rtmapi import Rtm, RtmRequestFailedException

from homeassistant.components.remember_the_milk import DOMAIN, RTM_SCHEMA
from homeassistant.components.remember_the_milk.const import CONF_SHARED_SECRET
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY, CONF_NAME, CONF_TOKEN, CONF_URL


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
            api_key=api_key,
            shared_secret=shared_secret,
            perms="delete",
            token=self.data.get(CONF_TOKEN, None),
        )

        try:
            url, frob = await self.hass.async_add_executor_job(
                self._rtm_api.authenticate_desktop
            )
            # TODO: I think we don't need frob, don't put it in data
            self.data["frob"] = frob
            self.data[CONF_URL] = url
            self.data[CONF_TOKEN] = self._rtm_api.token

        except RtmRequestFailedException:
            # TODO: doing this clears the data that the user entered. That's not nice but I don't know how to pass the data back
            return self.async_show_form(
                step_id="user",
                data_schema=RTM_SCHEMA,
                errors={
                    CONF_API_KEY: "Call to RememberTheMilk failed. Please check that api_key and shared_secret are correct."
                },
            )

        return self.async_create_entry(title=self.data["name"], data=self.data)
