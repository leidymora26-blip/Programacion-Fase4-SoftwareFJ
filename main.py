# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo principal de ejecución.

# Importamos la biblioteca para la interfaz gráfica.
import tkinter as tk

# Importamos la clase de la interfaz.
from interfaz import InterfazSoftwareFJ

# Importamos las funciones de registro.
from config_logs import registrar_evento, registrar_excepcion


# Definimos la función principal del programa.
def main():

    # Intentamos iniciar la aplicación.
    try:

        # Registramos el inicio del programa.
        registrar_evento("Inicio del programa principal.")

        # Creamos la ventana principal.
        ventana = tk.Tk()

        # Creamos una instancia de la aplicación.
        aplicacion = InterfazSoftwareFJ(ventana)

        # Mantenemos activa la interfaz gráfica.
        ventana.mainloop()

    # Capturamos posibles errores inesperados.
    except Exception as error:

        # Registramos el error en el archivo de logs.
        registrar_excepcion(
            f"Error en el programa principal: {error}"
        )

        # Informamos el error en la terminal.
        print(f"Error controlado: {error}")

    # Registramos la finalización del programa.
    finally:
        registrar_evento("Programa principal finalizado.")


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Ejecutamos la función principal.
    main()
