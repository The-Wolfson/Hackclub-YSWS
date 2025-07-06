from datetime import datetime
from enum import Enum
from ..model.ysws.response import Response
from ..model.ysws.program import Program, Status


def ysws_list(context):
    query = context.req.query
    sort: Sort = Sort(query.get("sort")) if query.get("sort") else Sort.Date
    filter: Filter = Filter(query.get("filter")) if query.get("filter") else Filter.Active
    context.log(f"ysws List — Sort: {sort}, Filter: {filter}")

    response: Response = Response("https://raw.githubusercontent.com/hackclub/YSWS-Catalog/refs/heads/main/api.json")

    programs: list[Program] = sort_programs(filter_programs(response.programs, filter), sort)

    return context.res.json(
        {
            "blocks": [block for program in programs[:10] for block in program.to_blocks()]
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
