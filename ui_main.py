from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog, QLineEdit, QLabel, QCheckBox,
    QDialog, QDateEdit
)
import pandas as pd
import database
from ui_formulario import FormularioProducto
from ui_vender import FormularioVenta
from PySide6.QtGui import QShortcut, QKeySequence, QColor
from PySide6.QtCore import QDate


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Stock - Almacén")
        self.resize(860, 600)

        layout = QVBoxLayout()

        # Barra búsqueda y filtro
        topbar = QHBoxLayout()
        topbar.addWidget(QLabel("🔎 Buscar:"))
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Código o Nombre...")
        topbar.addWidget(self.input_buscar)
        self.chk_bajo_stock = QCheckBox("Solo bajo stock (≤5)")
        topbar.addWidget(self.chk_bajo_stock)
        layout.addLayout(topbar)

        # Tabla
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Historial
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setMaximumHeight(140)
        layout.addWidget(self.historial)

        # Botones
        botones = QHBoxLayout()
        self.btn_agregar = QPushButton("➕ Agregar (F1)")
        self.btn_editar = QPushButton("✏️ Editar (F3)")
        self.btn_eliminar = QPushButton("🗑 Eliminar (Del)")
        self.btn_importar = QPushButton("📥 Importar Excel")
        self.btn_exportar = QPushButton("📤 Exportar Stock")
        self.btn_vender = QPushButton("🛒 Vender (F2)")
        self.btn_reporte = QPushButton("📊 Reporte ventas")
        self.btn_bajo_stock = QPushButton("🖨 Imprimir bajo stock")

        for b in [self.btn_agregar, self.btn_editar, self.btn_eliminar,
                  self.btn_importar, self.btn_exportar, self.btn_vender,
                  self.btn_reporte, self.btn_bajo_stock]:
            botones.addWidget(b)
        layout.addLayout(botones)
        self.setLayout(layout)

        # Atajos
        QShortcut(QKeySequence("F1"), self, activated=self.abrir_formulario)
        QShortcut(QKeySequence("F2"), self, activated=self.vender_producto)
        QShortcut(QKeySequence("F3"), self, activated=self.editar_producto)
        QShortcut(QKeySequence("Delete"), self, activated=self.eliminar_producto)

        # Inicializar
        self._productos_cache = []
        self.actualizar_tabla()
        self.actualizar_historial()

        # Conexiones
        self.btn_agregar.clicked.connect(self.abrir_formulario)
        self.btn_importar.clicked.connect(self.importar_excel)
        self.btn_exportar.clicked.connect(self.exportar_excel)
        self.btn_editar.clicked.connect(self.editar_producto)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_vender.clicked.connect(self.vender_producto)
        self.input_buscar.textChanged.connect(self.aplicar_filtros)
        self.chk_bajo_stock.toggled.connect(self.aplicar_filtros)
        self.btn_reporte.clicked.connect(self.generar_reporte_ventas)
        self.btn_bajo_stock.clicked.connect(self.imprimir_bajo_stock)

    def _cargar_productos(self):
        self._productos_cache = database.obtener_productos()
        return self._productos_cache

    def actualizar_tabla(self):
        productos = self._cargar_productos()
        self._pintar_tabla(productos)

    def _pintar_tabla(self, productos):
        self.table.setRowCount(len(productos))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Cantidad", "Precio", "Movimientos"])

        for row, prod in enumerate(productos):
            for col, val in enumerate(prod):
                item = QTableWidgetItem(str(val))
                if col == 3:
                    try:
                        cant = int(val)
                        if cant <= 5:
                            item.setForeground(QColor("red"))
                        if cant == 0:
                            item.setForeground(QColor("#777777"))
                    except:
                        pass
                self.table.setItem(row, col, item)

        # ordenar automáticamente por nombre (columna 2)
        self.table.sortItems(2)

    def aplicar_filtros(self):
        texto = self.input_buscar.text().strip().lower()
        solo_bajo = self.chk_bajo_stock.isChecked()

        filtrados = []
        for prod in self._productos_cache:
            _id, codigo, nombre, cantidad, precio, movs = prod
            ok_texto = True
            if texto:
                ok_texto = (texto in str(codigo).lower()) or (texto in str(nombre).lower())

            ok_bajo = True
            if solo_bajo:
                try:
                    ok_bajo = int(cantidad) <= 5
                except:
                    ok_bajo = False

            if ok_texto and ok_bajo:
                filtrados.append(prod)

        self._pintar_tabla(filtrados)

    def actualizar_historial(self):
        movimientos = database.obtener_movimientos()
        self.historial.clear()
        for nombre, cambio, precio, fecha in movimientos:
            try:
                c = int(cambio)
                p = float(precio)
            except:
                c, p = cambio, precio

            if isinstance(c, int):
                if c > 0:
                    etiqueta = "✅ Ingreso"
                    signo = f"+{c}"
                elif c < 0:
                    etiqueta = "🛒 Venta"
                    signo = f"{c}"
                else:
                    etiqueta = "✏️ Editado" if p and float(p) > 0 else "❌ Eliminado"
                    signo = "0"
            else:
                etiqueta = "ℹ️ Movimiento"
                signo = str(c)

            self.historial.append(f"[{fecha}] {etiqueta}: {nombre} ({signo}) ${precio}")

    def abrir_formulario(self):
        dialog = FormularioProducto(self)
        if dialog.exec():
            datos = dialog.obtener_datos()
            try:
                if not datos["codigo"] or not datos["nombre"]:
                    self.historial.append("⚠ Completá Código y Nombre")
                    return
                database.agregar_o_actualizar_producto(
                    datos["codigo"],
                    datos["nombre"],
                    int(datos["cantidad"]),
                    float(datos["precio"])
                )
                self.actualizar_tabla()
                self.actualizar_historial()
                self.aplicar_filtros()
                self.historial.append(f"✅ Ingreso: {datos['nombre']} (+{int(datos['cantidad'])}) ${float(datos['precio'])}")
            except ValueError:
                self.historial.append("⚠ Error: cantidad y precio deben ser números")

    def exportar_excel(self):
        productos = database.obtener_productos()
        df = pd.DataFrame(productos, columns=["ID", "Código", "Nombre", "Cantidad", "Precio", "Movimientos"])
        df.to_excel("stock.xlsx", index=False)
        self.historial.append("✅ Exportado a stock.xlsx")

    def importar_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            try:
                df = pd.read_excel(file_path)
                requeridas = {"Codigo", "Nombre", "Cantidad", "Precio"}
                if not requeridas.issubset(set(df.columns)):
                    self.historial.append(f"⚠ El Excel debe tener columnas: {', '.join(sorted(requeridas))}")
                    return
                for _, row in df.iterrows():
                    database.agregar_o_actualizar_producto(
                        str(row["Codigo"]),
                        str(row["Nombre"]),
                        int(row["Cantidad"]),
                        float(row["Precio"])
                    )
                self.actualizar_tabla()
                self.actualizar_historial()
                self.aplicar_filtros()
                self.historial.append(f"📥 Importado desde {file_path}")
            except Exception as e:
                self.historial.append(f"❌ Error al importar: {e}")

    def editar_producto(self):
        fila = self.table.currentRow()
        if fila < 0:
            self.historial.append("⚠ Selecciona un producto para editar")
            return

        id_ = int(self.table.item(fila, 0).text())
        datos = {
            "codigo": self.table.item(fila, 1).text(),
            "nombre": self.table.item(fila, 2).text(),
            "cantidad": self.table.item(fila, 3).text(),
            "precio": self.table.item(fila, 4).text()
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
                self.aplicar_filtros()
                self.historial.append(f"✏️ Editado: {d['nombre']} (stock={int(d['cantidad'])}, precio=${float(d['precio'])})")
            except ValueError:
                self.historial.append("⚠ Error: cantidad y precio deben ser números")

    def eliminar_producto(self):
        fila = self.table.currentRow()
        if fila < 0:
            self.historial.append("⚠ Selecciona un producto para eliminar")
            return

        id_ = int(self.table.item(fila, 0).text())
        nombre = self.table.item(fila, 2).text()
        database.eliminar_producto(id_)
        self.actualizar_tabla()
        self.actualizar_historial()
        self.aplicar_filtros()
        self.historial.append(f"❌ Eliminado: {nombre}")

    def vender_producto(self):
        fila = self.table.currentRow()
        if fila < 0:
            self.historial.append("⚠ Selecciona un producto para vender")
            return

        id_ = int(self.table.item(fila, 0).text())
        nombre = self.table.item(fila, 2).text()
        stock_actual = int(self.table.item(fila, 3).text())

        dialog = FormularioVenta(self)
        if dialog.exec():
            cantidad = dialog.obtener_cantidad()
            if cantidad is None or cantidad <= 0:
                self.historial.append("⚠ Cantidad inválida")
                return
            if cantidad > stock_actual:
                self.historial.append(f"❌ Stock insuficiente: hay {stock_actual}, intentaste vender {cantidad}")
                return

            ok = database.modificar_stock(id_, -cantidad)
            if ok:
                self.actualizar_tabla()
                self.actualizar_historial()
                self.aplicar_filtros()
                self.historial.append(f"🛒 Vendidas {cantidad} unidades de {nombre} (ID {id_})")
            else:
                self.historial.append("❌ Stock insuficiente o producto no encontrado")

    def generar_reporte_ventas(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Generar reporte de ventas")
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Desde:"))
        date_ini = QDateEdit(QDate.currentDate().addDays(-7))
        date_ini.setCalendarPopup(True)
        vbox.addWidget(date_ini)
        vbox.addWidget(QLabel("Hasta:"))
        date_fin = QDateEdit(QDate.currentDate())
        date_fin.setCalendarPopup(True)
        vbox.addWidget(date_fin)
        btns = QHBoxLayout()
        ok = QPushButton("✅ Generar")
        cancel = QPushButton("❌ Cancelar")
        btns.addWidget(ok); btns.addWidget(cancel)
        vbox.addLayout(btns)
        dlg.setLayout(vbox)
        ok.clicked.connect(dlg.accept)
        cancel.clicked.connect(dlg.reject)

        if dlg.exec():
            fi = date_ini.date().toString("yyyy-MM-dd")
            ff = date_fin.date().toString("yyyy-MM-dd")
            ventas = database.obtener_ventas(fi, ff)
            if not ventas:
                self.historial.append("ℹ️ No se encontraron ventas en el rango")
                return
            df = pd.DataFrame(ventas, columns=["Código", "Nombre", "Cantidad", "Precio", "Fecha"])
            # Total vendido $
            total = sum(abs(v[2]) * v[3] for v in ventas)
            df.loc[len(df.index)] = ["", "TOTAL VENDIDO", "", total, ""]
            df.to_excel("reporte_ventas.xlsx", index=False)
            self.historial.append(f"📊 Reporte generado: reporte_ventas.xlsx ({fi} → {ff})")

    def imprimir_bajo_stock(self):
        productos = [p for p in self._productos_cache if int(p[3]) <= 5]
        if not productos:
            self.historial.append("ℹ️ No hay productos con bajo stock")
            return
        df = pd.DataFrame(productos, columns=["ID", "Código", "Nombre", "Cantidad", "Precio", "Movimientos"])
        df.to_excel("bajo_stock.xlsx", index=False)
        self.historial.append("🖨 Listado bajo stock generado: bajo_stock.xlsx")
