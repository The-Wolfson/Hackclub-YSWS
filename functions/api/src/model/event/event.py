from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    id: str
    slug: str
    title: str
    desc: str
    leader: str
    cal: str
    start: datetime
    end: datetime
    youtube: str | None
    ama: bool
    ama_id: str
    ama_avatar: str
    avatar: str

    def __init__(self, data: dict):
        self.id = data.get("id")
        self.slug = data.get("slug")
        self.title = data.get("title")
        self.desc = data.get("desc")
        self.leader = data.get("leader")
        self.cal = data.get("cal")
        self.start = datetime.fromisoformat(data["start"])
        self.end = datetime.fromisoformat(data["end"])
        self.youtube = data.get("youtube")
        self.ama = data.get("ama")
        self.ama_id = data.get("amaId")
        self.ama_avatar = data.get("amaAvatar")
        self.avatar = data.get("avatar")

    def to_blocks(self):
        elements = [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Add to Calendar"
                },
                "url": self.cal
            }
        ]
        if self.youtube:
            elements.append({
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Watch"
                                },
                                "url": self.youtube
            })
        return [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{self.title}*\n{self.desc}\n*{self.start.strftime("%H:%M")} - {self.end.strftime("%H:%M, %d %B")}*"
                },
                "accessory": {
                    "type": "image",
                    "image_url": self.avatar,
                    "alt_text": "Avatar"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"{"AMA p" if self.ama else "P"}resented by {self.leader}"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": elements
            }
        ]
