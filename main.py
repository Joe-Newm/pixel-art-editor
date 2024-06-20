import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

from editor import *
from dialog import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joseph's Pixel Art Editor")
        self.resize(1200,800)
        self.dialog_counter = 0

        # custom mouse cursor
        # pixelCursor = QPixmap("pixel-cursor-arrow-png")
        # self.scaled_pixelCursor = pixelCursor.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # functionality for being able to scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)
        
        # left tool bar for colors
        self.toolbarLeft = self.addToolBar("Colors")
        self.toolbarLeft.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbarLeft)
        self.toolbarLeft.setMovable(False)
        
        # right tool bar for tools
        self.toolbarRight = self.addToolBar("Tools")
        self.toolbarRight.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.RightToolBarArea, self.toolbarRight)
        self.toolbarRight.setMovable(False)
        
        # add editor and then add buttons to both tool bars
        self.show_dialog()
        self.add_brush_tool()
        self.add_eraser_tool()
        self.add_color_buttons()
        self.add_export_button()
        self.add_clear_button()

        # add menu bar with file > new button
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        new_action = file_menu.addAction("New")
        new_action.triggered.connect(self.show_dialog)
        edit_menu = menu.addMenu("&Edit")
        edit_menu.addAction("Undo")


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
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.editor.open_save_dialog)
        self.toolbarLeft.addWidget(self.export_btn)

    def add_clear_button(self):
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.editor.clear_canvas)
        self.toolbarLeft.addWidget(self.clear_btn)

    def add_brush_tool(self):
        self.brush_btn = QPushButton("B")
        self.brush_btn.setFixedSize(40,40)
        self.brush_btn.clicked.connect(self.editor.draw_switch)
        self.toolbarRight.addWidget(self.brush_btn)

    def add_eraser_tool(self):
        self.eraser_btn = QPushButton("E")
        self.eraser_btn.setFixedSize(40,40)
        self.eraser_btn.clicked.connect(self.editor.eraser_switch)
        self.toolbarRight.addWidget(self.eraser_btn)

    def setColor(self, color):
        self.editor.current_color = color

    def update_buttons(self):
        self.export_btn.clicked.disconnect()
        self.export_btn.clicked.connect(self.editor.open_save_dialog)

        self.clear_btn.clicked.disconnect()
        self.clear_btn.clicked.connect(self.editor.clear_canvas)
        
        self.brush_btn.clicked.disconnect()
        self.brush_btn.clicked.connect(self.editor.draw_switch)

        self.eraser_btn.clicked.disconnect()
        self.eraser_btn.clicked.connect(self.editor.eraser_switch)

    def show_dialog(self):
        dialog = InputDialog()
        if dialog.exec():
            input1, input2 = dialog.getInputs()
            self.editor = PixelArtEditor(int(input1), int(input2))
            self.scroll_area.setWidget(self.editor)
            self.setCentralWidget(self.scroll_area)
            self.dialog_counter += 1
            if self.dialog_counter > 1:
                self.update_buttons()

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

