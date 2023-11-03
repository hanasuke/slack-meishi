import io
import requests

from PIL import Image
from dataclasses import dataclass


@dataclass
class Person:
    icon: Image
    username: str
    realname: str

    def __init__(self, icon_url: str, username: str, realname: str):
        self.username = username
        self.realname = realname

        self.icon = Image.open(io.BytesIO(requests.get(icon_url).content))
