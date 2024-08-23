from flask import Flask

from api.services.postgres.provider import PostgresProvider
from api.settings import HttpSettings, PostgresSettings

http_settings = HttpSettings()
db_settings = PostgresSettings()

__pd_provider = PostgresProvider(db_settings)
__app = Flask(__name__)


def get_pg_provider() -> PostgresProvider:
    return __pd_provider


def get_flask_app() -> Flask:
    return __app
