from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.api_client.api_schemas import APISchema
from stadsarkiv_client.api_client.api_base import APIBase
# from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash
from json import JSONDecodeError
import json
log = get_log()


async def get_entity_create(request: Request):

    schema_type = request.path_params['schema_type']

    api_schema = APISchema(request=request)
    schema = await api_schema.get_schema(schema_type=schema_type, as_text=True)
    schema = schema.decode("utf-8")

    context_values = {"title": translate("Entities"), "schema": schema}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse('entities/entities.html', context)


async def post_entity_create(request: Request):

    schema_type = request.path_params['schema_type']
    log.debug(schema_type)

    # get body json from request
    body = await request.json()

    api_schema = APISchema(request=request)
    

    log.debug("POST ENTITY CREATE")
    log.debug(schema_type)
    log.debug(body)

    return JSONResponse({"message": "Hello, world!"})

    # return json.dumps(body)

    
"""     api_schema = APISchema(request=request)
    schema = await api_schema.get_schema(schema_type=schema_type, as_text=True)
    schema = schema.decode("utf-8")

    log.debug(schema)

    context_values = {"title": translate("Entities"), "schema": schema}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse('entities/entities.html', context) """


async def post_entity(request: Request):

    try:

        form = await request.form()
        type = str(form.get('type'))
        data = str(form.get('data'))

        data_dict = {}
        data_dict["type"] = type

        data = json.loads(data)
        data_dict["data"] = data

        schema = APIBase(request=request)
        schema.jwt_post_json(url="/schemas/", json=data_dict)
        flash.set_message(request, translate("Schema created."), type="success")

    except JSONDecodeError:
        flash.set_message(request, translate("Invalid JSON in data."), type="error")
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")

    return RedirectResponse(url='/schemas', status_code=302)
