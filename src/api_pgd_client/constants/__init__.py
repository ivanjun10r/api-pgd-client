from decouple import config

REQUEST_TIMEOUT = config("PGD_API_REQUEST_TIMEOUT", default=300, cast=int)

BASE_URL = config("PGD_API_URL", default="https://api-pgd.dth.api.gov.br/")

SOURCE_SYSTEM_NAME = config("PGD_SOURCE_SYSTEM_NAME")
SOURCE_SYSTEM_VERSION = config("PGD_SOURCE_SYSTEM_VERSION")
SOURCE_SYSTEM_ABOUT_URL = config(
    "PGD_SOURCE_SYSTEM_ABOUT_URL", default="url não informada"
)

API_USERNAME = config("PGD_API_USERNAME")
API_PASSWORD = config("PGD_API_PASSWORD")
