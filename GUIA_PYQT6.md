# Guía de sintaxis de PyQt6

Esta guía resume la sintaxis básica de **PyQt6** para crear interfaces gráficas
con Python. Los ejemplos utilizan los elementos que aparecen en el proyecto del
Buscaminas, pero se centran en la forma de escribirlos y relacionarlos, no en
explicar la lógica del juego.

## 1. Importar clases

Las clases de PyQt6 están agrupadas en módulos. Los widgets habituales se
encuentran en `PyQt6.QtWidgets`:

```python
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
```

También se puede importar una clase individual:

```python
from PyQt6.QtWidgets import QPushButton
```

La primera forma suele ser más cómoda cuando se utilizan varias clases.

## 2. La aplicación (`QApplication`)

Todo programa gráfico de PyQt necesita una instancia de `QApplication`:

```python
aplicacion = QApplication(sys.argv)
```

`sys.argv` permite que Qt reciba los argumentos utilizados al iniciar el
programa. Normalmente se escribe una sola instancia por aplicación.

Después se muestra la ventana y se inicia el bucle de eventos:

```python
ventana.show()
sys.exit(aplicacion.exec())
```

`exec()` mantiene la aplicación funcionando y espera eventos, como clics,
teclas o repintados de la ventana. Sin esta llamada, la aplicación terminaría
inmediatamente.

## 3. El punto de entrada

Esta condición hace que el código se ejecute solo cuando el archivo se inicia
directamente:

```python
if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = MineSweeper()
    ventana.show()
    sys.exit(aplicacion.exec())
```

Si el archivo se importa desde otro módulo, el bloque no se ejecuta
automáticamente.

## 4. Crear una ventana principal

Para una ventana principal se puede heredar de `QMainWindow`:

```python
class MineSweeper(QMainWindow):
    def __init__(self):
        super().__init__()
```

### `class`

Define una clase. La clase agrupa datos y funciones relacionados.

### `QMainWindow`

Es la clase base de una ventana principal de Qt. Al escribir:

```python
class MineSweeper(QMainWindow):
```

`MineSweeper` hereda las propiedades y métodos de `QMainWindow`.

### `__init__`

Es el método que se ejecuta al crear un objeto:

```python
ventana = MineSweeper()
```

### `self`

Representa el objeto actual. Se utiliza para guardar o acceder a elementos
pertenecientes a esa ventana:

```python
self.informacion = QLabel()
self.botones = []
```

Una variable local como esta:

```python
boton = QPushButton()
```

solo está disponible dentro del método actual. En cambio, una variable como:

```python
self.boton_nueva_partida = QPushButton()
```

puede utilizarse desde cualquier método de la clase.

### `super().__init__()`

Ejecuta el constructor de la clase heredada, en este caso `QMainWindow`.
Debe llamarse normalmente al principio de `__init__`.

## 5. Propiedades básicas de la ventana

Los métodos de Qt se llaman usando un punto:

```python
self.setWindowTitle("Buscaminas")
self.setFixedSize(500, 550)
```

Algunos métodos frecuentes:

```python
self.setWindowTitle("Título")  # Título de la ventana
self.resize(800, 600)          # Tamaño inicial
self.setFixedSize(500, 550)    # Tamaño que no se puede cambiar
self.show()                    # Muestra una ventana
self.close()                   # Cierra una ventana
```

## 6. Widgets

Un **widget** es un elemento visual de la interfaz: una etiqueta, un botón,
una entrada de texto o un contenedor.

### Etiqueta

```python
etiqueta = QLabel("Texto inicial")
```

Cambiar su texto:

```python
etiqueta.setText("Texto nuevo")
```

Leer su texto:

```python
texto = etiqueta.text()
```

### Botón

```python
boton = QPushButton("Aceptar")
```

Un botón sin texto también es válido:

```python
boton = QPushButton()
```

Métodos habituales:

```python
boton.setText("Abrir")
texto = boton.text()

boton.setEnabled(False)  # Desactiva el botón
boton.setEnabled(True)   # Activa el botón

esta_activo = boton.isEnabled()
```

También se puede cambiar su tamaño:

```python
boton.setFixedSize(45, 45)
```

## 7. `QWidget` como contenedor

`QWidget` puede actuar como un contenedor para otros elementos:

```python
contenedor = QWidget()
```

