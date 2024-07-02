import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt, QEvent

from editor import *
from dialog import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joseph's Pixel Art Editor")
        self.resize(1200,800)
        self.dialog_counter = 0
        self.tool_buttons = []

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
        self.add_grab_tool()
        self.add_brush_tool()
        self.add_eraser_tool()
        self.add_color_buttons()
        self.add_brushsize_slider()
        self.add_clear_button()
        self.add_menu_buttons()
        self.add_print_button()
        self.add_scale_button()
        self.add_zoom_button()
        self.add_fill_tool()
        self.set_toolbarRight_styles()
        self.set_toolbarLeft_styles()
        self.set_scrollarea_styles()
        


    def fill_white(self, image):
        for x in range(image.width()):
            for y in range(image.height()):
                if image.pixelColor(x, y).alpha() > 0:  # Keep transparency
                    image.setPixelColor(x, y, QColor(255,255,255))
        return QPixmap.fromImage(image)

        # add menu bar with file > new button
    def add_menu_buttons(self):
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")

        self.open_action = self.file_menu.addAction("Open")
        self.open_action.triggered.connect(self.open_image)

        self.new_action = self.file_menu.addAction("New")
        self.new_action.triggered.connect(self.show_dialog)

        self.export_action = self.file_menu.addAction("Export")
        self.export_action.triggered.connect(self.editor.open_save_dialog)

        self.edit_menu = self.menu.addMenu("&Edit")
        self.undo_btn = self.edit_menu.addAction("Undo")
        self.undo_btn.triggered.connect(self.editor.undo)


    def add_color_buttons(self):
        colors = [QColor("black"),QColor("white"),QColor("gray"), QColor("red"), QColor("green"), QColor("blue"), QColor("yellow"), QColor("purple"), QColor("brown")]
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

    def add_brushsize_slider(self):
        self.brush_size = QSlider(Qt.Horizontal)
        self.brush_size.setRange(1,50)
        self.brush_size.setValue(1)
        self.brush_size.valueChanged.connect(self.update_brush)
        self.toolbarLeft.addWidget(self.brush_size)

    def update_brush(self, value):
        if hasattr(self, "editor"):
            self.editor.set_brush_size(value)

    def add_print_button(self):
        self.print_btn = QPushButton("Print")
        self.print_btn.clicked.connect(self.editor.print)
        self.toolbarLeft.addWidget(self.print_btn)

    def add_scale_button(self):
        self.scale_btn = QPushButton("Scale x20")
        self.scale_btn.clicked.connect(self.set_scale)
        self.toolbarLeft.addWidget(self.scale_btn)

    def add_zoom_button(self):
        text = QLabel("         Zoom:")
        container = QWidget()
        zoom_layout = QHBoxLayout(container)
        self.zoom_out_btn = QPushButton("-")
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.clicked.connect(self.editor.zoom_in)
        self.zoom_out_btn.clicked.connect(self.editor.zoom_out)
        zoom_layout.addWidget(self.zoom_out_btn)
        zoom_layout.addWidget(self.zoom_in_btn)
        self.toolbarLeft.addWidget(text)
        self.toolbarLeft.addWidget(container)

    def add_brush_tool(self):
        pixmap = QPixmap("icons/brush.png")
        image = pixmap.toImage()
        fill_image = self.fill_white(image)
        icon = QIcon(fill_image)
        self.brush_btn = QPushButton()
        self.brush_btn.setIcon(icon)
        self.brush_btn.setCheckable(True)
        self.brush_btn.setChecked(True)
        self.brush_btn.clicked.connect(lambda: self.activate_tool(self.brush_btn, self.editor.draw_switch))
        self.brush_btn.setFixedSize(40,40)
        self.toolbarRight.addWidget(self.brush_btn)
        self.tool_buttons.append(self.brush_btn)

    def add_eraser_tool(self):
        pixmap = QPixmap("icons/eraser.png")
        image = pixmap.toImage()
        fill_image = self.fill_white(image)
        icon = QIcon(fill_image)
        self.eraser_btn = QPushButton()
        self.eraser_btn.setIcon(icon)
        self.eraser_btn.setCheckable(True)
        self.eraser_btn.clicked.connect(lambda: self.activate_tool(self.eraser_btn, self.editor.eraser_switch))
        self.eraser_btn.setFixedSize(40,40)
        self.toolbarRight.addWidget(self.eraser_btn)
        self.tool_buttons.append(self.eraser_btn)

    def add_fill_tool(self):
        pixmap = QPixmap("icons/paint-bucket.png")
        image = pixmap.toImage()
        fill_image = self.fill_white(image)
        icon = QIcon(fill_image)
        self.fill_btn = QPushButton()
        self.fill_btn.setIcon(icon)
        self.fill_btn.setCheckable(True)
        self.fill_btn.clicked.connect(lambda: self.activate_tool(self.fill_btn, self.editor.fill_switch))
        self.fill_btn.setFixedSize(40,40)
        self.toolbarRight.addWidget(self.fill_btn)
        self.tool_buttons.append(self.fill_btn)

    def add_grab_tool(self):
        pixmap = QPixmap("icons/grab.png")
        image = pixmap.toImage()
        fill_image = self.fill_white(image)
        icon = QIcon(fill_image)
        self.grab_btn = QPushButton()
        self.grab_btn.setIcon(icon)
        self.grab_btn.setCheckable(True)
        self.grab_btn.clicked.connect(lambda:self.activate_tool(self.grab_btn, self.editor.grab_switch))
        self.grab_btn.setFixedSize(40,40)
        self.toolbarRight.addWidget(self.grab_btn)
        self.tool_buttons.append(self.grab_btn)

    def set_toolbarRight_styles(self):
        self.toolbarRight.setStyleSheet("""
            
            QPushButton {
                background-color: #3c3e42;
                border: 1px solid black;
                padding: 5px;
            }
            QPushButton:checked {
                background-color: #1a5feb;
            }
            QToolBar {
            background-color: #222326;
            }                            
            
        """)

    def set_toolbarLeft_styles(self):
        self.toolbarLeft.setStyleSheet("""
            
            QPushButton {
                background-color: #3c3e42;
                border: 1px solid black;
                padding: 5px;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton:checked {
                background-color: #1a5feb;
            }
            * {
            background-color: #222326;
            }
            QPushbutton:te
        """)

    def set_scrollarea_styles(self):
        self.scroll_area.setStyleSheet("""
            * {
                background-color: grey;
                border: none;
            }
            QScrollBar {
                background-color: #222326;
            } """)

    def setColor(self, color):
        self.editor.current_color = color

    def update_buttons(self):
        self.export_action.triggered.disconnect()
        self.export_action.triggered.connect(self.editor.open_save_dialog)

        self.open_action.triggered.disconnect()
        self.open_action.triggered.connect(self.open_image)

        self.scale_btn.clicked.disconnect()
        self.scale_btn.clicked.connect(self.set_scale)

        self.print_btn.clicked.disconnect()
        self.print_btn.clicked.connect(self.editor.print)

        self.clear_btn.clicked.disconnect()
        self.clear_btn.clicked.connect(self.editor.clear_canvas)
        
        self.brush_btn.clicked.disconnect()
        self.brush_btn.clicked.connect(lambda: self.activate_tool(self.brush_btn, self.editor.draw_switch))

        self.eraser_btn.clicked.disconnect()
        self.eraser_btn.clicked.connect(lambda: self.activate_tool(self.eraser_btn, self.editor.eraser_switch))

        self.fill_btn.clicked.disconnect()
        self.fill_btn.clicked.connect(lambda: self.activate_tool(self.fill_btn, self.editor.fill_switch))

        self.grab_btn.clicked.disconnect()
        self.grab_btn.clicked.connect(lambda: self.activate_tool(self.grab_btn, self.editor.grab_switch))

        self.zoom_in_btn.clicked.disconnect()
        self.zoom_in_btn.clicked.connect(self.editor.zoom_in)

        self.zoom_out_btn.clicked.disconnect()
        self.zoom_out_btn.clicked.connect(self.editor.zoom_out)

        self.undo_btn.triggered.disconnect()
        self.undo_btn.triggered.connect(self.editor.undo)

    def activate_tool(self, button, action):
        # Uncheck all buttons
        for btn in self.tool_buttons:
            if btn is not button:
                btn.setChecked(False)

        # Check the clicked button
        button.setChecked(True)

        # Perform the action associated with the button
        action()

