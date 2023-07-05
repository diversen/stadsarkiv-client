from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import json
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.normalize_facets import NormalizeFacets
from stadsarkiv_client.records.meta_data import get_meta_data
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.facets import FACETS
from stadsarkiv_client.core import query


log = get_log()


async def get_records_search(request: Request):
    q = await query.get_search(request)
    query_params = await query.get_list(request, remove_keys=["q"])
    query_str = await query.get_str(request, remove_keys=["start", "size"])

    records = await api.proxies_records(request)
    alter_facets_content = NormalizeFacets(records, query_params=query_params, query_str=query_str)
    facets = alter_facets_content.get_altered_facets()
    facets_filters = alter_facets_content.get_checked_facets()

    context_values = {
        "title": translate("Search"),
        "records": records,
        "query_params": query_params,
        "query_str": query_str,
        "q": q,
        "record_facets": records["facets"],
        "facets": facets,
        "facets_filters": facets_filters,
    }

    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse("records/search.html", context)


async def get_record_view(request: Request):
    record_id = request.path_params["record_id"]
    record_sections = settings["record_sections"]

    record = await api.proxies_record_get_by_id(record_id)

    metadata = get_meta_data(request, record)
    record = {**record, **metadata}

    record_altered = record_alter.record_alter(request, record)
    record_and_types = record_alter.get_record_and_types(record_altered)
    sections = record_alter.get_section_data(record_sections, record_and_types)

    context_variables = {
        "title": record_altered["title"],
        "record_altered": record_altered,
        "sections": sections,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("records/record.html", context)


async def get_facets_test(request: Request):
    context = await get_context(request, {"facets": FACETS})
    return templates.TemplateResponse("records/facets.html", context)


async def get_record_view_json(request: Request):
    try:
        record_id = request.path_params["record_id"]
        type = request.path_params["type"]
        record_sections = settings["record_sections"]

        record = await api.proxies_record_get_by_id(record_id)

        metadata = get_meta_data(request, record)
        record_altered = {**record, **metadata}

        record_altered = record_alter.record_alter(request, record_altered)
        record_and_types = record_alter.get_record_and_types(record_altered)
        sections = record_alter.get_section_data(record_sections, record_and_types)

        if type == "record":
            record_json = json.dumps(record, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_json)

        elif type == "record_altered":
            record_altered_json = json.dumps(record_altered, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_altered_json)

        elif type == "record_and_types":
            record_and_types_json = json.dumps(record_and_types, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_and_types_json)

        elif type == "record_sections":
            record_sections_json = json.dumps(sections, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_sections_json)
        else:
            raise HTTPException(404, detail="type not found", headers=None)

    except Exception as e:
        log.exception(e)
        raise HTTPException(500, detail=str(e), headers=None)