Una ventana `QMainWindow` necesita normalmente un widget central:

```python
self.setCentralWidget(contenedor)
```

`setCentralWidget()` recibe un `QWidget`, no un layout directamente. Por eso
se suele crear un contenedor, asignarle un layout y convertirlo en el
contenido central de la ventana:

```python
contenedor = QWidget()
layout = QVBoxLayout()

contenedor.setLayout(layout)
self.setCentralWidget(contenedor)
```

## 8. Layouts

Los layouts organizan widgets y calculan automáticamente su posición y
tamaño.

### `QVBoxLayout`

Coloca los elementos verticalmente:

```python
layout = QVBoxLayout()

layout.addWidget(QLabel("Título"))
layout.addWidget(QPushButton("Jugar"))
```

Resultado conceptual:

```text
Título
Jugar
```

### `QHBoxLayout`

Coloca los elementos horizontalmente:

```python
layout = QHBoxLayout()

layout.addWidget(QPushButton("Sí"))
layout.addWidget(QPushButton("No"))
```

Resultado conceptual:

```text
Sí    No
```

### `QGridLayout`

Coloca widgets en una cuadrícula:

```python
layout = QGridLayout()

layout.addWidget(widget, fila, columna)
```

Los índices empiezan en cero:

```python
layout.addWidget(boton_a, 0, 0)
layout.addWidget(boton_b, 0, 1)
layout.addWidget(boton_c, 1, 0)
```

La llamada tiene esta forma:

```python
layout.addWidget(widget, fila, columna)
```

`fila` y `columna` no son coordenadas de pantalla. Son la posición lógica del
widget dentro del `QGridLayout`.

### Añadir widgets y layouts

Para añadir un widget se usa:

```python
layout.addWidget(widget)
```

Para añadir otro layout se usa:

```python
layout.addLayout(otro_layout)
```

Ejemplo de layouts anidados:

```python
principal = QVBoxLayout()
tablero = QGridLayout()

principal.addWidget(QLabel("Buscaminas"))
principal.addLayout(tablero)
principal.addWidget(QPushButton("Nueva partida"))
```

## 9. Crear widgets repetidos con `for`

No es necesario escribir cada botón por separado. `range(9)` genera los
números del `0` al `8`:

```python
for fila in range(9):
    for columna in range(9):
        boton = QPushButton()
        tablero.addWidget(boton, fila, columna)
```

Los dos bucles crean las 81 posiciones de una cuadrícula de 9 × 9.

Para conservar los botones, se puede guardar cada fila en una lista:

```python
botones = []

for fila in range(9):
    fila_botones = []

    for columna in range(9):
        boton = QPushButton()
        tablero.addWidget(boton, fila, columna)
        fila_botones.append(boton)

    botones.append(fila_botones)
```

El resultado es una lista de listas:

```python
botones[fila][columna]
```

Ejemplos:

```python
botones[0][0]  # Primera fila, primera columna
botones[4][4]  # Fila y columna centrales
botones[8][8]  # Última fila, última columna
```

## 10. Señales y slots

PyQt utiliza **señales** para avisar de que ha ocurrido un evento. Los
métodos que responden a esos eventos suelen llamarse **slots**.

La señal de clic de un botón es `clicked`:

```python
boton.clicked.connect(funcion)
```

`connect()` establece la relación entre la señal y la función. La función no
debe ejecutarse al conectar:

```python
# Correcto: se pasa la función
boton.clicked.connect(self.pulsar)

# Incorrecto: se ejecuta inmediatamente
boton.clicked.connect(self.pulsar())
```

La diferencia son los paréntesis. Sin paréntesis se entrega la función; con
paréntesis se llama a la función en ese momento.

Ejemplo:

```python
def pulsar(self):
    print("Se ha pulsado el botón")

boton.clicked.connect(self.pulsar)
```

## 11. Funciones y métodos

Un método dentro de una clase se define con `def` y recibe `self` como primer
parámetro:

```python
class Ventana(QMainWindow):
    def mostrar_mensaje(self):
        print("Mensaje")
```

Se llama desde la propia clase mediante `self`:

```python
self.mostrar_mensaje()
```

Un método puede recibir argumentos:

```python
def mostrar_posicion(self, fila, columna):
    print(fila, columna)
```

## 12. `lambda` para pasar argumentos a una señal