# shows dialog for creating a new canvas
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

    def open_image(self):
        # Open file dialog to select an image
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)")
        
        if file_path:
            # Load the image
            image = QImage(file_path)
            
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % file_path)
                return
            
            # Create a new editor object with the size of the loaded image
            self.editor = PixelArtEditor(image.width(), image.height())
            
            # Set the loaded image on the canvas
            self.editor.image = image
            self.editor.pixmap_item.setPixmap(QPixmap.fromImage(image))
            
            # Set the new editor in the scroll area
            self.scroll_area.setWidget(self.editor)
            self.setCentralWidget(self.scroll_area)
            self.dialog_counter += 1
            if self.dialog_counter > 1:
                self.update_buttons()

    def set_scale(self):
        # Scale the current image by a factor of 20
        scale_factor = 20
        scaled_image = self.editor.image.scaled(
            self.editor.image.width() * scale_factor,
            self.editor.image.height() * scale_factor,
            Qt.KeepAspectRatio,
            Qt.FastTransformation
        )
        
        # Create a new editor object with the size of the scaled image
        self.editor = PixelArtEditor(scaled_image.width(), scaled_image.height())
        
        # Set the scaled image on the new canvas
        self.editor.image = scaled_image
        self.editor.pixmap_item.setPixmap(QPixmap.fromImage(scaled_image))
        
        print("working")
        # Set the new editor in the scroll area
        self.scroll_area.setWidget(self.editor)
        self.setCentralWidget(self.scroll_area)
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

