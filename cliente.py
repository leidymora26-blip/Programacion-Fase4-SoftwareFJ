# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de gestión de clientes.

# Importamos la biblioteca de expresiones regulares.
import re

# Importamos la clase abstracta Entidad.
from entidad import Entidad

# Importamos la excepción personalizada.
from excepciones import DatosInvalidosError

# Importamos las funciones de registro de eventos y errores.
from config_logs import registrar_evento, registrar_excepcion


# Definimos la clase Cliente que hereda de Entidad.
class Cliente(Entidad):

    # Constructor de la clase Cliente.
    def __init__(self, identificador, nombre, correo, telefono):

        # Validamos que la identificación contenga solo números.
        if not isinstance(identificador, str) or not identificador.isdigit():
            raise DatosInvalidosError(
                "La identificación debe contener únicamente números."
            )

        # Invocamos el constructor de la clase padre.
        super().__init__(identificador, nombre)

        # Asignamos el correo mediante su propiedad.
        self.correo = correo

        # Asignamos el teléfono mediante su propiedad.
        self.telefono = telefono

    # Propiedad para consultar el correo electrónico.
    @property
    def correo(self):
        return self.__correo

    # Método para modificar y validar el correo.
    @correo.setter
    def correo(self, nuevo_correo):

        # Definimos el patrón para validar correos electrónicos.
        patron = r"[^@\s]+@[^@\s]+\.[^@\s]+"

        # Verificamos que el correo tenga un formato válido.
        if not isinstance(nuevo_correo, str) or not re.fullmatch(
            patron, nuevo_correo
        ):
            raise DatosInvalidosError(
                "El correo electrónico no es válido."
            )

        # Guardamos el correo como atributo privado.
        self.__correo = nuevo_correo

    # Propiedad para consultar el teléfono.
    @property
    def telefono(self):
        return self.__telefono

    # Método para modificar y validar el teléfono.
    @telefono.setter
    def telefono(self, nuevo_telefono):

        # Validamos que el teléfono tenga diez dígitos.
        if (
            not isinstance(nuevo_telefono, str)
            or not nuevo_telefono.isdigit()
            or len(nuevo_telefono) != 10
        ):
            raise DatosInvalidosError(
                "El teléfono debe contener 10 dígitos."
            )

        # Guardamos el teléfono como atributo privado.
        self.__telefono = nuevo_telefono

    # Sobrescribimos el método abstracto de Entidad.
    def mostrar_informacion(self):

        # Retornamos la información completa del cliente.
        return (
            f"Identificación: {self.identificador}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Mostramos el encabezado de las pruebas.
    print("=== PRUEBAS DEL MÓDULO CLIENTE ===")

    # PRUEBA 1: Creación de un cliente válido.
    try:
        cliente1 = Cliente(
            "1001234567",
            "Ana Rodríguez",
            "ana@example.com",
            "3001234567"
        )

    # Capturamos posibles errores.
    except DatosInvalidosError as error:
        registrar_excepcion(str(error))
        print(f"Error: {error}")

    # Ejecutamos este bloque si no se presentan errores.
    else:
        registrar_evento("Cliente de prueba creado correctamente.")
        print("\nCliente registrado correctamente.")
        print(cliente1.mostrar_informacion())

    # PRUEBA 2: Cliente con correo incorrecto.
    try:
        cliente2 = Cliente(
            "1001234568",
            "Carlos Pérez",
            "correo_invalido",
            "3101234567"
        )

    # Capturamos y registramos el error.
    except DatosInvalidosError as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # PRUEBA 3: Cliente con teléfono incorrecto.
    try:
        cliente3 = Cliente(
            "1001234569",
            "María López",
            "maria@example.com",
            "12345"
        )

    # Capturamos y registramos el error.
    except DatosInvalidosError as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # Finalizamos las pruebas del módulo.
    finally:
        print("\nPruebas del módulo Cliente finalizadas.")
