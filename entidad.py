# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de la clase abstracta Entidad.

# Importamos las herramientas para crear clases abstractas.
from abc import ABC, abstractmethod

# Importamos la excepción personalizada para datos inválidos.
from excepciones import DatosInvalidosError


# Definimos la clase abstracta Entidad.
class Entidad(ABC):

    # Constructor de la clase.
    def __init__(self, identificador, nombre):

        # Validamos que el identificador sea un texto válido.
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError(
                "El identificador no puede estar vacío."
            )

        # Validamos que el nombre sea un texto válido.
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre no puede estar vacío."
            )

        # Almacenamos el identificador como atributo privado.
        self.__identificador = identificador.strip()

        # Almacenamos el nombre como atributo privado.
        self.__nombre = nombre.strip()

    # Propiedad para consultar el identificador.
    @property
    def identificador(self):
        return self.__identificador

    # Propiedad para consultar el nombre.
    @property
    def nombre(self):
        return self.__nombre

    # Método para modificar el nombre de forma controlada.
    @nombre.setter
    def nombre(self, nuevo_nombre):

        # Validamos el nuevo nombre.
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise DatosInvalidosError(
                "El nuevo nombre no puede estar vacío."
            )

        # Actualizamos el atributo privado.
        self.__nombre = nuevo_nombre.strip()

    # Método abstracto que deben implementar las clases hijas.
    @abstractmethod
    def mostrar_informacion(self):
        pass


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Importamos la función para registrar excepciones.
    from config_logs import registrar_excepcion

    # Intentamos crear un objeto de una clase abstracta.
    try:
        entidad = Entidad("E001", "Entidad de prueba")

    # Capturamos el error generado por Python.
    except TypeError:
        registrar_excepcion(
            "Intento de instanciar una clase abstracta."
        )

        # Informamos que el error fue controlado.
        print("Validación de abstracción exitosa.")
        print("No se puede instanciar una clase abstracta.")

    # Ejecutamos este bloque independientemente del resultado.
    finally:
        print("Prueba del módulo Entidad finalizada.")
