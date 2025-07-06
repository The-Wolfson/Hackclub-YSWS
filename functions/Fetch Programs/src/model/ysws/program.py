from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Status(Enum):
    Active = "active"
    Draft = "draft"
    Ended = "ended"

@dataclass
class Program:
    name: str
    description: str
    slack_channel: str
    detailed_description: str | None = None
    website: str | None = None
    slack: str | None = None
    status: Status | None = None
    deadline: datetime | None = None
    participants: int | None = None
    requirements: list[str] | None = None
    steps: list[str] | None = None
    details: list[str] | None = None

    def __init__(self, data: dict):
        self.name = data["name"]
        self.description = data["description"]
        self.slack_channel = data["slackChannel"]
        self.detailed_description = data.get("detailedDescription")
        self.website = data.get("website")
        self.slack = data.get("slack")
        self.status = Status(data["status"]) if data.get("status") else None
        self.deadline = datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None
        self.participants = data.get("participants")
        self.requirements = data.get("requirements", [])
        self.steps = data.get("steps", [])
        self.details = data.get("details", [])

    def to_blocks(self) -> list[dict]:
        return [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{f'<{self.website}|{self.name}>' if self.website else self.name}*\n{self.description}"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": self.slack_channel if self.slack else "Website"
                    },
                    "url": self.slack if self.slack else self.website
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": self.status.name + (
                            self.deadline.strftime(" | Ends on %-d %b") if self.deadline else "")
                    }
                ]
            }
        ]
