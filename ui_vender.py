from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton
from PySide6.QtGui import QIntValidator

class FormularioVenta(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vender producto")
        self.resize(260, 130)

        layout = QVBoxLayout()

        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Cantidad vendida")
        self.input_cantidad.setValidator(QIntValidator(1, 10**9, self))
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
            val = int(self.input_cantidad.text())
            return val if val >= 1 else None
        except ValueError:
            return None
