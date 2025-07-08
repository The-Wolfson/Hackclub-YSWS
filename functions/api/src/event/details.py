from ..model.event.event import Event
from ..model.event.response import Response


def event_details(context):
    path: str = context.req.path
    slug = path.split("/")[-1]

    context.log(f"Event Details — Slug: {slug}")

    response: Response = Response("https://events.hackclub.com/api/events/all/")

    event: Event | None = next((event for event in response.events if event.slug == slug), None)

    if not event:
        return context.res.text(f"No hackathon with slug {slug}", 404)

    return context.res.json(
        {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": event.title
            },
            "close": {
                "type": "plain_text",
                "text": "Done"
            },
            "blocks": event.to_blocks()
        }
    )
