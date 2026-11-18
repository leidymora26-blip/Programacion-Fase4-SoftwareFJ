# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de pruebas integrales del sistema.

# Importamos la clase administradora.
from sistema import SistemaSoftwareFJ

# Importamos los servicios especializados.
from reserva_sala import ReservaSala
from alquiler_equipo import AlquilerEquipo
from asesoria import AsesoriaEspecializada

# Importamos las excepciones personalizadas.
from excepciones import (
    DatosInvalidosError,
    ClienteDuplicadoError,
    ServicioDuplicadoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    ClienteNoEncontradoError
)

# Importamos las funciones de registro.
from config_logs import registrar_evento, registrar_excepcion


# Definimos la función para ejecutar las pruebas.
def ejecutar_pruebas():

    # Creamos una instancia independiente del sistema.
    sistema = SistemaSoftwareFJ()

    # Inicializamos los contadores de resultados.
    exitosas = 0
    errores_controlados = 0
    fallidas = 0

    # Definimos una función auxiliar para cada operación.
    def ejecutar(numero, descripcion, operacion,
                 error_esperado=None):

        # Permitimos modificar los contadores externos.
        nonlocal exitosas, errores_controlados, fallidas

        # Mostramos el número y la descripción.
        print(f"\nPRUEBA {numero}: {descripcion}")

        # Intentamos ejecutar la operación.
        try:

            # Ejecutamos la función recibida.
            operacion()

        # Capturamos las excepciones generadas.
        except Exception as error:

            # Registramos el error en el archivo de logs.
            registrar_excepcion(
                f"Prueba {numero}: {error}"
            )

            # Verificamos si el error era esperado.
            if (
                error_esperado is not None
                and isinstance(error, error_esperado)
            ):

                # Incrementamos los errores controlados.
                errores_controlados += 1

                # Mostramos el resultado esperado.
                print(f"ERROR CONTROLADO: {error}")

            else:

                # Incrementamos las pruebas fallidas.
                fallidas += 1

                # Informamos el error inesperado.
                print(f"PRUEBA FALLIDA: {error}")

        # Ejecutamos este bloque si no hubo excepciones.
        else:

            # Verificamos si esperábamos un error.
            if error_esperado is not None:

                # Registramos una prueba fallida.
                fallidas += 1

                # Informamos que faltó una validación.
                print("PRUEBA FALLIDA: Se esperaba un error.")

                # Registramos el fallo.
                registrar_evento(
                    f"Prueba {numero}: Faltó una validación."
                )

            else:

                # Incrementamos las operaciones exitosas.
                exitosas += 1

                # Mostramos el resultado.
                print("OPERACIÓN EXITOSA")

                # Registramos la operación.
                registrar_evento(
                    f"Prueba {numero} ejecutada correctamente."
                )

        # Finalizamos cada prueba.
        finally:
            print("-" * 55)

    # Mostramos el encabezado principal.
    print("=" * 55)
    print("SOFTWARE FJ - PRUEBAS INTEGRALES")
    print("=" * 55)

    # PRUEBA 1: Registro de un cliente válido.
    ejecutar(
        1,
        "Registro de cliente Ana Rodríguez",
        lambda: sistema.registrar_cliente(
            "1001234567",
            "Ana Rodríguez",
            "ana@example.com",
            "3001234567"
        )
    )

    # PRUEBA 2: Registro de un segundo cliente.
    ejecutar(
        2,
        "Registro de cliente Carlos Pérez",
        lambda: sistema.registrar_cliente(
            "1001234568",
            "Carlos Pérez",
            "carlos@example.com",
            "3101234567"
        )
    )

    # PRUEBA 3: Registro de un cliente duplicado.
    ejecutar(
        3,
        "Registro de cliente duplicado",
        lambda: sistema.registrar_cliente(
            "1001234567",
            "Ana Rodríguez",
            "ana@example.com",
            "3001234567"
        ),
        ClienteDuplicadoError
    )

    # PRUEBA 4: Registro con correo incorrecto.
    ejecutar(
        4,
        "Cliente con correo inválido",
        lambda: sistema.registrar_cliente(
            "1001234569",
            "Laura Gómez",
            "correo_invalido",
            "3201234567"
        ),
        DatosInvalidosError
    )

    # PRUEBA 5: Registro con teléfono incorrecto.
    ejecutar(
        5,
        "Cliente con teléfono inválido",
        lambda: sistema.registrar_cliente(
            "1001234570",
            "María López",
            "maria@example.com",
            "12345"
        ),
        DatosInvalidosError
    )

    # PRUEBA 6: Registro de una sala válida.
    ejecutar(
        6,
        "Registro de sala de conferencias",
        lambda: sistema.registrar_servicio(
            ReservaSala(
                "S001",
                "Sala de conferencias",
                50000,
                20
            )
        )
    )

    # PRUEBA 7: Registro de equipos tecnológicos.
    ejecutar(
        7,
        "Registro de alquiler de equipos",
        lambda: sistema.registrar_servicio(
            AlquilerEquipo(
                "S002",
                "Computadores portátiles",
                25000,
                3
            )
        )
    )

    # PRUEBA 8: Registro de una asesoría.
    ejecutar(
        8,
        "Registro de asesoría especializada",
        lambda: sistema.registrar_servicio(
            AsesoriaEspecializada(
                "S003",
                "Consultoría tecnológica",
                80000,
                "Desarrollo de software",
                "Andrés Martínez"
            )
        )
    )

    # PRUEBA 9: Sala con capacidad incorrecta.
    ejecutar(
        9,
        "Registro de sala con capacidad negativa",
        lambda: sistema.registrar_servicio(
            ReservaSala(
                "S004",
                "Sala pequeña",
                30000,
                -5
            )
        ),
        DatosInvalidosError
    )

    # PRUEBA 10: Registro de un servicio duplicado.
    ejecutar(
        10,
        "Registro de servicio duplicado",
        lambda: sistema.registrar_servicio(
            ReservaSala(
                "S001",
                "Sala duplicada",
                50000,
                20
            )
        ),
        ServicioDuplicadoError
    )

    # PRUEBA 11: Creación de una reserva válida.
    ejecutar(
        11,
        "Creación de reserva de sala",
        lambda: sistema.crear_reserva(
            "R001",
            "1001234567",
            "S001",
            2,
            19,
            10
        )
    )

    # PRUEBA 12: Confirmación de la reserva.
    ejecutar(
        12,
        "Confirmación de reserva R001",
        lambda: sistema.confirmar_reserva("R001")
    )

    # PRUEBA 13: Reserva de un servicio ocupado.
    ejecutar(
        13,
        "Intento de reservar una sala ocupada",
        lambda: sistema.crear_reserva(
            "R002",
            "1001234568",
            "S001",
            3
        ),
        ServicioNoDisponibleError
    )

    # PRUEBA 14: Procesamiento de la reserva.
    ejecutar(
        14,
        "Procesamiento de reserva R001",
        lambda: sistema.procesar_reserva("R001")
    )

    # PRUEBA 15: Reserva de equipos.
    ejecutar(
        15,
        "Creación de reserva de equipos",
        lambda: sistema.crear_reserva(
            "R003",
            "1001234568",
            "S002",
            2
        )
    )

    # PRUEBA 16: Confirmación del alquiler.
    ejecutar(
        16,
        "Confirmación de reserva R003",
        lambda: sistema.confirmar_reserva("R003")
    )

    # PRUEBA 17: Cancelación de una reserva.
    ejecutar(
        17,
        "Cancelación de reserva R003",
        lambda: sistema.cancelar_reserva("R003")
    )

    # PRUEBA 18: Intento de cancelar nuevamente.
    ejecutar(
        18,
        "Intento de doble cancelación",
        lambda: sistema.cancelar_reserva("R003"),
        OperacionNoPermitidaError
    )

    # PRUEBA 19: Reserva con duración negativa.
    ejecutar(
        19,
        "Reserva con duración negativa",
        lambda: sistema.crear_reserva(
            "R004",
            "1001234567",
            "S003",
            -2
        ),
        DatosInvalidosError
    )

    # PRUEBA 20: Reserva con cliente inexistente.
    ejecutar(
        20,
        "Reserva con cliente inexistente",
        lambda: sistema.crear_reserva(
            "R005",
            "9999999999",
            "S003",
            2
        ),
        ClienteNoEncontradoError
    )

    # Calculamos el total de operaciones ejecutadas.
    total = exitosas + errores_controlados + fallidas

    # Calculamos el porcentaje de pruebas superadas.
    porcentaje = (
        (exitosas + errores_controlados) / total
    ) * 100

    # Mostramos el resumen de las pruebas.
    print("\n" + "=" * 55)
    print("RESUMEN FINAL DE PRUEBAS")
    print("=" * 55)

    # Mostramos los contadores.
    print(f"Total de operaciones: {total}")
    print(f"Operaciones exitosas: {exitosas}")
    print(f"Errores controlados: {errores_controlados}")
    print(f"Pruebas fallidas: {fallidas}")
    print(f"Porcentaje de cumplimiento: {porcentaje:.2f}%")

    # Mostramos las estadísticas del sistema.
    print("\n=== ESTADO FINAL DEL SISTEMA ===")

    # Recorremos el diccionario de estadísticas.
    for clave, valor in sistema.resumen().items():
        print(f"{clave.capitalize()}: {valor}")

    # Registramos la finalización de las pruebas.
    registrar_evento(
        f"Pruebas integrales finalizadas. "
        f"Cumplimiento: {porcentaje:.2f}%"
    )

    # Informamos que el programa continúa funcionando.
    print("\nSimulación finalizada correctamente.")
    print("El sistema continúa funcionando.")

    # Retornamos los resultados para futuras consultas.
    return {
        "total": total,
        "exitosas": exitosas,
        "errores_controlados": errores_controlados,
        "fallidas": fallidas,
        "porcentaje": porcentaje
    }


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Ejecutamos las pruebas integrales.
    ejecutar_pruebas()