`clicked` puede emitir un argumento. Si se necesita pasar argumentos propios a
un método, se puede utilizar `lambda`:

```python
boton.clicked.connect(
    lambda _, f=fila, c=columna: self.pulsar_boton(f, c)
)
```

La sintaxis general de una función lambda es:

```python
lambda argumentos: expresion
```

Esta expresión:

```python
lambda x: x * 2
```

crea una función pequeña equivalente a:

```python
def duplicar(x):
    return x * 2
```

En el ejemplo del botón:

```python
lambda _, f=fila, c=columna: self.pulsar_boton(f, c)
```

- `_` recibe el argumento que envía PyQt y que no se necesita.
- `f=fila` guarda la fila actual.
- `c=columna` guarda la columna actual.
- `self.pulsar_boton(f, c)` se ejecuta cuando se pulsa el botón.

Los valores por defecto `f=fila` y `c=columna` son importantes dentro de un
bucle, porque conservan la posición correspondiente a cada botón.

Otra forma de pasar argumentos es `partial`:

```python
from functools import partial

boton.clicked.connect(
    partial(self.pulsar_boton, fila, columna)
)
```

## 13. Estilos

Qt permite aplicar estilos mediante una cadena con sintaxis similar a CSS:

```python
boton.setStyleSheet("""
    QPushButton {
        background-color: lightgray;
        border: 1px solid black;
    }
""")
```

Para quitar un estilo establecido:

```python
boton.setStyleSheet("")
```

También se pueden seleccionar estados:

```python
boton.setStyleSheet("""
    QPushButton:hover {
        background-color: yellow;
    }
""")
```

## 14. Cuadros de diálogo

`QMessageBox` muestra mensajes al usuario:

```python
QMessageBox.information(
    self,
    "Información",
    "Operación realizada",
)
```

Otros tipos habituales:

```python
QMessageBox.warning(self, "Aviso", "Hay un problema")
QMessageBox.critical(self, "Error", "La operación ha fallado")
```

El primer argumento suele ser la ventana padre, el segundo es el título y el
tercero es el texto.

## 15. Constantes de clase

Los datos que no deberían cambiar durante la ejecución pueden definirse como
atributos de clase:

```python
class MineSweeper(QMainWindow):
    FILAS = 9
    COLUMNAS = 9
    BOMBAS = 10
```

Desde un método se accede a ellos mediante `self`:

```python
for fila in range(self.FILAS):
    for columna in range(self.COLUMNAS):
        ...
```

También se puede acceder usando el nombre de la clase:

```python
MineSweeper.FILAS
```

## 16. Esquema mínimo de una aplicación

La estructura mínima habitual es:

```python
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi aplicación")


if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(aplicacion.exec())
```

Una estructura con contenedor y layout sería:

```python
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        contenedor = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Hola"))
        layout.addWidget(QPushButton("Aceptar"))

        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)
```

## 17. Errores frecuentes

### No llamar a `exec()`

```python
ventana.show()
# Falta iniciar el bucle de eventos
```

Solución:

```python
sys.exit(aplicacion.exec())
```

### Pasar un layout directamente a `setCentralWidget`

```python
self.setCentralWidget(layout)  # Incorrecto
```

Solución:

```python
contenedor = QWidget()
contenedor.setLayout(layout)
self.setCentralWidget(contenedor)
```

### Ejecutar el método en vez de conectarlo

```python
boton.clicked.connect(self.accion())  # Incorrecto
```

Solución:

```python
boton.clicked.connect(self.accion)
```

Si necesita argumentos:

```python
boton.clicked.connect(lambda: self.accion(valor))
```

### Crear el layout dentro de un bucle por accidente

La creación de botones puede estar dentro de un `for`, pero la configuración
final del contenedor normalmente debe hacerse una sola vez, después del bucle:

```python
for fila in range(9):
    ...

layout_principal.addLayout(tablero)
contenedor.setLayout(layout_principal)
self.setCentralWidget(contenedor)
```

### Indentar un método dentro de otro

Los métodos de una clase deben estar al mismo nivel:

```python
class Ventana(QMainWindow):
    def primero(self):
        pass

    def segundo(self):
        pass
```

Si `segundo` tiene una indentación adicional, se convierte en una función
local de `primero` y no estará disponible como `self.segundo`.

## 18. Orden recomendado al construir una interfaz

Una forma clara de organizar `__init__` es:

