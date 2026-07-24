# Validaciones de Seguridad para APIs con FastAPI

Este repositorio tiene como objetivo demostrar distintas técnicas para reforzar la seguridad de APIs desarrolladas con **FastAPI**.

Cada ejemplo está implementado de forma independiente para facilitar el estudio y la comprensión de cómo funcionan las validaciones más comunes utilizadas en aplicaciones reales.

El proyecto irá creciendo con nuevas validaciones y mecanismos de protección, por lo que servirá como una colección de ejemplos prácticos para aprender desarrollo backend y seguridad en APIs.

---

##  Requisitos

Instalar las dependencias:

```bash
pip install fastapi uvicorn
```

---

##  Ejemplos disponibles

### 1. Rate Limiting (HTTP 429)

Archivo:

```text
validacion429.py
```

Ejecutar:

```bash
uvicorn validacion429:app --reload
```

Endpoint disponible:

```http
GET /
GET /saludar
```

**¿Qué demuestra?**

- Limitación de solicitudes por dirección IP.
- Ventana de tiempo configurable.
- Respuesta **HTTP 429 - Too Many Requests** cuando se supera el límite establecido.

---

### 2. Validación mediante API Key

Archivo:

```text
validacion_api_key.py
```

Ejecutar:

```bash
uvicorn validacion_api_key:app --reload
```

Endpoints disponibles:

```http
GET /
GET /saludar
GET /datos-privados
```

Para acceder al endpoint protegido es necesario enviar el header:

```http
x-api-key: 12345
```

---

##  Objetivo del proyecto

Este proyecto tiene fines educativos y busca explicar cómo implementar distintos mecanismos de seguridad en una API utilizando FastAPI.

Con el tiempo se incorporarán nuevas validaciones como:

-  Rate Limiting
-  API Keys
-  Logging de solicitudes
-  Blacklist temporal de IPs
-  Detección de User-Agent sospechosos
-  JWT Authentication
-  Roles y permisos
-  Auditoría de eventos
-  Middleware de seguridad
-  Protección contra fuerza bruta
-  Detección de escaneos automatizados

---

## Tecnologías utilizadas

- Python 3
- FastAPI
- Uvicorn

---

Proyectito para estudiar

-Francisco Toloza
