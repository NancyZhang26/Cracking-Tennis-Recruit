from enum import Enum

class Browsers(str, Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"

class Proxy(Enum):