```python
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Configuración de la ventana
        self.setWindowTitle("Título")

        # 2. Crear contenedores y layouts
        contenedor = QWidget()
        layout = QVBoxLayout()

        # 3. Crear widgets
        self.etiqueta = QLabel("Texto")
        self.boton = QPushButton("Pulsar")

        # 4. Conectar señales
        self.boton.clicked.connect(self.accion)

        # 5. Añadir widgets al layout
        layout.addWidget(self.etiqueta)
        layout.addWidget(self.boton)

        # 6. Asignar el layout y el widget central
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

    def accion(self):
        self.etiqueta.setText("Pulsado")
```

Esta separación facilita localizar errores y permite distinguir entre:

- la creación de objetos;
- su organización visual;
- la conexión de eventos;
- el comportamiento de los métodos.

## 19. Cómo aprender a crear funciones por tu cuenta

La mejor forma de aprender a crear funciones no es memorizar código, sino
aprender a convertir un problema en pasos pequeños.

### 19.1. Describe la función con palabras

Antes de escribir código, responde:

- ¿Qué tarea debe realizar?
- ¿Qué datos necesita?
- ¿Qué resultado debe producir?
- ¿Qué casos especiales pueden ocurrir?

Por ejemplo, para colocar bombas:

> Necesito una función que cree posiciones posibles, elija algunas al azar y
> marque esas posiciones como bombas.

A partir de ahí:

```python
def colocar_bombas(self):
    # 1. Crear posiciones
    # 2. Elegir posiciones
    # 3. Marcar bombas
```

### 19.2. La estructura básica de una función

Una función tiene esta forma:

```python
def nombre_de_la_funcion(parametro1, parametro2):
    resultado = parametro1 + parametro2
    return resultado
```

Ejemplo:

```python
def sumar(numero1, numero2):
    return numero1 + numero2
```

Se utiliza así:

```python
resultado = sumar(3, 5)
print(resultado)  # 8
```

En una clase, la función se llama método y recibe `self` como primer
parámetro:

```python
class Juego:
    def mostrar_mensaje(self, mensaje):
        print(mensaje)
```

Se llama así:

```python
juego = Juego()
juego.mostrar_mensaje("Hola")
```

### 19.3. Separa entrada, proceso y salida

Una técnica útil es separar cada función en tres partes:

```text
Entrada → Proceso → Salida
```

Ejemplo: contar bombas cercanas.

```text
Entrada:
    fila y columna de una casilla

Proceso:
    revisar las casillas vecinas
    contar cuántas son bombas

Salida:
    número de bombas cercanas
```

Código:

```python
def contar_bombas_cercanas(self, fila, columna):
    contador = 0

    for fila_vecina, columna_vecina in self.vecinas(fila, columna):
        if self.matriz[fila_vecina][columna_vecina] == -1:
            contador += 1

    return contador
```

La función hace una sola tarea: contar. No crea botones, no muestra mensajes y
no termina la partida.

### 19.4. Divide las funciones grandes

Una función es demasiado grande cuando hace muchas cosas distintas. Por
ejemplo, `nueva_partida()` se puede dividir:

```python
def nueva_partida(self):
    self.reiniciar_botones()
    self.crear_matriz()
    self.colocar_bombas()
    self.calcular_numeros()
```

Cada función tiene una responsabilidad:

```python
def reiniciar_botones(self):
    for fila in range(self.FILAS):
        for columna in range(self.COLUMNAS):
            boton = self.botones[fila][columna]
            boton.setText("")
            boton.setEnabled(True)
```

```python
def crear_matriz(self):
    self.matriz = [
        [0 for _ in range(self.COLUMNAS)]
        for _ in range(self.FILAS)
    ]
```

La función principal resulta más fácil de leer porque describe el proceso
general.

### 19.5. Practica primero sin PyQt

Antes de mezclar lógica y ventanas, prueba las funciones en la consola:

```python
def es_bomba(valor):
    return valor == -1


print(es_bomba(-1))  # True
print(es_bomba(3))   # False
```

Otro ejemplo:

```python
def obtener_vecinas(fila, columna, filas, columnas):
    resultado = []

    for cambio_fila in (-1, 0, 1):
        for cambio_columna in (-1, 0, 1):
            if cambio_fila == 0 and cambio_columna == 0:
                continue

            nueva_fila = fila + cambio_fila
            nueva_columna = columna + cambio_columna

            if (
                0 <= nueva_fila < filas
                and 0 <= nueva_columna < columnas
            ):
                resultado.append((nueva_fila, nueva_columna))

    return resultado
```

