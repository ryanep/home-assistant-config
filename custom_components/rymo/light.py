"""Rymo Light Home Assistant Integration"""
import logging
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import homeassistant.util.color as color_util

from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.components.light import (
    LightEntity,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    ATTR_RGB_COLOR,
    COLOR_MODE_RGB
)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP_ADDRESS): cv.string
})

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Rymo Light platform."""

    ipAddress = config[CONF_IP_ADDRESS]

    add_entities([RymoLedBulb(ipAddress)])


class RymoLedBulb(LightEntity):
    """Representation of a Rymo LED bulb"""

    def __init__(self, ipAddress):
        self._ip_address = ipAddress
        self._is_on = False
        self._brightness = 255
        self._rgb_color = [255, 0, 0]
        self._color_mode = COLOR_MODE_RGB
        self._supported_color_modes = set([COLOR_MODE_RGB])

        self.update()

    @property
    def name(self):
        """Name of the device."""
        return self._name

    @property
    def unique_id(self):
        """Unique id."""
        return self._unique_id

    @property
    def is_on(self):
        """Status of the device."""
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def rgb_color(self):
        return self._rgb_color

    @property
    def color_mode(self):
        return self._color_mode

    @property
    def supported_color_modes(self):
        return self._supported_color_modes

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR

    def turn_on(self, **kwargs) -> None:
        """Turn LED On"""

        _LOGGER.info(kwargs)

        if ATTR_RGB_COLOR in kwargs:
            rgb = kwargs[ATTR_RGB_COLOR]
            self._rgb_color = rgb

            URL = f"http://{self._ip_address}/on?red={rgb[0]}&green={rgb[1]}&blue={rgb[2]}"
            r = requests.get(URL)
        else:
            URL = f"http://{self._ip_address}/on?red=255&green=0&blue=0"
            r = requests.get(URL)
            self._rgb_color = [255, 0, 0]

        self._is_on = True
        self._brightness = 255

    def turn_off(self, **kwargs):
        """Turn LED Off"""
        URL = f"http://{self._ip_address}/off"

        r = requests.get(URL)

        self._is_on = False
        self._rgb_color = [0, 0, 0]

    def update(self):
        URL = f"http://{self._ip_address}/status"

        r = requests.get(URL)
        data = r.json()

        self._name = "rymo"
        self._unique_id = "1234"
        self._is_on = data["status"]
        self._brightness = 255
        self._rgb_color = data["color"]
