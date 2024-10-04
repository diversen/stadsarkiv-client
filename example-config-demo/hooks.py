from starlette.routing import Route
from starlette.requests import Request
from starlette.exceptions import HTTPException
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.records import record_utils
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.core.database import bookmarks
from stadsarkiv_client.core.database import cache
from stadsarkiv_client.core import api
from stadsarkiv_client.core.context import get_context
import json
import os
import csv
from stadsarkiv_client.core.api_error import OpenAwsException


log = get_log()

current_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.abspath(__file__))


def _get_bookmarks_by_email(email):
    """ "
    Get bookmarks by email from csv file
    """

    bookmarks_file = os.path.join(base_dir, "..", "data", "bookmarks_with_emails.csv")
    resource_ids = []
    with open(bookmarks_file, "r") as bookmarks_file:
        reader = csv.DictReader(bookmarks_file)
        for row in reader:
            if row["email"] == email:
                resource_ids.append(row["resource_id"])
    return resource_ids


def _user_mail_exists(email):
    """
    Check if email exists in user file
    """
    users_emails_file = os.path.join(base_dir, "..", "data", "users_emails.csv")
    with open(users_emails_file, "r") as users_emails_file:
        reader = csv.DictReader(users_emails_file)
        for row in reader:
            if row["email"] == email:
                return True
    return False


async def docs_endpoint(request: Request):

    docs_folder = str(os.path.join(base_dir, "..", "docs"))

    docs_data = [
        {"title": "stadsarkiv-client", "file": "README.md", "path": "/"},
        {"title": "Create client", "file": "README.client.md", "path": "/docs/README.client.md"},
        {"title": "Run on server", "file": "README.server.md", "path": "/docs/README.server.md"},
    ]

    url_path = request.url.path

    for doc in docs_data:
        if doc["path"] != url_path:
            continue
        # open file and read it.
        file_path = os.path.join(docs_folder, doc.get("file", ""))
        with open(file_path, "r") as file:
            content = file.read()

        context_values = {"title": "Documentation", "doc_data": docs_data, "content": content}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse(request, "docs/docs.html", context)

    raise HTTPException(404, detail="type not found", headers=None)


class Hooks(HooksSpec):
    def __init__(self, request):
        super().__init__(request)

    def after_routes_init(self, routes: list) -> list:
        log.info("Hooks. After routes init")

        routes_test = [
            Route("/", endpoint=docs_endpoint, name="homepage", methods=["GET"]),
            Route("/docs/{page:str}", endpoint=docs_endpoint, name="docs", methods=["GET"]),
        ]

        routes = routes_test + routes

        return routes

    async def after_login_success(self, response: dict) -> dict:
        """
        After a successful login.
        """
        me = await api.me_get(self.request)
        user_id = me["id"]
        email = me["email"]

        cache_key = f"bookmarks_imported_{user_id}"
        result = await cache.cache_get(cache_key)

        if not result:

            log.info(f"Importing bookmarks for user: {email}")
            bookmarks_from_file = _get_bookmarks_by_email(email)

            for bookmark_from_file in bookmarks_from_file:
                await bookmarks.bookmarks_insert(user_id, bookmark_from_file)

            await cache.cache_set(cache_key, True)

        return response

    async def after_login_failure(self, response: dict) -> dict:
        """
        After a login failure
        """
        request = self.request
        form = await request.form()
        username = str(form.get("email"))
        if _user_mail_exists(username):
            raise OpenAwsException(
                401,
                "Kære bruger. Du er tilknyttet det gamle system. Men da vi er overgået til et nyt system, skal du oprette en ny bruger. Hvis du bruger samme email vil systemet ved første login forsøge at importere data fra det gamle system.",
            )
        return response

    async def before_get_auto_complete(self, query_params: list) -> list:
        query_params.append(("limit", "10"))

        """
        Alter the query params before the autocomplete is executed.
        """
        return query_params

    async def before_context(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        context["meta_title"] = context["meta_title"] + " | AarhusArkivet"

        return context

    async def before_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        return query_params

    async def after_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        """
        return query_params

    async def after_get_record(self, record: dict, meta_data: dict) -> tuple:
        """
        Alter the record and meta_data dictionaries after the api call
        """
        # sejrs sedler
        if record_utils.is_collection(record, 1):
            meta_data["title"] = ""
            meta_data["record_type"] = "sejrs_sedler"
            meta_data["representation_text"] = record["summary"]
            del record["summary"]

        # teater arkivet
        if record_utils.is_curator(record, 4):
            if record.get("summary"):
                meta_data["title"] = f"[{record['summary']}]"

        return record, meta_data

    async def after_get_record_and_types(self, record: dict, record_and_types: dict) -> tuple:
        if record_utils.is_collection(record, 48):
            agenda_items = record.get("admin_data", {}).get("agendaItems")

            if agenda_items:
                agenda_items = json.loads(agenda_items)
                agenda_items = _convert_agenda_items_to_link_list(agenda_items)
                record_alter.set_record_and_type(record_and_types, "agenda_items", agenda_items, "link_list")

            original_id = record.get("original_id")
            if original_id:
                record_alter.set_record_and_type(record_and_types, "original_id", original_id, "string")

        return record, record_and_types

    async def after_get_resource(self, type: str, resource: dict) -> dict:
        """
        Alter the entity json is returned from the proxies api.
        """
        return resource


def _convert_agenda_items_to_link_list(agenda_items: list) -> list:
    """
    Convert agenda items to link dictionary
    agenda items is a list of dicts, e.g.:
    [{"href": "https://storage.googleapis.com/openaws-webonly/19010523_149.pdf", "start_page": 1}]
    This will be converted to a type, 'link_list' that can be used in the templates
    """
    agenda_items_parsed = []
    for item in agenda_items:
        agenda_item = {}

        href = item.get("href")

        # from e.g. https://storage.googleapis.com/openaws-webonly/19010523_149.pdf get '19010523'
        date = href.split("/")[-1].split("_")[0]

        # convert to date: 1901-05-23
        date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"

        agenda_item["label"] = date
        agenda_item["search_query"] = item.get("href") + "#page=" + str(item.get("start_page", 1))
        agenda_items_parsed.append(agenda_item)
    return agenda_items_parsed
