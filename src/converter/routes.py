from logging import getLogger

from aiohttp import web

from src.converter.models import ConvertCurrecnyQuery, UpdateRatesBody, UpdateRatesQuery
from src.converter.service import ConvertService

routes = web.RouteTableDef()
log = getLogger(__name__)


@routes.get("/convert")
async def convert_currency_handler(req: web.Request):
    convert_service: ConvertService = req.app["convert_service"]
    convert_params = ConvertCurrecnyQuery(**req.query)

    log.debug(f"{convert_params=}")
    converted = await convert_service.convert_currency(convert_params)
    return web.json_response({"result": converted})


@routes.post("/database")
async def update_currency_rates(req: web.Request):
    convert_service: ConvertService = req.app["convert_service"]
    update_params = UpdateRatesQuery(**req.query)

    update_data = None
    if update_params.merge:
        update_data = UpdateRatesBody.parse_raw(await req.text())

    log.debug(f"Updating rates with {update_params=} {update_data=}")
    await convert_service.update(update_params, update_data)
    return web.json_response({"success": True})
