from flask import Blueprint, render_template, request

from app.extensions import db
from app.models import Habito, Registro
from app.services.racha_service import (
    resumen_habito,
    resumen_general_desde_resumenes,
    hoy_mexico,
)

habitos_bp = Blueprint("habitos", __name__)


def _todos_los_resumenes():
    habitos = Habito.query.order_by(Habito.fecha_creacion.desc()).all()
    return [resumen_habito(h) for h in habitos]


def _barra_resumen_actualizada():
    """Fragmento OOB con la barra de resumen recalculada, para pegarlo
    al final de cualquier respuesta que cambie el estado de los hábitos."""
    resumen_general = resumen_general_desde_resumenes(_todos_los_resumenes())
    return render_template("partials/resumen_general.html", resumen_general=resumen_general)


@habitos_bp.route("/")
def index():
    resumenes = _todos_los_resumenes()
    resumen_general = resumen_general_desde_resumenes(resumenes)
    return render_template("index.html", resumenes=resumenes, resumen_general=resumen_general)


@habitos_bp.route("/habitos", methods=["POST"])
def crear_habito():
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip() or None

    if not nombre:
        return render_template(
            "partials/form_error.html",
            mensaje="El nombre es obligatorio.",
        ), 400

    habito = Habito(nombre=nombre, descripcion=descripcion)
    db.session.add(habito)
    db.session.commit()

    tarjeta = render_template("partials/habito_card.html", resumen=resumen_habito(habito))
    return tarjeta + _barra_resumen_actualizada()


@habitos_bp.route("/habitos/<int:habito_id>", methods=["DELETE"])
def eliminar_habito(habito_id):
    habito = Habito.query.get_or_404(habito_id)
    db.session.delete(habito)
    db.session.commit()

    # Sin contenido "principal": el swap del botón de eliminar recibe
    # una cadena vacía y quita la tarjeta; la barra viaja aparte como OOB.
    return _barra_resumen_actualizada()


@habitos_bp.route("/habitos/<int:habito_id>", methods=["PUT"])
def editar_habito(habito_id):
    habito = Habito.query.get_or_404(habito_id)
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip() or None

    if not nombre:
        return render_template(
            "partials/form_error.html",
            mensaje="El nombre es obligatorio.",
        ), 400

    habito.nombre = nombre
    habito.descripcion = descripcion
    db.session.commit()

    tarjeta = render_template("partials/habito_card.html", resumen=resumen_habito(habito))
    return tarjeta + _barra_resumen_actualizada()


@habitos_bp.route("/habitos/<int:habito_id>/cumplir", methods=["POST"])
def marcar_cumplido(habito_id):
    habito = Habito.query.get_or_404(habito_id)
    hoy = hoy_mexico()

    ya_existe = Registro.query.filter_by(habito_id=habito.id, fecha=hoy).first()
    if not ya_existe:
        db.session.add(Registro(habito_id=habito.id, fecha=hoy))
        db.session.commit()

    tarjeta = render_template("partials/habito_card.html", resumen=resumen_habito(habito))
    return tarjeta + _barra_resumen_actualizada()