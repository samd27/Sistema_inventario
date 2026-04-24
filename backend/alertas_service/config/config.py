import os
import ssl


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "alertas-service-dev-secret"

    MICROSERVICES_DATABASE_URL = os.environ.get("MICROSERVICES_DATABASE_URL") or \
        "mysql+pymysql://root:@localhost:3306/tienda_microservicios?charset=utf8mb4"
    INVENTORY_API_URL = os.environ.get("INVENTORY_API_URL") or "http://127.0.0.1:8080"

    SQLALCHEMY_DATABASE_URI = MICROSERVICES_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BREVO_API_KEY = os.environ.get("BREVO_API_KEY") or ""
    BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL") or ""
    BREVO_SENDER_NAME = os.environ.get("BREVO_SENDER_NAME") or ""
    BREVO_API_URL = os.environ.get("BREVO_API_URL") or "https://api.brevo.com/v3/smtp/email"
    ALERTS_TO_EMAIL = os.environ.get("ALERTS_TO_EMAIL") or ""

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {
            "ssl": ssl_context
        }
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
