# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de asesorías especializadas.

# Importamos la clase abstracta Servicio.
from servicio import Servicio

# Importamos las excepciones personalizadas.
from excepciones import DatosInvalidosError, ErrorSistema

# Importamos las funciones de registro de eventos y errores.
from config_logs import registrar_evento, registrar_excepcion


# Definimos la clase AsesoriaEspecializada.
class AsesoriaEspecializada(Servicio):

    # Constructor de la clase.
    def __init__(self, identificador, nombre, tarifa_base,
                 especialidad, asesor, disponible=True):

        # Invocamos el constructor de la clase padre.
        super().__init__(
            identificador, nombre, tarifa_base, disponible
        )

        # Asignamos la especialidad mediante su propiedad.
        self.especialidad = especialidad

        # Asignamos el asesor mediante su propiedad.
        self.asesor = asesor

        # Validamos los parámetros del servicio.
        self.validar_parametros()

    # Propiedad para consultar la especialidad.
    @property
    def especialidad(self):
        return self.__especialidad

    # Método para modificar y validar la especialidad.
    @especialidad.setter
    def especialidad(self, nueva_especialidad):

        # Validamos que la especialidad no esté vacía.
        if (
            not isinstance(nueva_especialidad, str)
            or not nueva_especialidad.strip()
        ):
            raise DatosInvalidosError(
                "La especialidad no puede estar vacía."
            )

        # Guardamos la especialidad como atributo privado.
        self.__especialidad = nueva_especialidad.strip()

    # Propiedad para consultar el nombre del asesor.
    @property
    def asesor(self):
        return self.__asesor

    # Método para modificar y validar el asesor.
    @asesor.setter
    def asesor(self, nuevo_asesor):

        # Validamos que el nombre del asesor sea válido.
        if (
            not isinstance(nuevo_asesor, str)
            or not nuevo_asesor.strip()
        ):
            raise DatosInvalidosError(
                "El nombre del asesor no puede estar vacío."
            )

        # Guardamos el nombre como atributo privado.
        self.__asesor = nuevo_asesor.strip()

    # Sobrescribimos el método de validación de parámetros.
    def validar_parametros(self):

        # Verificamos que exista una especialidad.
        if not self.especialidad:
            raise DatosInvalidosError(
                "La especialidad no es válida."
            )

        # Verificamos que exista un asesor asignado.
        if not self.asesor:
            raise DatosInvalidosError(
                "Debe asignarse un asesor."
            )

    # Sobrescribimos el método para calcular costos.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        # Verificamos la disponibilidad del servicio.
        self.verificar_disponibilidad()

        # Validamos la duración de la asesoría.
        self.validar_duracion(duracion)

        # Validamos los parámetros específicos.
        self.validar_parametros()

        # Calculamos el costo según las horas contratadas.
        costo = self.tarifa_base * duracion

        # Aplicamos los impuestos y descuentos.
        return self.aplicar_ajustes(costo, impuesto, descuento)

    # Sobrescribimos el método para describir el servicio.
    def describir_servicio(self):

        # Retornamos una descripción de la asesoría.
        return (
            f"Asesoría especializada: {self.nombre}. "
            f"Especialidad: {self.especialidad}. "
            f"Asesor: {self.asesor}."
        )

    # Sobrescribimos el método para mostrar información.
    def mostrar_informacion(self):

        # Obtenemos la información de la clase padre.
        informacion = super().mostrar_informacion()

        # Agregamos la información específica de la asesoría.
        return (
            f"{informacion}\n"
            f"Tipo: Asesoría especializada\n"
            f"Especialidad: {self.especialidad}\n"
            f"Asesor: {self.asesor}"
        )


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Mostramos el encabezado de las pruebas.
    print("=== PRUEBAS DEL MÓDULO ASESORÍA ===")

    # PRUEBA 1: Creación de una asesoría válida.
    try:

        # Creamos un servicio de asesoría especializada.
        asesoria = AsesoriaEspecializada(
            "S008",
            "Consultoría tecnológica",
            80000,
            "Desarrollo de software",
            "Andrés Martínez"
        )

        # Mostramos la información del servicio.
        print("\nAsesoría creada correctamente.")
        print(asesoria.mostrar_informacion())

        # Calculamos el costo básico por tres horas.
        print(
            f"\nCosto básico: "
            f"${asesoria.calcular_costo(3):,.2f}"
        )

        # Calculamos el costo con impuesto del 19%.
        print(
            f"Costo con impuesto: "
            f"${asesoria.calcular_costo(3, 19):,.2f}"
        )

        # Calculamos el costo con impuesto y descuento.
        print(
            f"Costo con impuesto y descuento: "
            f"${asesoria.calcular_costo(3, 19, 10):,.2f}"
        )

    # Capturamos posibles errores.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"Error controlado: {error}")

    # Registramos la operación exitosa.
    else:
        registrar_evento("Prueba de asesoría exitosa.")

    # PRUEBA 2: Asesoría sin especialidad.
    try:

        # Intentamos crear una asesoría inválida.
        AsesoriaEspecializada(
            "S009",
            "Consultoría",
            60000,
            "",
            "Carlos Pérez"
        )

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # PRUEBA 3: Asesoría sin asesor asignado.
    try:

        # Intentamos registrar una asesoría sin asesor.
        AsesoriaEspecializada(
            "S010",
            "Consultoría informática",
            70000,
            "Informática",
            ""
        )

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # PRUEBA 4: Asesoría no disponible.
    try:

        # Creamos una asesoría que no está disponible.
        asesoria_ocupada = AsesoriaEspecializada(
            "S011",
            "Consultoría de seguridad",
            90000,
            "Ciberseguridad",
            "Laura Gómez",
            False
        )

        # Intentamos calcular el costo de la asesoría.
        asesoria_ocupada.calcular_costo(2)

    # Capturamos y registramos el error.
    except ErrorSistema as error:
        registrar_excepcion(str(error))
        print(f"\nError controlado: {error}")

    # Finalizamos las pruebas del módulo.
    finally:
        print("\nPruebas del módulo AsesoriaEspecializada finalizadas.")
