from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from .location import Location

class Modality(Enum):
    Hybrid = "hybrid"
    In_Person = "in_person"
    Online = "online"
    All = "all"


class TypeEnum(Enum):
    HACKATHON = "hackathon"

@dataclass
class Hackathon:
    id: str
    type: TypeEnum
    name: str
    starts_at: datetime
    ends_at: datetime
    modality: Modality
    website: str
    logo_url: str
    banner_url: str
    location: Location
    apac: bool
    created_at: datetime

    def __init__(self, data: dict):
        self.id = data.get("id")
        self.type = TypeEnum(data.get("type"))
        self.name = data.get("name")
        self.starts_at = datetime.fromisoformat(data["starts_at"]) if data.get("starts_at") else None
        self.ends_at = datetime.fromisoformat(data["ends_at"]) if data.get("ends_at") else None
        self.modality = Modality(data.get("modality"))
        self.website = data.get("website")
        self.logo_url = data.get("logo_url")
        self.banner_url = data.get("banner_url")
        self.location = Location(data.get("location"))
        self.apac = data.get("apac")
        self.created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None

    def to_blocks(self):
        return [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{self.website}|{self.name}>*\n{self.modality.value.capitalize()} Hackathon\n{self.starts_at.strftime('%d %b')} to {self.ends_at.strftime('%d %b')}\n" + (f"{self.location.city}, {self.location.country}" if self.location.city and self.location.country else "")
                },
                "accessory": {
                    "type": "image",
                    "image_url": self.logo_url,
                    "alt_text": f"{self.name} thumbnail"
                }
            }
        ]