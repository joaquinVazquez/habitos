from datetime import date, timedelta
from zoneinfo import ZoneInfo

MEXICO_TZ = ZoneInfo("America/Mexico_City")


def hoy_mexico() -> date:
    """'Hoy' siempre calculado en hora de México, sin importar dónde
    corra el servidor (Render usa UTC internamente)."""
    from datetime import datetime
    return datetime.now(MEXICO_TZ).date()


def calcular_racha(habito, hoy: date | None = None) -> int:
    """Cuenta días consecutivos con registro, empezando hoy y retrocediendo.
    En cuanto falta un día en la secuencia, la racha se corta ahí."""
    hoy = hoy or hoy_mexico()
    fechas_cumplidas = {r.fecha for r in habito.registros}

    racha = 0
    dia = hoy
    while dia in fechas_cumplidas:
        racha += 1
        dia -= timedelta(days=1)
    return racha

def calcular_racha_maxima(habito) -> int:
    """Encuentra la racha más larga en todo el historial, no solo la que
    sigue activa hasta hoy. Recorre las fechas ordenadas y mide la
    secuencia consecutiva más larga que aparezca en cualquier punto."""
    fechas = sorted({r.fecha for r in habito.registros})
    if not fechas:
        return 0

    mejor = racha_en_curso = 1
    for i in range(1, len(fechas)):
        if fechas[i] == fechas[i - 1] + timedelta(days=1):
            racha_en_curso += 1
        else:
            racha_en_curso = 1
        mejor = max(mejor, racha_en_curso)

    return mejor


def ultimos_7_dias(habito, hoy: date | None = None) -> list[dict]:
    """Devuelve los últimos 7 días (incluyendo hoy) en orden cronológico,
    cada uno marcado si tuvo registro."""
    hoy = hoy or hoy_mexico()
    fechas_cumplidas = {r.fecha for r in habito.registros}

    return [
        {
            "fecha": hoy - timedelta(days=i),
            "cumplido": (hoy - timedelta(days=i)) in fechas_cumplidas,
            "es_hoy": i == 0,
        }
        for i in range(6, -1, -1)
    ]


def ya_cumplido_hoy(habito, hoy: date | None = None) -> bool:
    hoy = hoy or hoy_mexico()
    return hoy in {r.fecha for r in habito.registros}


def resumen_habito(habito) -> dict:
    """Empaqueta todo lo que necesita la tarjeta: datos del hábito +
    racha + últimos 7 días + si ya se marcó hoy. Un solo punto de verdad
    para index() y para cada ruta que devuelve el partial de la tarjeta."""
    hoy = hoy_mexico()
    return {
        "id": habito.id,
        "nombre": habito.nombre,
        "descripcion": habito.descripcion,
        "racha": calcular_racha(habito, hoy),
        "racha_maxima": calcular_racha_maxima(habito),
        "dias": ultimos_7_dias(habito, hoy),
        "cumplido_hoy": ya_cumplido_hoy(habito, hoy),
    }

def resumen_general_desde_resumenes(resumenes: list[dict]) -> dict:
    """Agrega los resúmenes individuales en las 3 métricas de la barra
    superior. Recibe la lista ya calculada para no recalcular cada
    hábito dos veces en la misma petición."""
    return {
        "total_habitos": len(resumenes),
        "racha_mas_alta": max((r["racha"] for r in resumenes), default=0),
        "cumplidos_hoy": sum(1 for r in resumenes if r["cumplido_hoy"]),
    }

