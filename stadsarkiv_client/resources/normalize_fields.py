from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.resources.resource_definitions import resource_definitions
import re
from urllib.parse import unquote


log = get_log()


def _should_linkify(value: str):
    """Check if string should be linkified. '1;collection'
    Split into id and label. If ';' in string, return True
    """
    value = value.strip()
    if value.find(";") != -1:
        return True

    return False


def _get_link_list(name: str, values: list):
    links = []
    for elem in values:
        id_label = elem.split(";")
        links.append({"search_query": f"{name}={id_label[0]}", "label": f"{id_label[1]}"})

    return links


def _linkify_str(text):
    pattern = r"(https?://\S+)"

    def replace_with_link(match):
        url = match.group(1)
        decoded_url = unquote(url)
        return f'<a href="{url}">{decoded_url}</a>'

    return re.sub(pattern, replace_with_link, text)


def get_string_or_link_list(name: str, values: list):
    """Get string list and convert to link list if needed if string contains ';'"""
    should_linkify = _should_linkify(values[0])
    if should_linkify:
        links = _get_link_list(name, values)

        return {
            "type": "link_list",
            "value": links,
            "name": name,
        }

    else:
        return {
            "type": "string_list",
            "value": values,
            "name": name,
        }


def get_sources_normalized(data: list):
    # iterate data and linkify
    data_normalized = []
    for i in range(len(data)):
        data_normalized.append(_linkify_str(data[i]))

    return data_normalized


def set_sources_normalized(data: dict):
    """Set sources field on dict"""
    if "sources" in data:
        data["sources_normalized"] = get_sources_normalized(data["sources"])

    return data


def set_outer_years(data: dict):
    """Set outer_years field on dict"""
    if "date_from" and "date_to" in data:
        outer_years = data["date_from"] + "-" + data["date_to"]
        data["outer_years"] = outer_years
    elif "date_from" in data:
        data["outer_years"] = data["date_from"]
    return data


def set_latitude_longitude(data: dict):
    """Set latitude and longitude fields on dict"""
    if "latitude" and "longitude" in data:
        data["latitude_longitude"] = {
            "type": "string",
            "value": str(data["latitude"]) + ", " + str(data["longitude"]),
            "name": "latitude_longitude_normalized",
        }

    return data


def set_creators_link_list(data: dict):
    """Set creator_link field on dict."""

    if "is_creator" in data and data["is_creator"]:
        value = [
            {
                "search_query": f"creators={data['id_real']}",
                "label": translate("See all records this creator has created"),
            }
        ]
        data["creators_link"] = value

    return data


def set_collectors_link_list(data: dict):
    """Set creator_link field on dict."""

    if "is_creator" in data and data["is_creative_creator"]:
        value = [
            {
                "search_query": f"collectors={data['id_real']}",
                "label": translate("See all records this organization has collected"),
            }
        ]
        data["collectors_link"] = value

    return data


def get_resource_and_types(resource):
    record_altered = {}
    for key, value in resource.items():
        resource_item = {}
        resource_item["value"] = value
        resource_item["name"] = key

        try:
            definition = resource_definitions[key]
            resource_item["type"] = definition["type"]
            record_altered[key] = resource_item
        except KeyError:
            # Don't alter if not defined
            record_altered[key] = value

    return record_altered
