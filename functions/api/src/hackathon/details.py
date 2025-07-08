from ..model.hackathon.hackathon import Hackathon
from ..model.hackathon.response import Response


def hackathon_details(context):
    path: str = context.req.path
    id = path.split("/")[-1]

    context.log(f"Event Details — ID: {id}")

    response: Response = Response("https://dash.hackathons.hackclub.com/api/v1/hackathons")

    hackathon: Hackathon | None = next((hackathon for hackathon in response.hackathons if hackathon.id == id), None)

    if not hackathon:
        return context.res.text(f"No hackathon with id {id}", 404)

    blocks = hackathon.to_blocks()
    blocks.append(
        {
            "type": "image",
            "image_url": hackathon.banner_url,
            "alt_text": f"{hackathon.name} banner"
        }
    )
    return context.res.json(
        {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": hackathon.name
            },
            "close": {
                "type": "plain_text",
                "text": "Done"
            },
            "blocks": blocks
        }
    )
