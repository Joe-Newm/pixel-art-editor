import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

from editor import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joseph's Pixel Art Editor")
        self.resize(1200,800)

        # custom mouse cursor
        # pixelCursor = QPixmap("pixel-cursor-arrow-png")
        # self.scaled_pixelCursor = pixelCursor.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # create pixel editor object
        height = 64
        width = 64
        self.editor = PixelArtEditor(width,height)
        
        # functionality for being able to scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.editor)
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)
        
        # left tool bar for colors
        self.toolbarLeft = self.addToolBar("Colors")
        self.toolbarLeft.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbarLeft)
        self.add_color_buttons()
        self.toolbarLeft.setMovable(False)

        # right tool bar for tools
        self.toolbarRight = self.addToolBar("Tools")
        self.toolbarRight.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.RightToolBarArea, self.toolbarRight)
        
        self.add_export_button()
        self.add_clear_button()

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
        self.toolbarLeft.addWidget(containerWidget)
    
    def add_export_button(self):
        btn = QPushButton("export")
        btn.clicked.connect(self.editor.open_save_dialog)
        self.toolbarLeft.addWidget(btn)

    def add_clear_button(self):
        btn = QPushButton("clear")
        btn.clicked.connect(self.editor.clear_canvas)
        self.toolbarLeft.addWidget(btn)

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

