"""
Auth endpoints.
"""

from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.auth import is_authenticated
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core import user
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.api import OpenAwsException
from stadsarkiv_client.core import api
from stadsarkiv_client.endpoints import auth_data

log = get_log()


async def login_get(request: Request):
    next_url = request.query_params.get("next", "/search")
    context_values = {"title": translate("Login"), "post_url": "/auth/login?next=" + next_url}
    context = await get_context(request, context_values=context_values)

    if await api.is_logged_in(request):
        flash.set_message(request, translate("You are already logged in."), type="error", remove=True)
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse(request, "auth/login.html", context)


async def login_post(request: Request):
    next_url = request.query_params.get("next", "/search")
    try:
        await api.auth_jwt_login_post(request)
        flash.set_message(request, translate("You have been logged in."), type="success", remove=True)

        return RedirectResponse(url=next_url, status_code=302)

    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login?next=" + next_url, status_code=302)
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)


async def logout_get(request: Request):
    await is_authenticated(request)
    context_values = {"title": translate("Logout")}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "auth/logout.html", context)


async def logout_post(request: Request):
    try:
        user.logout(request)
        flash.set_message(request, translate("You have been logged out."), type="success")

    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.error("Logout error", exc_info=True)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/auth/login", status_code=302)


async def register_get(request: Request):
    context_values = {"title": translate("Register new user")}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "auth/register.html", context)


async def register_post(request: Request):
    try:
        await api.auth_register_post(request)
        flash.set_message(
            request,
            translate("You have been registered. Check your email to confirm your account."),
            type="success",
        )

        return RedirectResponse(url="/auth/login", status_code=302)
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    return RedirectResponse(url="/auth/register", status_code=302)


async def verify_get(request: Request):
    try:
        await api.auth_verify_post(request)
        flash.set_message(
            request,
            translate("You have been verified."),
            type="success",
        )

        return RedirectResponse(url="/", status_code=302)
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    return RedirectResponse(url="/", status_code=302)


async def me_permission_translated(request: Request):
    permission_list = await api.me_permissions(request)
    permissions_translated = []

    for permission in permission_list:
        permissions_translated.append(translate(f"Permission {permission}"))

    return permissions_translated[-1]


async def me_get(request: Request):
    await is_authenticated(request)
    try:
        me = await api.users_me_get(request)
        me["token"] = request.session["access_token"]
        permissions = await api.me_permissions(request)
        permission_translated = user.permission_translated(permissions)

        context_values = {"title": translate("Profile"), "me": me, "permission_translated": permission_translated}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse(request, "auth/me.html", context)
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def orders(request: Request):
    await is_authenticated(request)
    try:
        me = await api.users_me_get(request)
        context_values = {"title": translate("Your orders"), "me": me, "orders": auth_data.api_orders}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse(request, "auth/orders.html", context)
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def bookmarks(request: Request):
    await is_authenticated(request)
    try:
        me = await api.users_me_get(request)
        context_values = {"title": translate("Your bookmarks"), "me": me, "bookmarks": auth_data.api_booksmarks}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse(request, "auth/bookmarks.html", context)
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def search_results(request: Request):
    await is_authenticated(request)
    try:
        me = await api.users_me_get(request)
        context_values = {"title": translate("Your search results"), "me": me, "search_results": auth_data.api_search_results}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse(request, "auth/search_results.html", context)
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def forgot_password_get(request: Request):
    context_values = {"title": translate("Forgot your password")}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "auth/forgot_password.html", context)


async def forgot_password_post(request: Request):
    try:
        await api.auth_forgot_password(request)
        flash.set_message(
            request,
            translate("An email has been sent to you with instructions on how to reset your password."),
            type="success",
        )
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    return RedirectResponse(url="/auth/forgot-password", status_code=302)


async def reset_password_get(request: Request):
    token = request.path_params["token"]
    context_values = {"title": translate("Enter new password"), "token": token}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "auth/reset_password.html", context)


async def reset_password_post(request: Request):
    try:
        await api.auth_reset_password_post(request)
        flash.set_message(
            request,
            translate("Your password has been reset. You can now login."),
            type="success",
        )
        return RedirectResponse(url="/auth/login", status_code=302)

    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    token = request.path_params["token"]
    return RedirectResponse(url="/auth/reset-password/" + token, status_code=302)


async def send_verify_email(request: Request):
    try:
        await api.auth_request_verify_post(request)
        flash.set_message(
            request,
            translate("A verify link has been sent to your email. You may verify your account now by clicking the link."),
            type="success",
        )

    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    return RedirectResponse(url="/auth/me", status_code=302)


async def me_post(request: Request):
    is_logged_in = await api.is_logged_in(request)
    return JSONResponse({"is_logged_in": is_logged_in})
