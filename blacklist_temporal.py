import time

from fastapi import FastAPI, HTTPException, Request

app = FastAPI(
    title="Blacklist temporal de IPs",
    description="Ejemplo educativo de bloqueo temporal por abuso de solicitudes",
    version="1.0.0",
)

# Guarda las solicitudes recientes de cada IP.
#
# Ejemplo:
# {
#     "127.0.0.1": [1721840000.1, 1721840001.8]
solicitudes_por_ip: dict[str, list[float]] = {}

# Guarda las IP bloqueadas y el momento exacto
# en que termina su bloqueo. (la lista de arriba xD)
#
# Ejemplo:
# {
#     "127.0.0.1": 1721840030.5
# }
ips_bloqueadas: dict[str, float] = {}

LIMITE_SOLICITUDES = 3
VENTANA_SEGUNDOS = 5
TIEMPO_BLOQUEO_SEGUNDOS = 30


def obtener_ip_cliente(request: Request) -> str:
    """
    Obtiene la IP del cliente que realizó la solicitud.
    """

    if request.client is None:
        return "IP-desconocida"

    return request.client.host


def verificar_blacklist(ip_cliente: str) -> None:
    """
    Revisa si una IP está bloqueada.

    Si el tiempo de bloqueo ya terminó, elimina la IP
    de la blacklist y permite que continúe.
    """

    desbloqueo_en = ips_bloqueadas.get(ip_cliente)

    # La IP no está bloqueada.
    if desbloqueo_en is None:
        return

    ahora = time.time()

    # El bloqueo ya expiró.
    if ahora >= desbloqueo_en:
        ips_bloqueadas.pop(ip_cliente, None)
        solicitudes_por_ip.pop(ip_cliente, None)

        print(f"[DESBLOQUEO] IP {ip_cliente} eliminada de la blacklist")
        return

    segundos_restantes = max(1, int(desbloqueo_en - ahora) + 1)

    print(
        f"[BLOQUEADA] IP {ip_cliente} intentó acceder. "
        f"Restan {segundos_restantes} segundos."
    )

    raise HTTPException(
        status_code=429,
        detail={
            "mensaje": "IP bloqueada temporalmente",
            "segundos_restantes": segundos_restantes,
        },
        headers={
            "Retry-After": str(segundos_restantes),
        },
    )


def registrar_solicitud(ip_cliente: str) -> int:
    """
    Registra una solicitud y controla si la IP supera el límite.

    Retorna la cantidad de solicitudes que todavía puede realizar
    dentro de la ventana actual.
    """

    ahora = time.time()

    historial = solicitudes_por_ip.get(ip_cliente, [])

    # Conservamos únicamente las solicitudes realizadas
    # dentro de los últimos 5 segundos.
    solicitudes_recientes = [
        timestamp
        for timestamp in historial
        if ahora - timestamp < VENTANA_SEGUNDOS
    ]

    # Si ya había realizado 3 solicitudes recientes,
    # este nuevo intento provoca el bloqueo.
    if len(solicitudes_recientes) >= LIMITE_SOLICITUDES:
        desbloqueo_en = ahora + TIEMPO_BLOQUEO_SEGUNDOS

        ips_bloqueadas[ip_cliente] = desbloqueo_en
        solicitudes_por_ip.pop(ip_cliente, None)

        print(
            f"[ALERTA] IP {ip_cliente} superó el límite. "
            f"(****************************************************)"
            #Aqui nos printiara en la terminal un msj de alerta que dice que la ip XXX.XXX.XXX fue bloqueada por 30 segundos
            f"Bloqueada durante {TIEMPO_BLOQUEO_SEGUNDOS} segundos."
        )

        raise HTTPException(
            status_code=429,
            detail={
                "mensaje": "Demasiadas solicitudes",
                "bloqueo_segundos": TIEMPO_BLOQUEO_SEGUNDOS,
            },
            headers={
                "Retry-After": str(TIEMPO_BLOQUEO_SEGUNDOS),
            },
        )

    solicitudes_recientes.append(ahora)
    solicitudes_por_ip[ip_cliente] = solicitudes_recientes

    solicitudes_restantes = (
        LIMITE_SOLICITUDES - len(solicitudes_recientes)
    )

    return solicitudes_restantes


@app.get("/")
def inicio():
    return {
        "mensaje": "API con blacklist temporal",
        "limite_solicitudes": LIMITE_SOLICITUDES,
        "ventana_segundos": VENTANA_SEGUNDOS,
        "tiempo_bloqueo_segundos": TIEMPO_BLOQUEO_SEGUNDOS,
    }


@app.get("/saludar")
def saludar(request: Request):
    ip_cliente = obtener_ip_cliente(request)

    # Primera barrera:
    # comprobar si la IP ya está bloqueada.
    verificar_blacklist(ip_cliente)

    # Segunda barrera:
    # registrar la solicitud y comprobar abuso.
    solicitudes_restantes = registrar_solicitud(ip_cliente)

    return {
        "mensaje": "Solicitud permitida",
        "ip_cliente": ip_cliente,
        "solicitudes_restantes": solicitudes_restantes,
    }


@app.get("/estado-blacklist")
def estado_blacklist():
    """
    Endpoint educativo para revisar los bloqueos activos.

    En producción debería estar protegido o no existir.
    """

    ahora = time.time()
    bloqueos_activos = []

    for ip, desbloqueo_en in list(ips_bloqueadas.items()):
        if ahora >= desbloqueo_en:
            ips_bloqueadas.pop(ip, None)
            solicitudes_por_ip.pop(ip, None)
            continue

        bloqueos_activos.append(
            {
                "ip": ip,
                "segundos_restantes": max(
                    1,
                    int(desbloqueo_en - ahora) + 1,
                ),
            }
        )

    return {
        "cantidad_ips_bloqueadas": len(bloqueos_activos),
        "ips_bloqueadas": bloqueos_activos,
    }