# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo especializado de reserva de salas.

# Importamos la clase abstracta Servicio.
from servicio import Servicio

# Importamos las excepciones personalizadas.
from excepciones import DatosInvalidosError, ErrorSistema

# Importamos las funciones para registrar eventos y errores.
from config_logs import registrar_evento, registrar_excepcion


# Definimos la clase ReservaSala que hereda de Servicio.
class ReservaSala(Servicio):

    # Constructor de la clase.
    def __init__(self, identificador, nombre, tarifa_base,
                 capacidad, disponible=True):

        # Invocamos el constructor de la clase padre.
        super().__init__(
            identificador, nombre, tarifa_base, disponible
        )

        # Asignamos la capacidad mediante su propiedad.
        self.capacidad = capacidad

        # Validamos los parámetros del servicio.
        self.validar_parametros()

    # Propiedad para consultar la capacidad de la sala.
    @property
    def capacidad(self):
        return self.__capacidad

    # Método para modificar la capacidad.
    @capacidad.setter
    def capacidad(self, nueva_capacidad):

        # Validamos que la capacidad sea un entero positivo.
        if (
            isinstance(nueva_capacidad, bool)
            or not isinstance(nueva_capacidad, int)
            or nueva_capacidad <= 0
        ):
            raise DatosInvalidosError(
                "La capacidad debe ser un número entero positivo."
            )

        # Guardamos la capacidad como atributo privado.
        self.__capacidad = nueva_capacidad

    # Sobrescribimos el método de validación de parámetros.
    def validar_parametros(self):

        # Verificamos que la capacidad sea válida.
        if self.capacidad <= 0:
            raise DatosInvalidosError(
                "La capacidad de la sala no es válida."
            )

    # Sobrescribimos el método para calcular costos.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        # Verificamos la disponibilidad de la sala.
        self.verificar_disponibilidad()

        # Validamos la duración de la reserva.
        self.validar_duracion(duracion)

        # Validamos los parámetros específicos del servicio.
        self.validar_parametros()

        # Calculamos el costo base según las horas reservadas.
        costo = self.tarifa_base * duracion

        # Aplicamos los impuestos y descuentos correspondientes.
        return self.aplicar_ajustes(costo, impuesto, descuento)

    # Sobrescribimos el método para describir el servicio.
    def describir_servicio(self):

        # Retornamos una descripción de la sala.
        return (
            f"Reserva de sala: {self.nombre}. "
            f"Capacidad máxima: {self.capacidad} personas."
        )

    # Sobrescribimos el método para mostrar información.
    def mostrar_informacion(self):

        # Obtenemos la información de la clase padre.
        informacion = super().mostrar_informacion()

        # Agregamos la información específica de la sala.
        return (
            f"{informacion}\n"
            f"Tipo: Reserva de sala\n"
            f"Capacidad: {self.capacidad} personas"
        )


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Mostramos el encabezado de las pruebas.
    print("=== PRUEBAS DEL MÓDULO RESERVA SALA ===")

    # PRUEBA 1: Creación de una sala válida.
    try:

        # Creamos una sala con capacidad para 20 personas.
        sala = ReservaSala(
            "S001",
            "Sala de conferencias",
            50000,
            20
        )

        # Mostramos la información de la sala.
        print("\nSala creada correctamente.")
        print(sala.mostrar_informacion())

        # Calculamos el costo de dos horas.
        print(f"\nCosto básico: ${sala.calcular_costo(2):,.2f}")

        # Calculamos el costo con impuesto del 19%.
        print(
            f"Costo con impuesto: "
            f"${sala.calcular_costo(2, 19):,.2f}"
        )

        # Calculamos el costo con impuesto y descuento.
        print(
            f"Costo con impuesto y descuento: "
            f"${sala.calcular_costo(2, 19, 10):,.2f}"
        )

    # Capturamos posibles errores.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"Error controlado: {error}")

    # Registramos la operación exitosa.
    else:
        registrar_evento("Prueba de reserva de sala exitosa.")

    # PRUEBA 2: Creación de una sala con capacidad inválida.
    try:
        sala_invalida = ReservaSala(
            "S002", "Sala pequeña", 30000, -5
        )

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # PRUEBA 3: Reserva de una sala no disponible.
    try:

        # Creamos una sala que no está disponible.
        sala_ocupada = ReservaSala(
            "S003", "Sala de reuniones", 40000, 10, False
        )

        # Intentamos calcular el costo de la reserva.
        sala_ocupada.calcular_costo(2)

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # Finalizamos las pruebas.
    finally:
        print("\nPruebas del módulo ReservaSala finalizadas.")
