# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de administración integral del sistema.

# Importamos las clases desarrolladas anteriormente.
from cliente import Cliente
from servicio import Servicio
from reserva import Reserva
from functools import wraps

# Importamos las excepciones personalizadas.
from excepciones import (
    ErrorSistema,
    DatosInvalidosError,
    ClienteDuplicadoError,
    ServicioDuplicadoError,
    ClienteNoEncontradoError,
    ServicioNoEncontradoError,
    ReservaNoEncontradaError,
    ReservaInvalidaError
)

# Importamos las funciones de registro.
from config_logs import registrar_evento, registrar_excepcion


# Decorador para registrar errores de las operaciones.
def controlar_errores(funcion):

    # Conservamos la información de la función original.
    @wraps(funcion)
    def ejecutar(*args, **kwargs):

        # Intentamos ejecutar la operación solicitada.
        try:
            return funcion(*args, **kwargs)

        # Capturamos las excepciones personalizadas.
        except ErrorSistema as error:
            registrar_excepcion(f"{funcion.__name__}: {error}")
            raise

        # Capturamos errores inesperados.
        except Exception as error:
            registrar_excepcion(
                f"Error inesperado en {funcion.__name__}: {error}"
            )

            # Encadenamos la excepción original.
            raise ErrorSistema(
                "No fue posible completar la operación."
            ) from error

    # Retornamos la función protegida.
    return ejecutar


