from flask import Flask

from .services.http.api import BookRoutes
from .services.postgres.provider import PostgresProvider
from .dependencies import get_flask_app, http_settings, db_settings


def init_pg_provider() -> PostgresProvider | None:
    return PostgresProvider(db_settings)


def init_book_routing(app: Flask, pg_provider: PostgresProvider):
    BookRoutes(app, pg_provider)


def main() -> None:
    app = get_flask_app()
    pg_provider = init_pg_provider()
    init_book_routing(app, pg_provider)
    app.run(debug=True, port=http_settings.port)


if __name__ == "__main__":
    main()
