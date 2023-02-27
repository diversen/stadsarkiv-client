import typing
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from .flash import get_messages
from stadsarkiv_client.utils import dynamic_settings

def get_main_menu() -> typing.List[str]:
    main_menu = []
    if "main_menu" in dynamic_settings.settings:
        main_menu = dynamic_settings.settings["main_menu"]
    return main_menu

def get_title(request: Request) -> str:
    pages = []
    title = "No title"
    if "pages" in dynamic_settings.settings:
        pages = dynamic_settings.settings["pages"]

    for page in pages:
        if page["url"] == request.url.path:
            title = page["title"]
    return title

def get_context(request: Request) -> typing.Dict[str, typing.Any]:
    dict_values = {
        'path': request.url.path,
        'request': request,
        'title': get_title(request),
        'flash_messages': get_messages(request),
        'main_menu': get_main_menu(),
    }

    return dict_values