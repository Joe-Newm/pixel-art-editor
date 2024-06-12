import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

from editor import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joseph's Pixel Art Editor")
        self.resize(1000,1000)

        self.editor = PixelArtEditor(24,24)

        # add canvas in a frame to main window 
        self.frame = QFrame()
        self.frame_layout = QVBoxLayout()
        self.frame_layout.addWidget(self.editor)
        self.frame_layout.setContentsMargins(0, 0, 0, 0) 
        self.frame.setLayout(self.frame_layout)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.frame)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.central_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.central_widget)
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)



###################### Main #####################

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

