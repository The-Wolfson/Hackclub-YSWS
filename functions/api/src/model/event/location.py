from dataclasses import dataclass

@dataclass
class Location:
    city: str | None = None
    province: str | None = None
    country: str | None = None
    country_code: str | None = None
    longitude: str | None = None
    latitude: str | None = None

    def __init__(self, data: dict):
        self.city = data.get("city")
        self.province = data.get("province")
        self.country = data.get("country")
        self.country_code = data.get("country_code")
        self.longitude = data.get("longitude")
        self.latitude = data.get("latitude")