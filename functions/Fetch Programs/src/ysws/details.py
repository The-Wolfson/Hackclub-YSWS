from ..model.ysws.response import Response
from ..model.ysws.program import Program


def ysws_details(context):
    path: str = context.req.path
    slack_channel = path.split("/")[-1]

    context.log(f"Event Details — Slack_Channel: {slack_channel}")

    response: Response = Response("https://raw.githubusercontent.com/hackclub/YSWS-Catalog/refs/heads/main/api.json")

    program: Program | None = next(
        (program for program in response.programs if program.slack_channel.strip("#") == slack_channel), None)

    if not program:
        return context.res.text(f"No program for Slack Channel: {slack_channel}", 404)

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*" + program.description + "*"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": program.status.name
                },
                **(
                    {"style": "primary"} if program.status.value == "active"
                    else {"style": "danger"} if program.status.value == "ended"
                    else {}
                )
            }
        }
    ]

    if program.detailed_description:
        blocks.append({
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": program.detailed_description
            }
        })

    if program.details:
        blocks.append({
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": program.details
            }
        })

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Ends on " + program.deadline.strftime("%B %d")
        }
    })

    action_elements = []
    if program.website:
        action_elements.append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Website"
            },
            "url": program.website
        })
    if program.slack:
        action_elements.append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Slack Channel"
            },
            "url": program.slack
        })

    if action_elements:
        blocks.append({
            "type": "actions",
            "elements": action_elements
        })

    return context.res.json(
        {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": program.name
            },
            "close": {
                "type": "plain_text",
                "text": "Done"
            },
            "blocks": blocks
        }
    )