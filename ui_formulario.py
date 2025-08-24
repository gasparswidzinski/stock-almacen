from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class FormularioProducto(QDialog):
    def __init__(self, parent=None, datos=None):
        super().__init__(parent)
        self.setWindowTitle("Producto")
        self.resize(300, 200)

        layout = QVBoxLayout()

        # Código
        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Código o escanear con lector")
        layout.addWidget(QLabel("Código"))
        layout.addWidget(self.input_codigo)

        # Nombre
        self.input_nombre = QLineEdit()
        layout.addWidget(QLabel("Nombre"))
        layout.addWidget(self.input_nombre)

        # Cantidad
        self.input_cantidad = QLineEdit()
        layout.addWidget(QLabel("Cantidad"))
        layout.addWidget(self.input_cantidad)

        # Precio
        self.input_precio = QLineEdit()
        layout.addWidget(QLabel("Precio"))
        layout.addWidget(self.input_precio)

        # Botones
        botones = QHBoxLayout()
        self.btn_guardar = QPushButton("✅ Guardar")
        self.btn_cancelar = QPushButton("❌ Cancelar")
        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_cancelar)
        layout.addLayout(botones)

        self.setLayout(layout)

        # Conexiones
        self.btn_guardar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

        # Si se pasan datos → cargar en el formulario (para edición)
        if datos:
            self.input_codigo.setText(str(datos.get("codigo", "")))
            self.input_nombre.setText(datos.get("nombre", ""))
            self.input_cantidad.setText(str(datos.get("cantidad", "")))
            self.input_precio.setText(str(datos.get("precio", "")))

    def obtener_datos(self):
        return {
            "codigo": self.input_codigo.text(),
            "nombre": self.input_nombre.text(),
            "cantidad": self.input_cantidad.text(),
            "precio": self.input_precio.text()
        }
