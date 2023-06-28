import typing
import os
from jinja2 import FileSystemLoader
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from .translate import translate
from .dynamic_settings import get_setting
from .logging import get_log
import json


log = get_log()


def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {"app": request.app}


def get_template_dirs() -> list:
    template_dirs = []

    # local templates
    if os.path.exists("templates"):
        template_dirs.append("templates")
        log.info("Loaded local templates: templates/")
    else:
        log.info("Local templates NOT loaded: templates/")

    # Full path to module templates
    current_dir = os.path.dirname(os.path.realpath(__file__))
    template_module_dirs = current_dir + "/../templates"
    template_dirs.append(template_module_dirs)

    return template_dirs


loader = FileSystemLoader(get_template_dirs())


templates = Jinja2Templates(
    directory="",
    context_processors=[app_context],
    loader=loader,
)


def to_json(variable):
    return json.dumps(variable, indent=4, ensure_ascii=False)


templates.env.globals.update(translate=translate)
templates.env.globals.update(get_setting=get_setting)
templates.env.globals.update(to_json=to_json)
