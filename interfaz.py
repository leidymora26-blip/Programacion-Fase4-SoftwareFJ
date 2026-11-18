# Proyecto: Sistema Integral de Gestión - Software FJ
# Universidad Nacional Abierta y a Distancia - UNAD
# Módulo de interfaz gráfica.

# Importamos las herramientas de interfaz gráfica.
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Importamos la clase administradora del sistema.
from sistema import SistemaSoftwareFJ

# Importamos los tres servicios especializados.
from reserva_sala import ReservaSala
from alquiler_equipo import AlquilerEquipo
from asesoria import AsesoriaEspecializada

# Importamos las excepciones personalizadas.
from excepciones import ErrorSistema

# Importamos las funciones de registro.
from config_logs import registrar_evento, registrar_excepcion


# Excepción interna para cancelar formularios.
class FormularioCancelado(Exception):
    pass


# Definimos la clase de la interfaz gráfica.
class InterfazSoftwareFJ:

    # Constructor de la interfaz.
    def __init__(self, ventana):

        # Almacenamos la ventana principal.
        self.ventana = ventana

        # Creamos una instancia del sistema.
        self.sistema = SistemaSoftwareFJ()

        # Configuramos el título de la ventana.
        self.ventana.title("Software FJ - Sistema Integral")

        # Establecemos las dimensiones iniciales.
        self.ventana.geometry("1000x720")

        # Establecemos las dimensiones mínimas.
        self.ventana.minsize(800, 650)

        # Configuramos el color de fondo.
        self.ventana.configure(bg="#EDF2F8")

        # Configuramos los colores principales.
        self.azul_oscuro = "#142B49"
        self.azul = "#285486"
        self.blanco = "#FFFFFF"

        # Creamos las variables de los indicadores.
        self.total_clientes = tk.StringVar(value="0")
        self.total_servicios = tk.StringVar(value="0")
        self.total_reservas = tk.StringVar(value="0")

        # Construimos los componentes gráficos.
        self.crear_interfaz()

        # Mostramos el mensaje de bienvenida.
        self.mostrar_resultado(
            "Sistema Software FJ iniciado correctamente."
        )

    # Método para construir la interfaz gráfica.
    def crear_interfaz(self):

        # Creamos el encabezado principal.
        encabezado = tk.Frame(
            self.ventana,
            bg=self.azul_oscuro
        )

        # Ubicamos el encabezado.
        encabezado.pack(fill="x")

        # Mostramos el nombre de la empresa.
        tk.Label(
            encabezado,
            text="SOFTWARE FJ",
            font=("Arial", 26, "bold"),
            bg=self.azul_oscuro,
            fg=self.blanco
        ).pack(pady=(15, 2))

        # Mostramos el subtítulo.
        tk.Label(
            encabezado,
            text="Sistema Integral de Gestión",
            font=("Arial", 13),
            bg=self.azul_oscuro,
            fg=self.blanco
        ).pack(pady=(0, 15))

        # Creamos el panel de indicadores.
        indicadores = tk.Frame(
            self.ventana,
            bg="#EDF2F8"
        )

        # Ubicamos los indicadores.
        indicadores.pack(fill="x", padx=20, pady=15)

        # Definimos los datos de cada indicador.
        datos = [
            ("CLIENTES", self.total_clientes),
            ("SERVICIOS", self.total_servicios),
            ("RESERVAS", self.total_reservas)
        ]

        # Creamos los tres indicadores.
        for titulo, variable in datos:

            # Creamos la tarjeta.
            tarjeta = tk.Frame(
                indicadores,
                bg=self.blanco
            )

            # Distribuimos las tarjetas horizontalmente.
            tarjeta.pack(
                side="left",
                expand=True,
                fill="both",
                padx=5
            )

            # Mostramos el título del indicador.
            tk.Label(
                tarjeta,
                text=titulo,
                font=("Arial", 11, "bold"),
                bg=self.blanco,
                fg=self.azul
            ).pack(pady=(10, 2))

            # Mostramos el valor actualizado.
            tk.Label(
                tarjeta,
                textvariable=variable,
                font=("Arial", 26, "bold"),
                bg=self.blanco,
                fg=self.azul_oscuro
            ).pack(pady=(0, 10))

        # Creamos el panel de botones.
        panel = tk.Frame(
            self.ventana,
            bg="#EDF2F8"
        )

        # Ubicamos el panel.
        panel.pack(fill="x", padx=20)

        # Definimos los botones y sus funciones.
        botones = [
            ("Registrar cliente", self.registrar_cliente),
            ("Registrar servicio", self.registrar_servicio),
            ("Crear reserva", self.crear_reserva),
            ("Confirmar reserva", self.confirmar_reserva),
            ("Cancelar reserva", self.cancelar_reserva),
            ("Procesar reserva", self.procesar_reserva),
            ("Consultar clientes", self.listar_clientes),
            ("Consultar servicios", self.listar_servicios),
            ("Consultar reservas", self.listar_reservas),
            ("Resumen del sistema", self.mostrar_resumen),
            ("Limpiar pantalla", self.limpiar_resultados),
            ("Salir", self.salir)
        ]

        # Creamos los botones del menú.
        for indice, (texto, funcion) in enumerate(botones):

            # Creamos cada botón.
            boton = tk.Button(
                panel,
                text=texto,
                command=funcion,
                bg=self.azul,
                fg=self.blanco,
                font=("Arial", 11, "bold"),
                relief="flat",
                cursor="hand2",
                height=2
            )

            # Distribuimos los botones en tres columnas.
            boton.grid(
                row=indice // 3,
                column=indice % 3,
                padx=5,
                pady=5,
                sticky="ew"
            )

        # Configuramos el ancho de las columnas.
        for columna in range(3):
            panel.columnconfigure(columna, weight=1)

        # Creamos el título del área de resultados.
        tk.Label(
            self.ventana,
            text="Resultados de operaciones",
            font=("Arial", 13, "bold"),
            bg="#EDF2F8",
            fg=self.azul_oscuro
        ).pack(anchor="w", padx=25, pady=(15, 5))

        # Creamos el contenedor de resultados.
        contenedor = tk.Frame(self.ventana)

        # Ubicamos el contenedor.
        contenedor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 10)
        )

        # Creamos la barra de desplazamiento.
        barra = ttk.Scrollbar(contenedor)

        # Ubicamos la barra.
        barra.pack(side="right", fill="y")

        # Creamos el área de texto.
        self.resultados = tk.Text(
            contenedor,
            font=("Consolas", 11),
            bg=self.blanco,
            fg=self.azul_oscuro,
            wrap="word",
            yscrollcommand=barra.set,
            state="disabled"
        )

        # Ubicamos el área de texto.
        self.resultados.pack(fill="both", expand=True)

        # Vinculamos la barra de desplazamiento.
        barra.config(command=self.resultados.yview)

        # Creamos el pie de página.
        tk.Label(
            self.ventana,
            text="UNAD | Ingeniería de Sistemas | Software FJ",
            bg=self.azul_oscuro,
            fg=self.blanco,
            font=("Arial", 10)
        ).pack(fill="x", ipady=8)

        # Controlamos el cierre de la ventana.
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)

    # Método para solicitar información.
    def solicitar(self, mensaje, tipo=str):

        # Solicitamos un número entero.
        if tipo is int:
            valor = simpledialog.askinteger(
                "Software FJ", mensaje,
                parent=self.ventana
            )

        # Solicitamos un número decimal.
        elif tipo is float:
            valor = simpledialog.askfloat(
                "Software FJ", mensaje,
                parent=self.ventana
            )

        # Solicitamos una cadena de texto.
        else:
            valor = simpledialog.askstring(
                "Software FJ", mensaje,
                parent=self.ventana
            )

        # Detectamos si el usuario cancela.
        if valor is None:
            raise FormularioCancelado()

        # Retornamos el dato ingresado.
        return valor

    # Método para mostrar los resultados.
    def mostrar_resultado(self, mensaje):

        # Habilitamos temporalmente la edición.
        self.resultados.config(state="normal")

        # Insertamos el mensaje.
        self.resultados.insert(
            tk.END,
            str(mensaje) + "\n" + "-" * 60 + "\n"
        )

        # Desplazamos la vista al último mensaje.
        self.resultados.see(tk.END)

        # Bloqueamos la edición manual.
        self.resultados.config(state="disabled")

    # Método para actualizar los indicadores.
    def actualizar_indicadores(self):

        # Consultamos el resumen del sistema.
        resumen = self.sistema.resumen()

        # Actualizamos los valores.
        self.total_clientes.set(resumen["clientes"])
        self.total_servicios.set(resumen["servicios"])
        self.total_reservas.set(resumen["reservas"])

    # Método para controlar las operaciones gráficas.
    def ejecutar_operacion(self, operacion):

        # Intentamos ejecutar la operación.
        try:
            operacion()

        # Controlamos la cancelación de formularios.
        except FormularioCancelado:
            self.mostrar_resultado("Operación cancelada.")

        # Capturamos los errores personalizados.
        except ErrorSistema as error:

            # Registramos el error.
            registrar_excepcion(str(error))

            # Mostramos una alerta.
            messagebox.showerror("Error controlado", str(error))

            # Mostramos el error en el panel.
            self.mostrar_resultado(f"ERROR: {error}")

        # Capturamos errores inesperados.
        except Exception as error:

            # Registramos la excepción.
            registrar_excepcion(str(error))

            # Informamos al usuario.
            messagebox.showerror(
                "Error",
                "No fue posible completar la operación."
            )

        # Actualizamos los indicadores.
        finally:
            self.actualizar_indicadores()

    # Método para registrar clientes.
    def registrar_cliente(self):

        # Definimos la operación.
        def operacion():

            # Solicitamos los datos personales.
            identificador = self.solicitar("Identificación:")
            nombre = self.solicitar("Nombre completo:")
            correo = self.solicitar("Correo electrónico:")
            telefono = self.solicitar("Teléfono:")

            # Registramos el cliente.
            cliente = self.sistema.registrar_cliente(
                identificador, nombre, correo, telefono
            )

            # Mostramos la información.
            self.mostrar_resultado(
                "Cliente registrado correctamente.\n"
                + cliente.mostrar_informacion()
            )

            # Informamos el registro exitoso.
            messagebox.showinfo(
                "Registro exitoso",
                "Cliente registrado correctamente."
            )

        # Ejecutamos la operación protegida.
        self.ejecutar_operacion(operacion)

    # Método para registrar servicios.
    def registrar_servicio(self):

        # Definimos la operación.
        def operacion():

            # Solicitamos el tipo de servicio.
            tipo = self.solicitar(
                "Seleccione el tipo de servicio:\n"
                "1. Reserva de sala\n"
                "2. Alquiler de equipos\n"
                "3. Asesoría especializada",
                int
            )

            # Validamos la opción seleccionada.
            if tipo not in (1, 2, 3):
                raise ErrorSistema("Tipo de servicio inválido.")

            # Solicitamos los datos generales.
            codigo = self.solicitar("Código del servicio:")
            nombre = self.solicitar("Nombre del servicio:")
            tarifa = self.solicitar("Tarifa base por hora:", float)

            # Creamos una reserva de sala.
            if tipo == 1:

                # Solicitamos la capacidad.
                capacidad = self.solicitar("Capacidad máxima:", int)

                # Creamos el servicio especializado.
                servicio = ReservaSala(
                    codigo, nombre, tarifa, capacidad
                )

            # Creamos un alquiler de equipos.
            elif tipo == 2:

                # Solicitamos la cantidad de equipos.
                cantidad = self.solicitar("Cantidad de equipos:", int)

                # Creamos el servicio especializado.
                servicio = AlquilerEquipo(
                    codigo, nombre, tarifa, cantidad
                )

            # Creamos una asesoría especializada.
            else:

                # Solicitamos los datos específicos.
                especialidad = self.solicitar("Especialidad:")
                asesor = self.solicitar("Nombre del asesor:")

                # Creamos el servicio especializado.
                servicio = AsesoriaEspecializada(
                    codigo, nombre, tarifa,
                    especialidad, asesor
                )

            # Registramos el servicio.
            self.sistema.registrar_servicio(servicio)

            # Mostramos la información.
            self.mostrar_resultado(
                "Servicio registrado correctamente.\n"
                + servicio.mostrar_informacion()
            )

            # Informamos el resultado.
            messagebox.showinfo(
                "Registro exitoso",
                "Servicio registrado correctamente."
            )

        # Ejecutamos la operación protegida.
        self.ejecutar_operacion(operacion)

    # Método para crear reservas.
    def crear_reserva(self):

        # Definimos la operación.
        def operacion():

            # Solicitamos los datos de la reserva.
            codigo = self.solicitar("Código de la reserva:")
            cliente = self.solicitar("Identificación del cliente:")
            servicio = self.solicitar("Código del servicio:")
            duracion = self.solicitar("Duración en horas:", float)
            impuesto = self.solicitar("Impuesto (%):", float)
            descuento = self.solicitar("Descuento (%):", float)

            # Creamos la reserva.
            reserva = self.sistema.crear_reserva(
                codigo, cliente, servicio,
                duracion, impuesto, descuento
            )

            # Mostramos la información.
            self.mostrar_resultado(
                "Reserva creada correctamente.\n"
                + reserva.mostrar_informacion()
            )

            # Informamos el resultado.
            messagebox.showinfo(
                "Reserva exitosa",
                "Reserva creada correctamente."
            )

        # Ejecutamos la operación protegida.
        self.ejecutar_operacion(operacion)

    # Método para confirmar reservas.
    def confirmar_reserva(self):

        # Definimos la operación.
        def operacion():

            # Solicitamos el código.
            codigo = self.solicitar("Código de la reserva:")

            # Confirmamos la reserva.
            mensaje = self.sistema.confirmar_reserva(codigo)

            # Mostramos el resultado.
            self.mostrar_resultado(mensaje)
            messagebox.showinfo("Confirmación", mensaje)

        # Ejecutamos la operación.
        self.ejecutar_operacion(operacion)

    # Método para cancelar reservas.
    def cancelar_reserva(self):

        # Definimos la operación.
        def operacion():

            # Solicitamos el código.
            codigo = self.solicitar("Código de la reserva:")

            # Solicitamos confirmación al usuario.
            confirmar = messagebox.askyesno(
                "Cancelar reserva",
                "¿Desea cancelar esta reserva?"
            )

            # Cancelamos si el usuario acepta.
            if confirmar:
                mensaje = self.sistema.cancelar_reserva(codigo)
                self.mostrar_resultado(mensaje)
                messagebox.showinfo("Cancelación", mensaje)

        # Ejecutamos la operación.
        self.ejecutar_operacion(operacion)

    # Método para procesar reservas.
    def procesar_reserva(self):

        # Definimos la operación.
        def operacion():

            # Solicitamos el código.
            codigo = self.solicitar("Código de la reserva:")

            # Procesamos la reserva.
            mensaje = self.sistema.procesar_reserva(codigo)

            # Mostramos el resultado.
            self.mostrar_resultado(mensaje)
            messagebox.showinfo("Procesamiento", mensaje)

        # Ejecutamos la operación.
        self.ejecutar_operacion(operacion)

    # Método auxiliar para mostrar listas.
    def mostrar_lista(self, titulo, elementos):

        # Mostramos el encabezado.
        self.mostrar_resultado(titulo)

        # Verificamos si existen registros.
        if not elementos:
            self.mostrar_resultado("No existen registros.")

        # Mostramos cada elemento.
        else:
            for elemento in elementos:
                self.mostrar_resultado(elemento)

    # Método para consultar clientes.
    def listar_clientes(self):
        self.ejecutar_operacion(
            lambda: self.mostrar_lista(
                "CLIENTES REGISTRADOS",
                self.sistema.listar_clientes()
            )
        )

    # Método para consultar servicios.
    def listar_servicios(self):
        self.ejecutar_operacion(
            lambda: self.mostrar_lista(
                "SERVICIOS REGISTRADOS",
                self.sistema.listar_servicios()
            )
        )

    # Método para consultar reservas.
    def listar_reservas(self):
        self.ejecutar_operacion(
            lambda: self.mostrar_lista(
                "RESERVAS REGISTRADAS",
                self.sistema.listar_reservas()
            )
        )

    # Método para mostrar las estadísticas.
    def mostrar_resumen(self):

        # Consultamos las estadísticas del sistema.
        resumen = self.sistema.resumen()

        # Creamos el encabezado.
        mensaje = "=== RESUMEN DEL SISTEMA ===\n"

        # Recorremos las estadísticas.
        for clave, valor in resumen.items():

            # Aplicamos formato monetario a los ingresos.
            if clave == "ingresos":
                mensaje += f"Ingresos: ${valor:,.2f}\n"

            # Mostramos los demás valores.
            else:
                mensaje += f"{clave.capitalize()}: {valor}\n"

        # Mostramos el resumen.
        self.mostrar_resultado(mensaje)

    # Método para limpiar el área de resultados.
    def limpiar_resultados(self):

        # Habilitamos la edición.
        self.resultados.config(state="normal")

        # Eliminamos el contenido.
        self.resultados.delete("1.0", tk.END)

        # Bloqueamos nuevamente la edición.
        self.resultados.config(state="disabled")

    # Método para cerrar la aplicación.
    def salir(self):

        # Solicitamos confirmación.
        confirmar = messagebox.askyesno(
            "Salir",
            "¿Desea cerrar Software FJ?\n"
            "Los registros almacenados en memoria se perderán."
        )

        # Cerramos si el usuario acepta.
        if confirmar:

            # Registramos el cierre.
            registrar_evento("Aplicación Software FJ cerrada.")

            # Destruimos la ventana.
            self.ventana.destroy()


# Verificamos si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Creamos la ventana principal.
    ventana = tk.Tk()

    # Creamos la aplicación.
    aplicacion = InterfazSoftwareFJ(ventana)

    # Mantenemos la ventana en funcionamiento.
    ventana.mainloop()