Se puede comprobar así:

```python
print(obtener_vecinas(0, 0, 9, 9))
```

Cuando una función funciona correctamente, se puede conectar con PyQt.

### 19.6. Ejercicios progresivos para el Buscaminas

#### Ejercicio 1: crear una matriz

```python
def crear_matriz(filas, columnas, valor_inicial):
    return [
        [valor_inicial for _ in range(columnas)]
        for _ in range(filas)
    ]
```

Prueba:

```python
matriz = crear_matriz(3, 3, 0)
print(matriz)
```

#### Ejercicio 2: marcar una bomba

```python
def marcar_bomba(matriz, fila, columna):
    matriz[fila][columna] = -1
```

#### Ejercicio 3: comprobar una bomba

```python
def es_bomba(matriz, fila, columna):
    return matriz[fila][columna] == -1
```

#### Ejercicio 4: contar bombas cercanas

Primero escribe una función que devuelva las vecinas. Después utiliza esa
función para contar cuántas de ellas son bombas.

#### Ejercicio 5: conectar la lógica con un botón

Cuando la lógica anterior funcione:

```python
boton.clicked.connect(
    lambda _, f=fila, c=columna: self.pulsar_boton(f, c)
)
```

La interfaz debería encargarse de mostrar información; las funciones deberían
encargarse de calcularla.

### 19.7. Elige nombres descriptivos

Un buen nombre ayuda a entender qué hace una función:

```python
colocar_bombas()
calcular_numeros()
contar_bombas_cercanas()
revelar_casilla()
comprobar_victoria()
reiniciar_botones()
```

Evita nombres poco descriptivos:

```python
hacer_cosa()
funcion1()
procesar()
```

Una función debería poder resumirse en una frase:

> `contar_bombas_cercanas` cuenta las bombas que rodean una casilla.

Si no se puede explicar una función en una sola frase, probablemente hace
demasiadas cosas.

### 19.8. Prueba cada función por separado

No esperes a ejecutar todo el juego para descubrir errores:

```python
def multiplicar(a, b):
    return a * b


print(multiplicar(2, 3))
print(multiplicar(0, 5))
print(multiplicar(-1, 4))
```

Para el Buscaminas:

```python
matriz = [
    [0, 0, 0],
    [0, -1, 0],
    [0, 0, 0],
]

print(es_bomba(matriz, 1, 1))  # True
print(es_bomba(matriz, 0, 0))  # False
```

Conviene comprobar:

- un caso normal;
- un caso vacío o cero;
- un caso límite;
- un caso incorrecto, si puede producirse.

### 19.9. Utiliza los errores como información

`AttributeError` suele indicar que se intenta acceder a un atributo o método
que no existe.

`IndexError` suele indicar que se intenta acceder a una posición inexistente de
una lista.

`TypeError` suele indicar que un tipo de dato se está utilizando de una forma
no válida.

Lee el error desde la última línea hacia arriba:

```text
File "...", line 92, in colocar_bombas
```

Eso indica dónde ocurrió el problema. Después revisa la línea concreta y los
valores que utiliza.

Para investigar se pueden imprimir valores:

```python
print(f"fila={fila}, columna={columna}")
print(self.botones)
```

### 19.10. Método de estudio recomendado

Para cada función nueva:

1. Escribe con palabras qué debe hacer.
2. Define qué datos recibe.
3. Define qué resultado devuelve o modifica.
4. Escribe un ejemplo manual.
5. Implementa la versión más sencilla.
6. Pruébala fuera de PyQt si es posible.
7. Conéctala a la interfaz.
8. Prueba casos normales y límites.
9. Divide la función si empieza a hacerse difícil de leer.

Por ejemplo:

```text
Función: contar_bombas_cercanas
Recibe: fila y columna
Consulta: matriz y vecinas
Devuelve: un número
No hace: modificar botones ni mostrar ventanas
```

Este pequeño diseño ya indica cómo empezar a escribir la función. No es
necesario recordar una solución completa: es mejor escribir una versión
pequeña, ejecutarla, leer el error y mejorarla paso a paso.
