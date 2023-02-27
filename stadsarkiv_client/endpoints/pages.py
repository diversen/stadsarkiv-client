from starlette.requests import Request
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.utils.logging import log

 
async def default(request: Request):

    context = get_context(request)
    return templates.TemplateResponse('pages/about.html', context)
