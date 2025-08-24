from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton

class FormularioVenta(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vender producto")
        self.resize(250, 120)

        layout = QVBoxLayout()

        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Cantidad vendida")
        layout.addWidget(QLabel("Cantidad"))
        layout.addWidget(self.input_cantidad)

        botones = QHBoxLayout()
        self.btn_ok = QPushButton("✅ Confirmar")
        self.btn_cancelar = QPushButton("❌ Cancelar")
        botones.addWidget(self.btn_ok)
        botones.addWidget(self.btn_cancelar)
        layout.addLayout(botones)

        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

    def obtener_cantidad(self):
        try:
            return int(self.input_cantidad.text())
        except ValueError:
            return None
