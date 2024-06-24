import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New Canvas")

        layout = QFormLayout()

        self.input1 = QLineEdit("64")
        self.input2 = QLineEdit("64")

        layout.addRow("Width: ", self.input1)
        layout.addRow("Height: ", self.input2)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def getInputs(self):
        return self.input1.text(), self.input2.text()