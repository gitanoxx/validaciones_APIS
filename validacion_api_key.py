from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
#Esta es la llave de prueba para el ejemplo
API_KEY_VALIDA = "12345"





#Creacion de la validacion de la api key del usuario
def validar_api_key(
    x_api_key: str | None = Header(default=None)
):
    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Falta la API Key"
        )
    #IF que gatilla un error 403 si la api key no es valida
    if x_api_key != API_KEY_VALIDA:
        raise HTTPException(
            status_code=403,
            detail="API Key inválida"
        )
    #Retorno
    return x_api_key


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando"
    }


@app.get("/saludar")
def saludar():
    return {
        "mensaje": "Endpoint público"
    }

# Endpoint con info potencialmente sensible, protegida con la validacion de la api key anterior 
@app.get("/datos-privados")
def datos_privados(
    api_key: str = Header(alias="x-api-key")
):
    #Si la api key es invalida gatilla un 403
    if api_key != API_KEY_VALIDA:
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )
    #Retorna los datos del endpoind si la api key es la valida
    return {
        "mensaje": "Acceso autorizado",
        "datos": [
            "vehículo ABCD12",
            "GPS instalado",
            "SIM activa"
        ]
    }