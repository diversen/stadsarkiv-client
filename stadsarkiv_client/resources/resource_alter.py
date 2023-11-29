"""
File contains functions for altering resources,
e.g. set sources_normalized, set outer years, etc.
"""

from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()


def resource_alter(resource: dict):
    schema = resource["schema"]

    relations = resource.get("relations")

    resource = normalize_fields.set_created_decommissioned(resource)
    resource = normalize_fields.set_collectors_link_list(resource, schema)
    resource = normalize_fields.set_creators_link_list(resource, schema)
    resource = normalize_fields.set_sources_normalized(resource)
    resource = normalize_fields.set_outer_years(resource)
    resource = normalize_fields.set_latitude_longitude(resource)
    resource = normalize_fields.get_resource_and_types(resource)

    # These are either string_list or link_list.
    string_list_or_link_list = [
        "collectors",
        "curators",
    ]

    for elem in string_list_or_link_list:
        if elem in resource:
            resource[elem] = normalize_fields.get_string_or_link_list(elem, resource[elem])

    resource["relations"] = relations
    return resource
