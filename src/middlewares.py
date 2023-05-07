from logging import getLogger

from aiohttp import web
from pydantic import ValidationError

log = getLogger(__name__)


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response

    except ValidationError as exc:
        message = exc.errors()
        status = 422

    except Exception as exc:
        log.error("Unhandled exception")
        log.exception(exc)
        message = "Internal Error"
        status = 500

    return web.json_response({"error": message}, status=status)
