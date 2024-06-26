"""
Alter the record
"""

from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.records import normalize_dates
from stadsarkiv_client.records.normalize_copyright_status import normalize_copyright_status
from stadsarkiv_client.records.normalize_contractual_status import normalize_contractual_status
from stadsarkiv_client.records.normalize_legal_restrictions import normalize_legal_restrictions
from stadsarkiv_client.records.normalize_availability import normalize_availability
from stadsarkiv_client.records.normalize_ordering import normalize_ordering
from stadsarkiv_client.records.normalize_record import RecordNormalizer
from stadsarkiv_client.records.record_definitions import get_record_definitions
from stadsarkiv_client.core.translate import translate
from starlette.requests import Request


_record_definitions = get_record_definitions()
log = get_log()


def record_alter(request: Request, record: dict, meta_data: dict):
    record = record.copy()

    record_normalizer = RecordNormalizer()
    record = record_normalizer.normalize_record_data(request, record, meta_data)

    record = normalize_dates.normalize_dates(record)
    record = normalize_copyright_status(record, meta_data)
    record = normalize_contractual_status(record, meta_data)
    record = normalize_legal_restrictions(record, meta_data)
    record = normalize_availability(record, meta_data)
    record = normalize_ordering(record, meta_data)

    return record


def get_record_and_types(record):
    """
    Get record with types
    """
    record_altered = {}
    for key, value in record.items():
        if not value:
            continue

        record_item = {}
        record_item["value"] = value
        record_item["name"] = key

        try:
            definition = _record_definitions[key]
            record_item["type"] = definition["type"]
            record_item["label"] = translate("label_" + key)
            record_altered[key] = record_item
        except KeyError:
            pass

    return record_altered


def set_record_and_type(record_and_types, key, value, type):
    """
    Set a new key value pair on record_and_type
    """
    record_and_types[key] = {}
    record_and_types[key]["name"] = key
    record_and_types[key]["value"] = value
    record_and_types[key]["type"] = type
    record_and_types[key]["label"] = translate("label_" + key)

    return record_and_types
