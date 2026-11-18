# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de gestión de reservas.

# Importamos las clases necesarias.
from cliente import Cliente
from servicio import Servicio

# Importamos las excepciones personalizadas.
from excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ErrorSistema
)

# Importamos las funciones de registro de eventos.
from config_logs import registrar_evento, registrar_excepcion

# Definimos la clase Reserva.
class Reserva:

    # Constructor de la clase.
    def __init__(self, identificador, cliente, servicio,
                 duracion, impuesto=0, descuento=0):

        # Validamos el identificador de la reserva.
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError(
                "El código de la reserva no puede estar vacío."
            )

        # Validamos que el cliente sea un objeto de la clase Cliente.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "Debe asignarse un cliente válido."
            )

        # Validamos que el servicio sea un objeto de la clase Servicio.
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "Debe asignarse un servicio válido."
            )

        # Validamos la duración de la reserva.
        servicio.validar_duracion(duracion)

        # Calculamos el costo inicial mediante polimorfismo.
        costo = servicio.calcular_costo(
            duracion, impuesto, descuento
        )

        # Almacenamos los atributos privados de la reserva.
        self.__identificador = identificador.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__impuesto = impuesto
        self.__descuento = descuento
        self.__costo = costo

        # Asignamos el estado inicial.
        self.__estado = "Pendiente"

    # Propiedad para consultar el código.
    @property
    def identificador(self):
        return self.__identificador

    # Propiedad para consultar el cliente.
    @property
    def cliente(self):
        return self.__cliente

    # Propiedad para consultar el servicio.
    @property
    def servicio(self):
        return self.__servicio

    # Propiedad para consultar la duración.
    @property
    def duracion(self):
        return self.__duracion

    # Propiedad para consultar el impuesto.
    @property
    def impuesto(self):
        return self.__impuesto

    # Propiedad para consultar el descuento.
    @property
    def descuento(self):
        return self.__descuento

    # Propiedad para consultar el costo.
    @property
    def costo(self):
        return self.__costo

    # Propiedad para consultar el estado.
    @property
    def estado(self):
        return self.__estado

    # Método para confirmar una reserva.
    def confirmar(self):

        # Verificamos que la reserva esté pendiente.
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        # Verificamos la disponibilidad del servicio.
        self.servicio.verificar_disponibilidad()

        # Actualizamos el costo antes de confirmar.
        self.__costo = self.servicio.calcular_costo(
            self.duracion, self.impuesto, self.descuento
        )

        # Marcamos el servicio como ocupado.
        self.servicio.disponible = False

        # Actualizamos el estado de la reserva.
        self.__estado = "Confirmada"

        # Registramos la operación realizada.
        registrar_evento(
            f"Reserva {self.identificador} confirmada."
        )

        # Retornamos el mensaje de confirmación.
        return "Reserva confirmada correctamente."

    # Método para cancelar una reserva.
    def cancelar(self):

        # Validamos que la cancelación esté permitida.
        if self.estado not in ("Pendiente", "Confirmada"):
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva "
                "procesada o cancelada."
            )

        # Liberamos el servicio si esta reserva lo ocupaba.
        if self.estado == "Confirmada":
            self.servicio.disponible = True

        # Actualizamos el estado de la reserva.
        self.__estado = "Cancelada"

        # Registramos la operación.
        registrar_evento(
            f"Reserva {self.identificador} cancelada."
        )

        # Retornamos el mensaje de cancelación.
        return "Reserva cancelada correctamente."

    # Método para procesar una reserva.
    def procesar(self):

        # Intentamos realizar el procesamiento.
        try:

            # Validamos que la reserva esté confirmada.
            if self.estado != "Confirmada":
                raise OperacionNoPermitidaError(
                    "Solo se pueden procesar "
                    "reservas confirmadas."
                )

            # Actualizamos el estado.
            self.__estado = "Procesada"

            # Liberamos el servicio para nuevas reservas.
            self.servicio.disponible = True

        # Capturamos los errores del sistema.
        except ErrorSistema as error:

            # Registramos la excepción.
            registrar_excepcion(str(error))

            # Propagamos el error para que pueda ser controlado.
            raise

        # Ejecutamos este bloque si no existen errores.
        else:

            # Registramos el procesamiento exitoso.
            registrar_evento(
                f"Reserva {self.identificador} procesada."
            )

            # Retornamos el mensaje de éxito.
            return "Reserva procesada correctamente."

        # Registramos la finalización del intento.
        finally:
            registrar_evento(
                f"Intento de procesamiento de "
                f"reserva {self.identificador} finalizado."
            )

    # Método para mostrar la información de la reserva.
    def mostrar_informacion(self):

        # Retornamos los datos completos.
        return (
            f"Código: {self.identificador}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duración: {self.duracion} horas\n"
            f"Impuesto: {self.impuesto}%\n"
            f"Descuento: {self.descuento}%\n"
            f"Costo total: ${self.costo:,.2f}\n"
            f"Estado: {self.estado}"
        )

# Verificamos si el módulo se ejecuta directamente.
if __name__ == "__main__":

    # Importamos un servicio especializado para las pruebas.
    from reserva_sala import ReservaSala

    # Mostramos el encabezado de las pruebas.
    print("=== PRUEBAS DEL MÓDULO RESERVA ===")

    # Creamos un cliente ficticio.
    cliente = Cliente(
        "1001234567",
        "Ana Rodríguez",
        "ana@example.com",
        "3001234567"
    )

    # Creamos una sala de conferencias.
    sala = ReservaSala(
        "S001", "Sala de conferencias", 50000, 20
    )

    # PRUEBA 1: Creación y confirmación exitosa.
    try:

        # Creamos una reserva de dos horas.
        reserva1 = Reserva(
            "R001", cliente, sala, 2, 19, 10
        )

        # Confirmamos la reserva.
        print("\n" + reserva1.confirmar())

        # Mostramos la información de la reserva.
        print(reserva1.mostrar_informacion())

    # Capturamos posibles errores.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"Error controlado: {error}")

    # PRUEBA 2: Intento de reservar un servicio ocupado.
    try:

        # Intentamos reservar la misma sala.
        Reserva("R002", cliente, sala, 3)

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # PRUEBA 3: Procesamiento de la primera reserva.
    try:

        # Procesamos la reserva confirmada.
        print("\n" + reserva1.procesar())

        # Mostramos su nuevo estado.
        print(f"Estado: {reserva1.estado}")

    # Capturamos posibles errores.
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # PRUEBA 4: Creación y cancelación de una reserva.
    try:

        # Creamos una nueva reserva.
        reserva2 = Reserva("R003", cliente, sala, 4)

        # Confirmamos la reserva.
        print("\n" + reserva2.confirmar())

        # Cancelamos la reserva.
        print(reserva2.cancelar())

        # Mostramos el estado actualizado.
        print(f"Estado: {reserva2.estado}")

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"Error controlado: {error}")

    # PRUEBA 5: Intento de cancelar nuevamente.
    try:
        reserva2.cancelar()

    # Capturamos la operación no permitida.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # PRUEBA 6: Reserva con duración negativa.
    try:

        # Intentamos crear una reserva inválida.
        Reserva("R004", cliente, sala, -2)

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # Finalizamos las pruebas del módulo.
    finally:
        print("\nPruebas del módulo Reserva finalizadas.")