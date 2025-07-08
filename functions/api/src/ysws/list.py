from datetime import datetime
from enum import Enum
from ..model.ysws.response import Response
from ..model.ysws.program import Program, Status
import urllib.parse
import re

def ysws_list(context):
    body: str = context.req.body
    query = context.req.query

    # Decode the body to extract the 'text' parameter
    parsed = urllib.parse.parse_qs(body)
    text = parsed.get("text", [""])[0]  # default to "" if 'text' not found

    # Extract --filter: and --sort: values from text
    filter_match = re.search(r'--filter:([^\s]+)', text)
    sort_match = re.search(r'--sort:([^\s]+)', text)

    # Determine Sort and Filter values
    sort: Sort = (
        Sort(sort_match.group(1))
        if sort_match and sort_match.group(1) in Sort.__members__.values()
        else Sort(query.get("sort"))
        if query.get("sort") and query.get("sort") in Sort.__members__.values()
        else Sort.Date
    )

    filter: Filter = (
        Filter(filter_match.group(1))
        if filter_match and filter_match.group(1) in Filter.__members__.values()
        else Filter(query.get("filter"))
        if query.get("filter") and query.get("filter") in Filter.__members__.values()
        else Filter.Active
    )
    context.log(f"YSWS List — Sort: {sort}, Filter: {filter}")

    response: Response = Response("https://raw.githubusercontent.com/hackclub/YSWS-Catalog/refs/heads/main/api.json")

    programs: list[Program] = sort_programs(filter_programs(response.programs, filter), sort)

    return context.res.json(
        {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "YSWS Programs"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Filter"
                            },
                            "initial_option": {
                                "text": {
                                    "type": "plain_text",
                                    "text": filter.name
                                },
                                "value": filter.value
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": f.name
                                    },
                                    "value": f.value
                                } for f in Filter
                            ]
                        },
                        {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Sort"
                            },
                            "initial_option": {
                                "text": {
                                    "type": "plain_text",
                                    "text": sort.name
                                },
                                "value": sort.value
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": s.name
                                    },
                                    "value": s.value
                                } for s in Sort
                            ]
                        }
                    ]
                },
                *[block for program in programs[:10] for block in program.to_blocks()]
            ]
        }
    )


class Filter(Enum):
    All = "all"
    Active = "active"  # default
    Ended = "ended"
    Draft = "draft"


class Sort(Enum):
    Category = "category"
    Alphabetical = "alphabetical"
    Date = "date"  # default
    Status = "status"


def sort_programs(programs: list[Program], sort: Sort) -> list[Program]:
    match sort:
        case Sort.Category:
            return sorted(programs, key=lambda program: program.category)
        case Sort.Alphabetical:
            return sorted(programs, key=lambda program: program.name)
        case Sort.Status:
            return sorted(programs, key=lambda program: program.status.value)
        case _:  # Date
            return sorted(programs, key=lambda program: program.deadline if program.deadline else datetime.now(), reverse=True)


def filter_programs(programs: list[Program], filter: Filter) -> list[Program]:
    match filter:
        case Filter.All:
            return programs
        case Filter.Ended:
            return [program for program in programs if program.status == Status.Ended]
        case Filter.Draft:
            return [program for program in programs if program.status == Status.Draft]
        case _: # Active
            return [program for program in programs if program.status == Status.Active]
