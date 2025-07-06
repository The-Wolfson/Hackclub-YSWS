from .ysws.list import ysws_list
from .ysws.details import ysws_details
from .event.list import event_list
from .event.details import event_details


# This Appwrite function will be executed every time your function is triggered
def main(context):
    path: str = context.req.path
    split_path = path.split("/")[1:]

    context.log(split_path)
    context.log(len(split_path))

    if not context.req.method == "GET":
        return context.res.text(f"Invalid method. Only GET is supported.", 405)

    if not split_path[0] == "v1":
        return context.res.text(f"{path} is not a valid path. Requires a version.", 400)

    if split_path[1] == "ysws":
        if len(split_path) == 2:
            return ysws_list(context)
        elif len(split_path) == 3:
            return ysws_details(context)

    elif split_path[1] == "events":
        if len(split_path) == 2:
            return event_list(context)
        elif len(split_path) == 3:
            return event_details(context)

    context.error(f"Unsupported endpoint: {path}")
    return context.res.text(f"{path} is an unsupported endpoint", 400)

# https://dash.events.hackclub.com/api/v1/events
# https://raw.githubusercontent.com/hackclub/YSWS-Catalog/refs/heads/main/api.json