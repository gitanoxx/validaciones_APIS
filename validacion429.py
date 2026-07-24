import time

from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

# Guarda las solicitudes realizadas por cada IP.
# Ejemplo:
# {
#     "127.0.0.1": [tiempo1, tiempo2, tiempo3]
# }
solicitudes_por_ip: dict[str, list[float]] = {}
# Esto significa que si enviamos mas de 3 solicitudes en una ventana de 10 segundos nos va a devolver un 429 too many request
#al 4to intento
LIMITE_SOLICITUDES = 3
VENTANA_SEGUNDOS = 10


@app.get("/")
def inicio():
    return {
        "mensaje": "Hola Francisco"
    }

@app.get("/saludar")
def saludar(request: Request):
    # Aqui recepcionamos la ip del cliente y el tiempo actual en segundos
    ip_cliente = request.client.host
    tiempo_actual = time.time()

    # Obtenemos las solicitudes anteriores de esta IP.
    solicitudes = solicitudes_por_ip.get(ip_cliente, [])

    # Conservamos solamente las solicitudes realizadas
    # durante los últimos 10 segundos.
    solicitudes_recientes = [
        solicitud
        for solicitud in solicitudes
        if tiempo_actual - solicitud < VENTANA_SEGUNDOS
    ]
    # Si ya realizó 3 solicitudes recientes, la bloqueamos.
    if len(solicitudes_recientes) >= LIMITE_SOLICITUDES:
        raise HTTPException(
            status_code=429,
            detail="Demasiadas solicitudes. Intenta nuevamente en unos segundos."
        )
    # Registramos la solicitud actual.
    solicitudes_recientes.append(tiempo_actual)
    solicitudes_por_ip[ip_cliente] = solicitudes_recientes
    solicitudes_disponibles = (
        LIMITE_SOLICITUDES - len(solicitudes_recientes)
    )
    return {
        "nombre": "Francisco",
        "cargo": "Backend Developer",
        "solicitudes_disponibles": solicitudes_disponibles
    }