from ..model.event.event import Event
from ..model.event.response import Response

def event_details(context):
    path: str = context.req.path
    id = path.split("/")[-1]

    context.log(f"Event Details — ID: {id}")

    response: Response = Response("https://dash.hackathons.hackclub.com/api/v1/hackathons")

    event: Event | None = next((event for event in response.events if event.id == id), None)

    if not event:
        return context.res.text(f"No event with id {id}", 404)

    blocks = event.to_blocks()
    blocks.append(
        {
            "type": "image",
            "image_url": event.banner_url,
            "alt_text": f"{event.name} banner"
        }
    )
    return context.res.json(
        {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": event.name
            },
            "close": {
                "type": "plain_text",
                "text": "Done"
            },
            "blocks": blocks
        }
    )
