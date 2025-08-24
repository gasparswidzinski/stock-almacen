from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog
)
import pandas as pd
import database
from ui_formulario import FormularioProducto
from ui_vender import FormularioVenta
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtGui import QColor



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
        # Botones
        botones = QHBoxLayout()
        self.btn_agregar = QPushButton("➕ Agregar producto")
        self.btn_editar = QPushButton("✏️ Editar producto")
        self.btn_eliminar = QPushButton("🗑 Eliminar producto")
        self.btn_importar = QPushButton("📥 Importar desde Excel")
        self.btn_exportar = QPushButton("📤 Exportar a Excel")
        self.btn_vender = QPushButton("🛒 Vender producto")

        botones.addWidget(self.btn_agregar)
        botones.addWidget(self.btn_editar)
        botones.addWidget(self.btn_eliminar)
        botones.addWidget(self.btn_importar)
        botones.addWidget(self.btn_exportar)
        botones.addWidget(self.btn_vender)
        layout.addLayout(botones)
        self.setLayout(layout)
        
        # Atajos de teclado
        QShortcut(QKeySequence("F1"), self, activated=self.abrir_formulario)
        QShortcut(QKeySequence("F2"), self, activated=self.vender_producto)
        QShortcut(QKeySequence("F3"), self, activated=self.editar_producto)
        QShortcut(QKeySequence("Delete"), self, activated=self.eliminar_producto)

        # Cargar datos iniciales
        self.actualizar_tabla()
        self.actualizar_historial()

        # Conexiones
        self.btn_agregar.clicked.connect(self.abrir_formulario)
        self.btn_importar.clicked.connect(self.importar_excel)
        self.btn_exportar.clicked.connect(self.exportar_excel)
        self.btn_editar.clicked.connect(self.editar_producto)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_vender.clicked.connect(self.vender_producto)
        


    def actualizar_tabla(self):
        productos = database.obtener_productos()
        self.table.setRowCount(len(productos))
        self.table.setColumnCount(6)  # porque en la DB tenés: id, codigo, nombre, cantidad, precio, movimientos
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Cantidad", "Precio", "Movimientos"])

        for row, prod in enumerate(productos):
            for col, val in enumerate(prod):
                item = QTableWidgetItem(str(val))

                # Si estamos en la columna "Cantidad" (índice 3) y es bajo → rojo
                if col == 3 and int(val) <= 5:
                    item.setForeground(QColor("red"))

                self.table.setItem(row, col, item)
    
    def actualizar_historial(self):
        movimientos = database.obtener_movimientos()
        self.historial.clear()
        for m in movimientos:
            self.historial.append(f"[{m[3]}] {m[0]} ({m[1]} unidades) ${m[2]}")

    def abrir_formulario(self):
        dialog = FormularioProducto(self)
        if dialog.exec():
            datos = dialog.obtener_datos()
            try:
                database.agregar_o_actualizar_producto(
                    datos["codigo"],     # Código
                    datos["nombre"],     # Nombre
                    int(datos["cantidad"]),  # Cantidad
                    float(datos["precio"])   # Precio
                )
                self.actualizar_tabla()
                self.actualizar_historial()
            except ValueError:
                self.historial.append("⚠ Error: cantidad y precio deben ser números")

    def exportar_excel(self):
        productos = database.obtener_productos()
        df = pd.DataFrame(productos, columns=["ID", "Nombre", "Cantidad", "Precio"])
        df.to_excel("stock.xlsx", index=False)
        self.historial.append("✅ Exportado a stock.xlsx")

    def importar_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            df = pd.read_excel(file_path)
            # Espera columnas: Nombre, Cantidad, Precio
            for _, row in df.iterrows():
                database.agregar_o_actualizar_producto(
                    str(row["Codigo"]),   # Código (columna del Excel)
                    row["Nombre"],        # Nombre
                    int(row["Cantidad"]), # Cantidad
                    float(row["Precio"])  # Precio
                )
            self.actualizar_tabla()
            self.actualizar_historial()
            self.historial.append(f"📥 Importado desde {file_path}")

    def editar_producto(self):
        fila = self.table.currentRow()
        if fila < 0:
            self.historial.append("⚠ Selecciona un producto para editar")
            return

        id_ = int(self.table.item(fila, 0).text())
        datos = {
            "codigo": self.table.item(fila, 1).text(),   # Columna Código
            "nombre": self.table.item(fila, 2).text(),   # Columna Nombre
            "cantidad": self.table.item(fila, 3).text(), # Columna Cantidad
            "precio": self.table.item(fila, 4).text()    # Columna Precio
        }

        dialog = FormularioProducto(self, datos)
        if dialog.exec():
            d = dialog.obtener_datos()
            try:
                database.editar_producto(
                    id_,
                    d["nombre"],
                    int(d["cantidad"]),
                    float(d["precio"])
                )
                self.actualizar_tabla()
                self.actualizar_historial()
            except ValueError:
                self.historial.append("⚠ Error: cantidad y precio deben ser números")

    def eliminar_producto(self):
        fila = self.table.currentRow()
        if fila < 0:
            self.historial.append("⚠ Selecciona un producto para eliminar")
            return

        id_ = int(self.table.item(fila, 0).text())
        database.eliminar_producto(id_)
        self.actualizar_tabla()
        self.actualizar_historial()

    def vender_producto(self):
        fila = self.table.currentRow()
        if fila < 0:
            self.historial.append("⚠ Selecciona un producto para vender")
            return

        id_ = int(self.table.item(fila, 0).text())
        dialog = FormularioVenta(self)
        if dialog.exec():
            cantidad = dialog.obtener_cantidad()
            if cantidad is None or cantidad <= 0:
                self.historial.append("⚠ Cantidad inválida")
                return

            ok = database.modificar_stock(id_, -cantidad)
            if ok:
                self.actualizar_tabla()
                self.actualizar_historial()
                self.historial.append(f"🛒 Vendidas {cantidad} unidades (ID {id_})")
            else:
                self.historial.append("❌ Stock insuficiente o producto no encontrado")

