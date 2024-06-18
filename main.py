import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

from editor import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joseph's Pixel Art Editor")
        self.resize(1400,1000)

        # custom mouse cursor
        # pixelCursor = QPixmap("pixel-cursor-arrow-png")
        # self.scaled_pixelCursor = pixelCursor.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # create pixel editor object
        self.editor = PixelArtEditor(24,24)

        # wrapper widget with border that allows for scrolling around the canvas
        self.wrapper_widget = QWidget()
        self.wrapper_layout = QVBoxLayout()
        self.wrapper_layout.addStretch(1)
        self.wrapper_layout.addWidget(self.editor, 0, Qt.AlignCenter)
        self.wrapper_layout.addStretch(1)
        self.wrapper_widget.setLayout(self.wrapper_layout)
        self.wrapper_widget.setFixedSize(self.editor.width + 1500, self.editor.height + 1500)  # Large border

        # functionality for being able to scroll -not implemented yet
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.wrapper_widget)
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)

        # tool bar
        self.toolbar = self.addToolBar("Tools")
        self.toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.add_color_buttons()
        
    def add_color_buttons(self):
        colors = [QColor("black"),QColor("white"),QColor("gray"), QColor("red"), QColor("green"), QColor("blue"), QColor("yellow"), QColor("purple")]
        i = 0
        j = 0
        containerWidget = QWidget()
        grid = QGridLayout()
        for color in colors:
            btn = QPushButton()
            btn.setStyleSheet(f"background-color: {color.name()}; border: 2px solid black")
            btn.setFixedSize(20,20)
            btn.clicked.connect(lambda _, col=color: self.setColor(col))
            grid.addWidget(btn, j, i)
            containerWidget.setLayout(grid)
            i+=1
            if i > 2:
                i = 0
                j += 1
        self.toolbar.addWidget(containerWidget)

    def setColor(self, color):
        self.editor.current_color = color

        # change cursor icon
    # def enterEvent(self, event):
    #     # Change the cursor when the mouse enters the view
    #     self.setCursor(QCursor(self.scaled_pixelCursor))
    #     super().enterEvent(event)

    # def leaveEvent(self, event):
    #     # Restore the cursor when the mouse leaves the view
    #     self.unsetCursor()
    #     super().leaveEvent(event)


    
###################### Main #####################

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

