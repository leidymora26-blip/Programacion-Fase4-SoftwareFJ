# SOFTWARE FJ
## Sistema Integral de Gestión de Clientes, Servicios y Reservas

### Información académica

- Universidad Nacional Abierta y a Distancia - UNAD.
- Programa: Ingeniería de Sistemas.
- Curso: Programación Orientada a Objetos.
- Actividad: Fase 4.
- Estudiante: Leidy Johana Mora Rodríguez.
- Modalidad: Individual, con autorización.

## 1. Descripción del proyecto

Software FJ es una aplicación de escritorio desarrollada
en Python, utilizando los principios de la programación
orientada a objetos.

El sistema permite gestionar clientes, servicios y reservas
mediante una interfaz gráfica desarrollada con Tkinter.

La aplicación no utiliza bases de datos. La información
se administra mediante objetos y listas internas, mientras
que los archivos se utilizan para registrar eventos y errores.

## 2. Objetivo del proyecto

Desarrollar un sistema integral, modular, robusto y
extensible que permita gestionar clientes, servicios y
reservas, aplicando los principios de la programación
orientada a objetos y el manejo avanzado de excepciones.

## 3. Funcionalidades

- Registro de clientes.
- Validación de datos personales.
- Registro de servicios.
- Reserva de salas.
- Alquiler de equipos tecnológicos.
- Asesorías especializadas.
- Creación de reservas.
- Confirmación de reservas.
- Cancelación de reservas.
- Procesamiento de reservas.
- Cálculo de costos, impuestos y descuentos.
- Consulta de registros.
- Generación de estadísticas.
- Registro de eventos y errores.
- Interfaz gráfica de usuario.
- Simulación de 20 operaciones de prueba.

## 4. Principios de programación orientada a objetos

### Abstracción

Implementación de clases abstractas, como Entidad
y Servicio.

### Encapsulación

Protección de atributos y listas internas mediante
propiedades y métodos de acceso.

### Herencia

Creación de clases especializadas a partir de
clases base.

### Polimorfismo

Implementación de comportamientos específicos para
cada tipo de servicio.

### Sobrescritura de métodos

Redefinición de métodos heredados según las
características de cada servicio.

### Sobrecarga de comportamiento

Utilización de parámetros opcionales para calcular
costos con impuestos y descuentos.

## 5. Manejo avanzado de excepciones

El sistema incorpora:

- Excepciones personalizadas.
- Bloques try/except.
- Bloques try/except/else.
- Bloques try/except/finally.
- Encadenamiento de excepciones.
- Decoradores para el control de errores.
- Validación de datos.
- Registro de eventos y excepciones.

## 6. Estructura del proyecto

Software_FJ/
    excepciones.py
    config_logs.py
    entidad.py
    cliente.py
    servicio.py
    reserva_sala.py
    alquiler_equipo.py
    asesoria.py
    reserva.py
    sistema.py
    pruebas.py
    interfaz.py
    main.py
    README.md
    software_fj.log (generado durante la ejecución)

## 7. Tecnologías utilizadas

- Python 3.13.
- Tkinter.
- Visual Studio Code.
- GitHub.
- ABC.
- Logging.
- Pathlib.
- Functools.

## 8. Requisitos de ejecución

- Tener Python 3 instalado.
- Contar con Tkinter.
- Descargar los archivos del repositorio.
- No se requiere un motor de base de datos.

## 9. Ejecución del programa

Abrir una terminal en la carpeta del proyecto y ejecutar:

    python main.py

## 10. Ejecución de las pruebas

Para ejecutar las 20 operaciones de simulación:

    python pruebas.py

Las pruebas incluyen operaciones válidas e inválidas,
con el propósito de verificar la estabilidad y el
manejo de excepciones del sistema.

## 11. Registro de eventos

El archivo software_fj.log permite consultar los
eventos y errores registrados durante la ejecución
de la aplicación.

## 12. Conclusión

El desarrollo de Software FJ permite aplicar los
principios de la programación orientada a objetos
en un contexto empresarial simulado, integrando
validaciones, manejo de excepciones y una interfaz
gráfica para facilitar la gestión de la información.

---

Proyecto académico - UNAD - 2026.
