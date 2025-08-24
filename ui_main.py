from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QInputDialog, QMessageBox, QLineEdit
)
import database
from ui_formulario import FormularioProducto
import pandas as pd

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Stock - Almacén")
        self.resize(850, 500)

        layout = QVBoxLayout()

        # Campo de escaneo de código
        self.input_scan = QLineEdit()
        self.input_scan.setPlaceholderText("Escanee un código de barras aquí y presione Enter")
        layout.addWidget(self.input_scan)
        self.input_scan.returnPressed.connect(self.procesar_codigo)

        # Tabla
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Historial
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setMaximumHeight(120)
        layout.addWidget(self.historial)

        # Botones
        botones = QHBoxLayout()
        self.btn_agregar = QPushButton("➕ Agregar producto manual")
        self.btn_modificar = QPushButton("✏️ Modificar stock")
        self.btn_eliminar = QPushButton("🗑 Eliminar producto")
        self.btn_exportar = QPushButton("📤 Exportar a Excel")
        botones.addWidget(self.btn_agregar)
        botones.addWidget(self.btn_modificar)
        botones.addWidget(self.btn_eliminar)
        botones.addWidget(self.btn_exportar)
        layout.addLayout(botones)

        self.setLayout(layout)

        # Datos iniciales
        self.actualizar_tabla()
        self.actualizar_historial()

        # Conexiones
        self.btn_agregar.clicked.connect(self.abrir_formulario)
        self.btn_modificar.clicked.connect(self.modificar_stock)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_exportar.clicked.connect(self.exportar_excel)

    def actualizar_tabla(self):
        productos = database.obtener_productos()
        self.table.setRowCount(len(productos))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Cantidad", "Precio", "Movimientos"])
        for row, prod in enumerate(productos):
            for col, val in enumerate(prod):
                self.table.setItem(row, col, QTableWidgetItem(str(val)))

    def actualizar_historial(self):
        movimientos = database.obtener_movimientos()
        self.historial.clear()
        for m in movimientos:
            self.historial.append(f"[{m[3]}] {m[0]} ({m[1]} unidades) ${m[2]}")

    def abrir_formulario(self, codigo=""):
        dialog = FormularioProducto(codigo, self)
        if dialog.exec():
            self.actualizar_tabla()
            self.actualizar_historial()

    def procesar_codigo(self):
        codigo = self.input_scan.text().strip()
        if not codigo:
            return
        # Buscar producto por código
        productos = database.obtener_productos()
        encontrado = None
        for p in productos:
            if p[1] == codigo:  # columna código
                encontrado = p
                break

        if encontrado:
            # Sumar 1 unidad automáticamente
            database.modificar_stock(encontrado[0], 1)
            self.historial.append(f"[Auto] 1 unidad agregada a {encontrado[2]}")
        else:
            # Abrir formulario para producto nuevo
            self.abrir_formulario(codigo)

        self.input_scan.clear()
        self.actualizar_tabla()
        self.actualizar_historial()

    def modificar_stock(self):
        id_str, ok = QInputDialog.getText(self, "Modificar stock", "Ingrese ID del producto:")
        if not ok or not id_str.isdigit():
            return
        cantidad_str, ok = QInputDialog.getText(self, "Modificar stock", "Ingrese cantidad (+ o -):")
        if not ok:
            return
        try:
            cantidad = int(cantidad_str)
            if database.modificar_stock(int(id_str), cantidad):
                self.actualizar_tabla()
                self.actualizar_historial()
            else:
                QMessageBox.warning(self, "Error", "No se pudo modificar (ID inválido o stock insuficiente)")
        except ValueError:
            QMessageBox.warning(self, "Error", "Debe ingresar un número válido")

    def eliminar_producto(self):
        id_str, ok = QInputDialog.getText(self, "Eliminar producto", "Ingrese ID del producto a eliminar:")
        if not ok or not id_str.isdigit():
            return
        database.eliminar_producto(int(id_str))
        self.actualizar_tabla()
        self.actualizar_historial()

    def exportar_excel(self):
        productos = database.obtener_productos()
        df = pd.DataFrame(productos, columns=["ID", "Código", "Nombre", "Cantidad", "Precio", "Movimientos"])
        df.to_excel("stock.xlsx", index=False)
        self.historial.append("✅ Exportado a stock.xlsx")
