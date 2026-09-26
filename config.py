import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base compartida por todos los entornos."""

    # Supabase entrega la cadena de conexión como postgres://...
    # SQLAlchemy 2.x requiere el prefijo postgresql://
    _raw_db_url = os.environ.get("DATABASE_URL", "")
    if _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-cambia-esto")

    # Zona horaria de referencia para calcular "hoy" y las rachas.
    # Todo el cálculo de fechas de la app pasa por esta zona, sin importar
    # en qué región esté corriendo el servidor (Render usa UTC por defecto).
    APP_TIMEZONE = "America/Mexico_City"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
