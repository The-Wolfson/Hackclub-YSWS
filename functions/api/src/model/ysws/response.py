from dataclasses import dataclass
from .program import Program
import requests

@dataclass
class Response:
    limited_time: list[Program]
    indefinite: list[Program]
    drafts: list[Program]

    @property
    def programs(self) -> list[Program]:
        return self.limited_time + self.indefinite + self.drafts

    def __init__(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        self.limited_time = [Program(p) for p in data.get("limitedTime", [])]
        self.indefinite = [Program(p) for p in data.get("indefinite", [])]
        self.drafts = [Program(p) for p in data.get("drafts", [])]

    def to_blocks(self) -> list[dict]:
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "ysws Programs"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*{len(self.limited_time) + len(self.indefinite) + len(self.drafts)}* programs found"
                    }
                ]
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Limited Time"
                }
            },
        ]

        for program in self.limited_time:
            blocks.extend(program.to_blocks())

        blocks.append(
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Indefinite"
                }
            }
        )

        for program in self.indefinite:
            blocks.extend(program.to_blocks())

        blocks.append(
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Drafts"
                }
            }
        )

        for program in self.limited_time:
            blocks.extend(program.to_blocks())

        return blocks