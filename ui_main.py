from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit
)
import database

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Stock - Almacén")
        self.resize(700, 500)

        layout = QVBoxLayout()

        # Tabla principal
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Historial
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setMaximumHeight(100)
        layout.addWidget(self.historial)

        # Botones
        botones = QHBoxLayout()
        self.btn_agregar = QPushButton("➕ Agregar producto")
        self.btn_exportar = QPushButton("📤 Exportar a Excel")
        botones.addWidget(self.btn_agregar)
        botones.addWidget(self.btn_exportar)
        layout.addLayout(botones)

        self.setLayout(layout)

        # Cargar datos iniciales
        self.actualizar_tabla()
        self.actualizar_historial()

        # Conexiones
        self.btn_agregar.clicked.connect(self.demo_agregar)  # temporal
        self.btn_exportar.clicked.connect(self.exportar_excel)

    def actualizar_tabla(self):
        productos = database.obtener_productos()
        self.table.setRowCount(len(productos))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Precio"])
        for row, prod in enumerate(productos):
            for col, val in enumerate(prod):
                self.table.setItem(row, col, QTableWidgetItem(str(val)))

    def actualizar_historial(self):
        movimientos = database.obtener_movimientos()
        self.historial.clear()
        for m in movimientos:
            self.historial.append(f"[{m[3]}] {m[0]} ({m[1]} unidades) ${m[2]}")

    def demo_agregar(self):
        # Ejemplo rápido para probar
        database.agregar_producto("Yerba", 5, 1500)
        self.actualizar_tabla()
        self.actualizar_historial()

    def exportar_excel(self):
        import pandas as pd
        productos = database.obtener_productos()
        df = pd.DataFrame(productos, columns=["ID", "Nombre", "Cantidad", "Precio"])
        df.to_excel("stock.xlsx", index=False)
        self.historial.append("✅ Exportado a stock.xlsx")
