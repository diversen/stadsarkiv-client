"""
Define routes for the application.
"""

from starlette.routing import Route, Mount
from .endpoints import auth, proxies_records, proxies_search, proxies_resources, testing, pages, schemas, entities
import os
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.multi_static import MultiStaticFiles
from stadsarkiv_client.core.args import get_config_dir
from stadsarkiv_client.core.logging import get_log
from typing import Any

log = get_log()


def _get_static_dirs() -> list:
    """
    If static/ dir exists in current dir, add it to static_dir_list
    This will be override the module static files
    """

    static_dir_list = []
    local_config_dir = get_config_dir() + "/static"
    if os.path.exists(local_config_dir):
        static_dir_list.append(local_config_dir)
        log.debug(f"Loaded local static files: {local_config_dir}")
    else:
        log.debug(f"Local static files NOT loaded: {local_config_dir}")

    # Module static files. Default static files
    static_dir = os.path.dirname(os.path.abspath(__file__)) + "/static"
    static_dir_list.append(static_dir)
    return static_dir_list


# Add basic routes
routes = [
    Mount("/static", MultiStaticFiles(directories=_get_static_dirs()), name="static"),
    Route("/auth/user-info", endpoint=auth.post_user_info, name="user_info", methods=["POST"]),
    Route("/auth/login", endpoint=auth.get_login, name="login"),
    Route(
        "/auth/post-login-jwt",
        endpoint=auth.post_login_jwt,
        name="post_login_jwt",
        methods=["POST"],
    ),
    Route("/auth/logout", endpoint=auth.get_logout, name="logout"),
    Route("/auth/post-logout", endpoint=auth.post_logout, name="post_logout", methods=["POST"]),
    Route("/auth/register", endpoint=auth.get_register, name="register"),
    Route("/auth/post-register", endpoint=auth.post_register, name="post_register", methods=["POST"]),
    Route("/auth/verify/{token:str}", endpoint=auth.get_verify, name="verify"),
    Route("/auth/forgot-password", endpoint=auth.get_forgot_password, name="forgot_password"),
    Route(
        "/auth/post-forgot-password",
        endpoint=auth.post_forgot_password,
        name="post_forgot_password",
        methods=["POST"],
    ),
    Route("/auth/reset-password/{token:str}", endpoint=auth.get_reset_password, name="reset_password"),
    Route("/auth/post-reset-password/{token:str}", endpoint=auth.post_reset_password, name="post_reset_password", methods=["POST"]),
    Route("/auth/send-verify-email", endpoint=auth.send_verify_email, name="send_verify_email"),
    Route("/auth/me", endpoint=auth.get_me_jwt, name="profile"),
    Route("/schema/{schema_type:str}", endpoint=schemas.get_schema, name="schemas"),
    Route("/schemas", endpoint=schemas.get_schemas, name="schemas"),
    Route("/schemas/post-schema", endpoint=schemas.post_schema, name="post_schema", methods=["POST"]),
    Route("/entities", endpoint=entities.get_entities, name="entities"),
    Route("/entities/{schema_type:str}", endpoint=entities.get_entity_create, name="entity_create"),
    Route(
        "/entities/post-entity/{schema_type:str}",
        endpoint=entities.post_entity_create,
        name="post_entity_create",
        methods=["POST"],
    ),
    Route("/entities/view/{uuid:str}", endpoint=entities.get_entity_view, name="entity_view"),
    # proxies
    Route("/search", endpoint=proxies_search.get_records_search, name="records_search"),
    Route("/search/json", endpoint=proxies_search.get_records_search_json, name="records_search_json"),
    Route("/records/{record_id:str}", endpoint=proxies_records.get_record_view, name="record_view"),
    Route("/records/{record_id:str}/json/{type:str}", endpoint=proxies_records.get_record_view_json, name="record_view_json"),
    Route("/{resource_type:str}/{id:str}", endpoint=proxies_resources.get_resources_view, name="collection_view"),
    Route("/{resource_type:str}/{id:str}/json", endpoint=proxies_resources.get_resources_view_json, name="collection_view_json"),
]

# Add test route
if settings["environment"] == "development":
    routes.append(Route("/test", endpoint=testing.test, name="test"))


# Add routes for custom pages
common_pages: Any = []
if "pages" in settings:
    common_pages = settings["pages"]

for common_page in common_pages:
    url = common_page["url"]
    name = common_page["name"]

    routes.append(Route(url, endpoint=pages.default, name=name, methods=["GET"]))
