from logging import basicConfig

from aiohttp import web

from src.config import Config, get_config
from src.converter.routes import routes as converter_routes
from src.converter.service import init_service
from src.middlewares import error_middleware
from src.redis import setup_redis


def init_app(config: Config) -> web.Application:
    app = web.Application(middlewares=[error_middleware])
    app["cfg"] = config
    basicConfig(level=config.LOG_LEVEL)

    app.cleanup_ctx.extend([setup_redis, init_service])

    app.add_routes(converter_routes)
    return app


def main():
    app = init_app(get_config())
    web.run_app(app, host=app["cfg"].APP_HOST, port=int(app["cfg"].APP_PORT))


if __name__ == "__main__":
    main()
