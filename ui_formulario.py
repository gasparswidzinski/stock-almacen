from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class FormularioProducto(QDialog):
    def __init__(self, parent=None, codigo=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar producto")
        self.resize(300, 200)

        layout = QVBoxLayout()

        # Código (opcional, solo lectura si lo pasás)
        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Código (opcional)")
        if codigo is not None:
            self.input_codigo.setText(str(codigo))   # 🔹 corrección: siempre string
            self.input_codigo.setReadOnly(True)
        layout.addWidget(QLabel("Código"))
        layout.addWidget(self.input_codigo)

        # Nombre
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Yerba")
        layout.addWidget(QLabel("Nombre"))
        layout.addWidget(self.input_nombre)

        # Cantidad
        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Ej: 10")
        layout.addWidget(QLabel("Cantidad"))
        layout.addWidget(self.input_cantidad)

        # Precio
        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Ej: 1500.50")
        layout.addWidget(QLabel("Precio"))
        layout.addWidget(self.input_precio)

        # Botón confirmar
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

    def obtener_datos(self):
        return {
            "codigo": self.input_codigo.text(),
            "nombre": self.input_nombre.text(),
            "cantidad": self.input_cantidad.text(),
            "precio": self.input_precio.text()
        }
