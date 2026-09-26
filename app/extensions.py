"""
Instancias de extensiones de Flask.

Se definen aquí (sin app todavía) para evitar imports circulares:
- models.py importa `db` desde aquí.
- __init__.py importa `db` y `migrate` y los inicializa con `init_app(app)`.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
