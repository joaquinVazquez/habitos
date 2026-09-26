from datetime import datetime

from app.extensions import db


class Habito(db.Model):
    __tablename__ = "habitos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Si se borra un hábito, se borran en cascada todos sus registros.
    # passive_deletes="all" delega el borrado a la base de datos (ondelete="CASCADE")
    # en vez de cargar todos los registros en memoria para borrarlos uno por uno.
    registros = db.relationship(
        "Registro",
        backref="habito",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Registro.fecha.desc()",
    )

    def __repr__(self):
        return f"<Habito {self.id} {self.nombre!r}>"


class Registro(db.Model):
    __tablename__ = "registros"

    id = db.Column(db.Integer, primary_key=True)
    habito_id = db.Column(
        db.Integer,
        db.ForeignKey("habitos.id", ondelete="CASCADE"),
        nullable=False,
    )
    fecha = db.Column(db.Date, nullable=False, server_default=db.func.current_date())

    # Un hábito no puede tener dos registros el mismo día.
    # Esto es la garantía a nivel de base de datos; en la ruta también
    # validamos antes de insertar para dar un mensaje claro al usuario.
    __table_args__ = (
        db.UniqueConstraint("habito_id", "fecha", name="uq_habito_fecha"),
    )

    def __repr__(self):
        return f"<Registro habito={self.habito_id} fecha={self.fecha}>"
