from dataclasses import dataclass
from .event import Event

import requests


@dataclass
class Response:
    events: list[Event]

    def __init__(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        self.events = [Event(e) for e in data]