# Definimos la clase administradora del sistema.
class SistemaSoftwareFJ:

    # Constructor de la clase.
    def __init__(self):

        # Creamos las listas privadas.
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        # Registramos el inicio del sistema.
        registrar_evento("Sistema Software FJ iniciado.")

    # Propiedad para consultar la lista de clientes.
    @property
    def clientes(self):
        return self.__clientes.copy()

    # Propiedad para consultar la lista de servicios.
    @property
    def servicios(self):
        return self.__servicios.copy()

    # Propiedad para consultar la lista de reservas.
    @property
    def reservas(self):
        return self.__reservas.copy()

    # Método para registrar un nuevo cliente.
    @controlar_errores
    def registrar_cliente(self, identificador, nombre,
                          correo, telefono):

        # Creamos y validamos el objeto Cliente.
        cliente = Cliente(
            identificador, nombre, correo, telefono
        )

        # Verificamos que el cliente no esté duplicado.
        for existente in self.__clientes:
            if existente.identificador == cliente.identificador:
                raise ClienteDuplicadoError(
                    "El cliente ya se encuentra registrado."
                )

        # Agregamos el cliente a la lista.
        self.__clientes.append(cliente)

        # Registramos la operación exitosa.
        registrar_evento("Cliente registrado correctamente.")

        # Retornamos el objeto creado.
        return cliente

    # Método para buscar un cliente por identificación.
    @controlar_errores
    def buscar_cliente(self, identificador):

        # Recorremos la lista de clientes.
        for cliente in self.__clientes:

            # Verificamos si coincide la identificación.
            if cliente.identificador == identificador:
                return cliente

        # Generamos una excepción si no existe.
        raise ClienteNoEncontradoError(
            "El cliente no se encuentra registrado."
        )

    # Método para registrar un servicio.
    @controlar_errores
    def registrar_servicio(self, servicio):

        # Validamos que sea un objeto de tipo Servicio.
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError(
                "Debe ingresar un servicio válido."
            )

        # Validamos sus parámetros específicos.
        servicio.validar_parametros()

        # Verificamos que el servicio no esté duplicado.
        for existente in self.__servicios:
            if existente.identificador == servicio.identificador:
                raise ServicioDuplicadoError(
                    "El servicio ya se encuentra registrado."
                )

        # Agregamos el servicio a la lista.
        self.__servicios.append(servicio)

        # Registramos la operación exitosa.
        registrar_evento(
            f"Servicio {servicio.identificador} registrado."
        )

        # Retornamos el servicio registrado.
        return servicio

    # Método para buscar un servicio.
    @controlar_errores
    def buscar_servicio(self, identificador):

        # Recorremos la lista de servicios.
        for servicio in self.__servicios:

            # Verificamos si coincide el código.
            if servicio.identificador == identificador:
                return servicio

        # Generamos una excepción si no existe.
        raise ServicioNoEncontradoError(
            "El servicio no se encuentra registrado."
        )

    # Método para crear una reserva.
    @controlar_errores
    def crear_reserva(self, identificador, id_cliente,
                      id_servicio, duracion,
                      impuesto=0, descuento=0):

        # Validamos el código de la reserva.
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError(
                "El código de la reserva no puede estar vacío."
            )

        # Eliminamos espacios innecesarios.
        identificador = identificador.strip()

        # Verificamos que la reserva no esté duplicada.
        for existente in self.__reservas:
            if existente.identificador == identificador:
                raise ReservaInvalidaError(
                    "El código de la reserva ya existe."
                )

        # Buscamos el cliente registrado.
        cliente = self.buscar_cliente(id_cliente)

        # Buscamos el servicio registrado.
        servicio = self.buscar_servicio(id_servicio)

        # Creamos el objeto Reserva.
        reserva = Reserva(
            identificador,
            cliente,
            servicio,
            duracion,
            impuesto,
            descuento
        )

        # Agregamos la reserva a la lista.
        self.__reservas.append(reserva)

        # Registramos la creación de la reserva.
        registrar_evento(
            f"Reserva {identificador} creada correctamente."
        )

        # Retornamos la reserva creada.
        return reserva

    # Método para buscar una reserva.
    @controlar_errores
    def buscar_reserva(self, identificador):

        # Recorremos la lista de reservas.
        for reserva in self.__reservas:

            # Verificamos si coincide el código.
            if reserva.identificador == identificador:
                return reserva

        # Generamos una excepción si no existe.
        raise ReservaNoEncontradaError(
            "La reserva no se encuentra registrada."
        )

    # Método para confirmar una reserva.
    @controlar_errores
    def confirmar_reserva(self, identificador):

        # Buscamos la reserva correspondiente.
        reserva = self.buscar_reserva(identificador)

        # Confirmamos la reserva.
        return reserva.confirmar()

    # Método para cancelar una reserva.
    @controlar_errores
    def cancelar_reserva(self, identificador):

        # Buscamos la reserva correspondiente.
        reserva = self.buscar_reserva(identificador)

        # Cancelamos la reserva.
        return reserva.cancelar()

    # Método para procesar una reserva.
    @controlar_errores
    def procesar_reserva(self, identificador):

        # Buscamos la reserva correspondiente.
        reserva = self.buscar_reserva(identificador)

        # Procesamos la reserva.
        return reserva.procesar()

    # Método para listar los clientes registrados.
    def listar_clientes(self):

        # Retornamos la información de los clientes.
        return [
            cliente.mostrar_informacion()
            for cliente in self.__clientes
        ]

    # Método para listar los servicios registrados.
    def listar_servicios(self):

        # Retornamos la información de los servicios.
        return [
            servicio.mostrar_informacion()
            for servicio in self.__servicios
        ]

    # Método para listar las reservas registradas.
    def listar_reservas(self):

        # Retornamos la información de las reservas.
        return [
            reserva.mostrar_informacion()
            for reserva in self.__reservas
        ]

    # Método para generar un resumen del sistema.
    def resumen(self):

        # Contamos las reservas confirmadas.
        confirmadas = sum(
            r.estado == "Confirmada"
            for r in self.__reservas
        )

        # Contamos las reservas canceladas.
        canceladas = sum(
            r.estado == "Cancelada"
            for r in self.__reservas
        )

        # Contamos las reservas pendientes.
        pendientes = sum(
            r.estado == "Pendiente"
            for r in self.__reservas
        )

        # Contamos las reservas procesadas.
        procesadas = sum(
            r.estado == "Procesada"
            for r in self.__reservas
        )

        # Calculamos los ingresos de reservas procesadas.
        ingresos = sum(
            r.costo for r in self.__reservas
            if r.estado == "Procesada"
        )

        # Retornamos las estadísticas del sistema.
        return {
            "clientes": len(self.__clientes),
            "servicios": len(self.__servicios),
            "reservas": len(self.__reservas),
            "confirmadas": confirmadas,
            "canceladas": canceladas,
            "pendientes": pendientes,
            "procesadas": procesadas,
            "ingresos": round(ingresos, 2)
        }


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Importamos los tres servicios especializados.
    from reserva_sala import ReservaSala
    from alquiler_equipo import AlquilerEquipo
    from asesoria import AsesoriaEspecializada

    # Mostramos el encabezado de las pruebas.
    print("=== PRUEBAS DEL SISTEMA SOFTWARE FJ ===")

    # Creamos una instancia del sistema.
    sistema = SistemaSoftwareFJ()

    # PRUEBA 1: Integración de clientes y servicios.
    try:

        # Registramos un cliente.
        sistema.registrar_cliente(
            "1001234567",
            "Ana Rodríguez",
            "ana@example.com",
            "3001234567"
        )

        # Registramos una sala.
        sistema.registrar_servicio(
            ReservaSala(
                "S001", "Sala de conferencias", 50000, 20
            )
        )

        # Registramos un alquiler de equipos.
        sistema.registrar_servicio(
            AlquilerEquipo(
                "S002", "Computadores portátiles", 25000, 3
            )
        )

        # Registramos una asesoría especializada.
        sistema.registrar_servicio(
            AsesoriaEspecializada(
                "S003",
                "Consultoría tecnológica",
                80000,
                "Software",
                "Andrés Martínez"
            )
        )

        # Creamos una reserva de sala por dos horas.
        reserva = sistema.crear_reserva(
            "R001",
            "1001234567",
            "S001",
            2,
            19,
            10
        )

        # Confirmamos la reserva.
        print(sistema.confirmar_reserva("R001"))

        # Procesamos la reserva.
        print(sistema.procesar_reserva("R001"))

        # Mostramos la información de la reserva.
        print("\n" + reserva.mostrar_informacion())

    # Capturamos posibles errores.
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # PRUEBA 2: Registro de un cliente duplicado.
    try:
        sistema.registrar_cliente(
            "1001234567",
            "Ana Rodríguez",
            "ana@example.com",
            "3001234567"
        )

    # Capturamos el error.
    except ErrorSistema as error:
        print(f"\nError controlado: {error}")

    # PRUEBA 3: Búsqueda de un servicio inexistente.
    try:
        sistema.buscar_servicio("S999")

    # Capturamos el error.
    except ErrorSistema as error:
        print(f"\nError controlado: {error}")

    # Mostramos el resumen general.
    print("\n=== RESUMEN DEL SISTEMA ===")

    # Recorremos las estadísticas generadas.
    for clave, valor in sistema.resumen().items():
        print(f"{clave.capitalize()}: {valor}")

    # Informamos que las pruebas terminaron.
    print("\nPruebas del sistema finalizadas.")
