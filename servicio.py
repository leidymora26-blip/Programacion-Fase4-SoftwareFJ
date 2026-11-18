# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de la clase abstracta Servicio.

# Importamos el decorador para métodos abstractos.
from abc import abstractmethod

# Importamos la biblioteca para validar valores numéricos.
import math

# Importamos la clase padre.
from entidad import Entidad

# Importamos las excepciones personalizadas.
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoCostoError
)

# Importamos las funciones para el registro de eventos.
from config_logs import registrar_excepcion


# Definimos la clase abstracta Servicio.
class Servicio(Entidad):

    # Constructor de la clase.
    def __init__(self, identificador, nombre, tarifa_base,
                 disponible=True):

        # Invocamos el constructor de la clase padre.
        super().__init__(identificador, nombre)

        # Asignamos la tarifa mediante su propiedad.
        self.tarifa_base = tarifa_base

        # Asignamos el estado de disponibilidad.
        self.disponible = disponible

    # Propiedad para consultar la tarifa base.
    @property
    def tarifa_base(self):
        return self.__tarifa_base

    # Método para modificar y validar la tarifa.
    @tarifa_base.setter
    def tarifa_base(self, nueva_tarifa):

        # Validamos que la tarifa sea numérica y positiva.
        if (
            isinstance(nueva_tarifa, bool)
            or not isinstance(nueva_tarifa, (int, float))
            or not math.isfinite(nueva_tarifa)
            or nueva_tarifa <= 0
        ):
            raise DatosInvalidosError(
                "La tarifa base debe ser un número positivo."
            )

        # Guardamos la tarifa como atributo privado.
        self.__tarifa_base = nueva_tarifa

    # Propiedad para consultar la disponibilidad.
    @property
    def disponible(self):
        return self.__disponible

    # Método para modificar la disponibilidad.
    @disponible.setter
    def disponible(self, nuevo_estado):

        # Validamos que el estado sea booleano.
        if not isinstance(nuevo_estado, bool):
            raise DatosInvalidosError(
                "La disponibilidad debe ser True o False."
            )

        # Actualizamos el atributo privado.
        self.__disponible = nuevo_estado

    # Método para verificar si el servicio está disponible.
    def verificar_disponibilidad(self):

        # Generamos una excepción si no está disponible.
        if not self.disponible:
            raise ServicioNoDisponibleError(
                "El servicio no se encuentra disponible."
            )

    # Método para validar la duración del servicio.
    def validar_duracion(self, duracion):

        # Comprobamos que la duración sea positiva.
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):
            raise DatosInvalidosError(
                "La duración debe ser mayor que cero."
            )

    # Método para aplicar impuestos y descuentos.
    def aplicar_ajustes(self, costo, impuesto=0, descuento=0):

        # Intentamos validar y calcular el costo final.
        try:

            # Validamos los valores recibidos.
            for valor in (costo, impuesto, descuento):
                if (
                    isinstance(valor, bool)
                    or not isinstance(valor, (int, float))
                    or not math.isfinite(valor)
                ):
                    raise ValueError("Valor numérico inválido.")

            # Validamos que el costo no sea negativo.
            if costo < 0:
                raise ValueError("El costo no puede ser negativo.")

            # Validamos el porcentaje de impuesto.
            if not 0 <= impuesto <= 100:
                raise ValueError("Impuesto fuera del rango permitido.")

            # Validamos el porcentaje de descuento.
            if not 0 <= descuento <= 100:
                raise ValueError("Descuento fuera del rango permitido.")

            # Aplicamos el descuento al costo.
            subtotal = costo * (1 - descuento / 100)

            # Aplicamos el impuesto al subtotal.
            total = subtotal * (1 + impuesto / 100)

            # Validamos que el resultado sea consistente.
            if not math.isfinite(total):
                raise ValueError("El costo final no es válido.")

            # Retornamos el costo final redondeado.
            return round(total, 2)

        # Capturamos los errores del cálculo.
        except (ValueError, TypeError, OverflowError) as error:

            # Aplicamos encadenamiento de excepciones.
            raise CalculoCostoError(
                f"Error al calcular el costo: {error}"
            ) from error

    # Método abstracto para calcular el costo.
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    # Método abstracto para describir el servicio.
    @abstractmethod
    def describir_servicio(self):
        pass

    # Método abstracto para validar parámetros específicos.
    @abstractmethod
    def validar_parametros(self):
        pass

    # Sobrescribimos el método heredado de Entidad.
    def mostrar_informacion(self):

        # Determinamos el texto de disponibilidad.
        estado = "Disponible" if self.disponible else "No disponible"

        # Retornamos la información general del servicio.
        return (
            f"Código: {self.identificador}\n"
            f"Servicio: {self.nombre}\n"
            f"Tarifa base: ${self.tarifa_base:,.2f}\n"
            f"Estado: {estado}"
        )


# Verificamos si el módulo se ejecuta directamente.
if __name__ == "__main__":

    # Mostramos el encabezado de las pruebas.
    print("=== PRUEBAS DEL MÓDULO SERVICIO ===")

    # Intentamos instanciar la clase abstracta.
    try:
        servicio = Servicio("S001", "Servicio de prueba", 50000)

    # Capturamos el error generado por Python.
    except TypeError:
        registrar_excepcion(
            "Intento de instanciar la clase abstracta Servicio."
        )
        print("Validación de abstracción exitosa.")
        print("No se puede instanciar la clase Servicio directamente.")

    # Finalizamos la prueba.
    finally:
        print("Pruebas del módulo Servicio finalizadas.")
