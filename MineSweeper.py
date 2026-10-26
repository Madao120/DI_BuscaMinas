import random
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QWidget, QLabel, QVBoxLayout, QMessageBox,
)


class MineSweeper(QMainWindow):
    FILAS = 9
    COLUMNAS = 9
    BOMBAS = 10

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MineSweeper")
        self.setFixedSize(500, 550)

        contenedor = QWidget()
        layout_principal = QVBoxLayout()

        self.informacion = QLabel()
        self.boton_nueva_partida = QPushButton("Nueva partida")
        self.boton_nueva_partida.clicked.connect(self.nueva_partida)


        self.tablero = QGridLayout()

        self.botones = []

        for fila in range(9):
            fila_botones = []

            for columna in range(9):
                boton = QPushButton()
                boton.setFixedSize(45, 45)

                boton.clicked.connect(
                    lambda _, f=fila, c = columna: self.pulsar_boton(f,c)
                )

                boton.setContextMenuPolicy(
                    Qt.ContextMenuPolicy.CustomContextMenu
                )

                boton.customContextMenuRequested.connect(
                    lambda _, f=fila, c=columna: self.marcar_bandera(f, c)
                )

                self.tablero.addWidget(boton, fila, columna)
                fila_botones.append(boton)

            self.botones.append(fila_botones)

        layout_principal.addWidget(self.informacion)
        layout_principal.addLayout(self.tablero)
        layout_principal.addWidget(self.boton_nueva_partida)

        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        self.nueva_partida()

    def nueva_partida(self):
        self.partida_terminada = False
        self.casillas_reveladas = 0

        # -1 representa una bomba.
        # 0-8 representa el número de bombas cercanas.
        self.matriz = [
            [0 for _ in range(self.COLUMNAS)]
            for _ in range(self.FILAS)
        ]

        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                boton = self.botones[fila][columna]
                boton.setText("")
                boton.setEnabled(True)
                boton.setStyleSheet("")

        self.colocar_bombas()
        self.calcular_numeros()

        self.informacion.setText(
            f"Bombas: {self.BOMBAS}"
        )

    def colocar_bombas(self):
        posiciones = [
            (fila, columna)
            for fila in range(self.FILAS)
            for columna in range(self.COLUMNAS)
        ]

        bombas = random.sample(posiciones, self.BOMBAS)

        for fila, columna in bombas:
            self.matriz[fila][columna] = -1

    def calcular_numeros(self):
        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                if self.matriz[fila][columna] == -1:
                    continue

                bombas_cercanas = 0

                for fila_vecina, columna_vecina in self.vecinas(
                        fila, columna
                ):
                    if self.matriz[fila_vecina][columna_vecina] == -1:
                        bombas_cercanas += 1

                self.matriz[fila][columna] = bombas_cercanas

    def vecinas(self, fila, columna):
        for cambio_fila in (-1, 0, 1):
            for cambio_columna in (-1, 0, 1):
                if cambio_fila == 0 and cambio_columna == 0:
                    continue

                nueva_fila = fila + cambio_fila
                nueva_columna = columna + cambio_columna

                if (
                        0 <= nueva_fila < self.FILAS
                        and 0 <= nueva_columna < self.COLUMNAS
                ):
                    yield nueva_fila, nueva_columna

    def pulsar_boton(self, fila, columna):
        if self.partida_terminada:
            return

        boton = self.botones[fila][columna]

        if not boton.isEnabled():
            return

        # No porder clickar si tiene bandera
        if boton.text() == "🚩":
            return

        if self.matriz[fila][columna] == -1:
            boton.setText("💣")
            self.finalizar_partida(False)
            return

        self.revelar_casilla(fila, columna)
        self.comprobar_victoria()

    def revelar_casilla(self, fila, columna):
        boton = self.botones[fila][columna]

        if not boton.isEnabled():
            return

        valor = self.matriz[fila][columna]

        boton.setEnabled(False)
        self.casillas_reveladas += 1

        if valor > 0:
            boton.setText(str(valor))
            return

        # Si la casilla vale cero, revelamos también sus vecinas.
        for fila_vecina, columna_vecina in self.vecinas(fila, columna):
            if self.matriz[fila_vecina][columna_vecina] != -1:
                self.revelar_casilla(
                    fila_vecina,
                    columna_vecina
                )

    def finalizar_partida(self, victoria):
        self.partida_terminada = True

        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                boton = self.botones[fila][columna]

                if self.matriz[fila][columna] == -1:
                    boton.setText("💣")

                boton.setEnabled(False)

        if victoria:
            QMessageBox.information(
                self,
                "Victoria",
                "¡Has ganado la partida!",
            )
        else:
            QMessageBox.critical(
                self,
                "Fin de la partida",
                "Has pulsado una bomba.",
            )

    def marcar_bandera(self, fila, columna):
        if self.partida_terminada:
            return

        boton = self.botones[fila][columna]

        if not boton.isEnabled():
            return

        if boton.text() == "🚩":
            boton.setText("")
        else:
            boton.setText("🚩")

    def comprobar_victoria(self):
        casillas_sin_bomba = (
                self.FILAS * self.COLUMNAS - self.BOMBAS
        )

        if self.casillas_reveladas == casillas_sin_bomba:
            self.finalizar_partida(True)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = MineSweeper()
    ventana.show()
    sys.exit(aplicacion.exec())