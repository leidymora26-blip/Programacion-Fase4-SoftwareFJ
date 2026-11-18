# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de configuración del registro de eventos y errores.

# Importamos la biblioteca para gestionar los registros.
import logging

# Importamos Path para gestionar la ruta del archivo.
from pathlib import Path

# Definimos la ubicación del archivo de logs.
RUTA_LOG = Path(__file__).resolve().parent / "software_fj.log"

# Configuramos el sistema de registro de eventos.
logging.basicConfig(
    filename=RUTA_LOG,  # Nombre y ubicación del archivo.
    level=logging.DEBUG,  # Nivel mínimo de registro.
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",  # Formato de fecha y hora.
    encoding="utf-8",  # Permite utilizar caracteres especiales.
    filemode="a"  # Conserva los registros anteriores.
)

# Creamos el objeto encargado de registrar los eventos.
logger = logging.getLogger("Software_FJ")


# Función para registrar operaciones exitosas.
def registrar_evento(mensaje):
    logger.info(mensaje)


# Función para registrar advertencias.
def registrar_advertencia(mensaje):
    logger.warning(mensaje)


# Función para registrar errores.
def registrar_error(mensaje):
    logger.error(mensaje)


# Función para registrar excepciones con su detalle técnico.
def registrar_excepcion(mensaje):
    logger.exception(mensaje)


# Comprobamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Simulamos diferentes tipos de registros.
    registrar_evento("Sistema Software FJ iniciado correctamente.")
    registrar_advertencia("Advertencia de prueba.")
    registrar_error("Error de prueba controlado.")

    # Informamos que la prueba terminó correctamente.
    print("Archivo de logs generado correctamente.")
