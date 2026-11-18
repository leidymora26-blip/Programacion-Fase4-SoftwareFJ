# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de excepciones personalizadas.


# Clase base para todos los errores del sistema.
class ErrorSistema(Exception):
    pass  # Hereda el comportamiento de Exception.


# Excepción para datos incorrectos o incompletos.
class DatosInvalidosError(ErrorSistema):
    pass


# Excepción para clientes duplicados.
class ClienteDuplicadoError(ErrorSistema):
    pass


# Excepción para servicios duplicados.
class ServicioDuplicadoError(ErrorSistema):
    pass


# Excepción para clientes que no existen.
class ClienteNoEncontradoError(ErrorSistema):
    pass


# Excepción para servicios que no existen.
class ServicioNoEncontradoError(ErrorSistema):
    pass


# Excepción para servicios no disponibles.
class ServicioNoDisponibleError(ErrorSistema):
    pass


# Excepción para reservas incorrectas.
class ReservaInvalidaError(ErrorSistema):
    pass


# Excepción para reservas que no existen.
class ReservaNoEncontradaError(ErrorSistema):
    pass


# Excepción para operaciones no permitidas.
class OperacionNoPermitidaError(ErrorSistema):
    pass


# Excepción para errores en el cálculo de costos.
class CalculoCostoError(ErrorSistema):
    pass
