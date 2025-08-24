from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
import database

class FormularioProducto(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar producto")
        self.resize(300, 150)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.input_nombre = QLineEdit()
        self.input_cantidad = QLineEdit()
        self.input_precio = QLineEdit()

        form.addRow("Nombre:", self.input_nombre)
        form.addRow("Cantidad:", self.input_cantidad)
        form.addRow("Precio:", self.input_precio)

        layout.addLayout(form)
        self.btn_guardar = QPushButton("Guardar")
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)
        self.btn_guardar.clicked.connect(self.guardar)

    def guardar(self):
        try:
            nombre = self.input_nombre.text().strip()
            cantidad = int(self.input_cantidad.text())
            precio = float(self.input_precio.text())

            if not nombre:
                QMessageBox.warning(self, "Error", "El nombre no puede estar vacío")
                return

            database.agregar_o_actualizar_producto(nombre, cantidad, precio)
            QMessageBox.information(self, "Éxito", "Producto registrado correctamente ✅")
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Error", "Cantidad y precio deben ser números")
