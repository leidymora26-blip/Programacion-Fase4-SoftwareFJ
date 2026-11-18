# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo especializado de alquiler de equipos.

# Importamos la clase abstracta Servicio.
from servicio import Servicio

# Importamos las excepciones personalizadas.
from excepciones import DatosInvalidosError, ErrorSistema

# Importamos las funciones de registro de eventos y errores.
from config_logs import registrar_evento, registrar_excepcion


# Definimos la clase AlquilerEquipo que hereda de Servicio.
class AlquilerEquipo(Servicio):

    # Constructor de la clase.
    def __init__(self, identificador, nombre, tarifa_base,
                 cantidad, disponible=True):

        # Invocamos el constructor de la clase padre.
        super().__init__(
            identificador, nombre, tarifa_base, disponible
        )

        # Asignamos la cantidad mediante su propiedad.
        self.cantidad = cantidad

        # Validamos los parámetros del servicio.
        self.validar_parametros()

    # Propiedad para consultar la cantidad de equipos.
    @property
    def cantidad(self):
        return self.__cantidad

    # Método para modificar la cantidad de equipos.
    @cantidad.setter
    def cantidad(self, nueva_cantidad):

        # Validamos que la cantidad sea un entero positivo.
        if (
            isinstance(nueva_cantidad, bool)
            or not isinstance(nueva_cantidad, int)
            or nueva_cantidad <= 0
        ):
            raise DatosInvalidosError(
                "La cantidad de equipos debe ser un entero positivo."
            )

        # Guardamos la cantidad como atributo privado.
        self.__cantidad = nueva_cantidad

    # Sobrescribimos el método de validación de parámetros.
    def validar_parametros(self):

        # Comprobamos que la cantidad sea válida.
        if self.cantidad <= 0:
            raise DatosInvalidosError(
                "La cantidad de equipos no es válida."
            )

    # Sobrescribimos el método para calcular costos.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        # Verificamos la disponibilidad de los equipos.
        self.verificar_disponibilidad()

        # Validamos la duración del alquiler.
        self.validar_duracion(duracion)

        # Validamos los parámetros específicos del servicio.
        self.validar_parametros()

        # Calculamos el costo por horas y cantidad de equipos.
        costo = self.tarifa_base * duracion * self.cantidad

        # Aplicamos los impuestos y descuentos.
        return self.aplicar_ajustes(costo, impuesto, descuento)

    # Sobrescribimos el método para describir el servicio.
    def describir_servicio(self):

        # Retornamos la descripción del equipo.
        return (
            f"Alquiler de equipos: {self.nombre}. "
            f"Cantidad: {self.cantidad} unidades."
        )

    # Sobrescribimos el método para mostrar información.
    def mostrar_informacion(self):

        # Obtenemos la información de la clase padre.
        informacion = super().mostrar_informacion()

        # Agregamos la información específica del equipo.
        return (
            f"{informacion}\n"
            f"Tipo: Alquiler de equipos\n"
            f"Cantidad: {self.cantidad} unidades"
        )


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Mostramos el encabezado de las pruebas.
    print("=== PRUEBAS DEL MÓDULO ALQUILER EQUIPO ===")

    # PRUEBA 1: Creación de un servicio válido.
    try:

        # Creamos un servicio de alquiler de tres computadores.
        equipo = AlquilerEquipo(
            "S004",
            "Computadores portátiles",
            25000,
            3
        )

        # Mostramos la información del servicio.
        print("\nServicio creado correctamente.")
        print(equipo.mostrar_informacion())

        # Calculamos el costo básico por dos horas.
        print(
            f"\nCosto básico: "
            f"${equipo.calcular_costo(2):,.2f}"
        )

        # Calculamos el costo con impuesto del 19%.
        print(
            f"Costo con impuesto: "
            f"${equipo.calcular_costo(2, 19):,.2f}"
        )

        # Calculamos el costo con impuesto y descuento.
        print(
            f"Costo con impuesto y descuento: "
            f"${equipo.calcular_costo(2, 19, 10):,.2f}"
        )

    # Capturamos posibles errores del sistema.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"Error controlado: {error}")

    # Registramos la operación si fue exitosa.
    else:
        registrar_evento("Prueba de alquiler de equipos exitosa.")

    # PRUEBA 2: Creación de un servicio con cantidad inválida.
    try:

        # Intentamos registrar una cantidad negativa.
        equipo_invalido = AlquilerEquipo(
            "S005", "Proyectores", 30000, -2
        )

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # PRUEBA 3: Alquiler de equipos no disponibles.
    try:

        # Creamos un servicio que no se encuentra disponible.
        equipo_ocupado = AlquilerEquipo(
            "S006", "Tabletas", 20000, 5, False
        )

        # Intentamos calcular el costo del alquiler.
        equipo_ocupado.calcular_costo(2)

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # PRUEBA 4: Cálculo con un impuesto inválido.
    try:

        # Creamos un equipo válido para esta prueba.
        equipo_prueba = AlquilerEquipo(
            "S007", "Monitor", 15000, 1
        )

        # Intentamos aplicar un impuesto superior al 100%.
        equipo_prueba.calcular_costo(2, 150)

    # Capturamos la excepción generada por el cálculo.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # Finalizamos las pruebas del módulo.
    finally:
        print("\nPruebas del módulo AlquilerEquipo finalizadas.")
