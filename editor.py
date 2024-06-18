import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

class PixelArtEditor(QGraphicsView):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.scaleNum = 20
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.drawn_pixels = set()
        self.image = QImage(width, height, QImage.Format_ARGB32)
        self.current_color = QColor(0, 0, 0)

        # create checkerboard pattern pixmap
        self.backgroundPixmap = self.create_checkerboard_pattern(width, height)
        self.background_item = QGraphicsPixmapItem(self.backgroundPixmap)
        self.scene.addItem(self.background_item)


        # pixmap for what i draw on the canvas
        self.image.fill(Qt.transparent)
        self.pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(self.pixmap_item)

        

        # add scale
        self.scale(self.scaleNum, self.scaleNum)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
                self.setPixel(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
                self.setPixel(event)
        super().mouseMoveEvent(event)

    def create_checkerboard_pattern(self, width, height):
        size = 10  # Size of the checker squares
        pixmap = QPixmap(width, height)
        with QPainter(pixmap) as painter:
            color1 = QColor(255, 255, 255)
            color2 = QColor(200, 200, 200)

            for y in range(0, height, size):
                for x in range(0, width, size):
                    if (x // size + y // size) % 2 == 0:
                        painter.fillRect(x, y, size, size, color1)
                    else:
                        painter.fillRect(x, y, size, size, color2)
        return pixmap

    def setPixel(self, event):
        pos = self.mapToScene(event.pos())
        x = int(pos.x())
        y = int(pos.y())
        self.image.setPixelColor(x, y, self.current_color)
        self.drawn_pixels.add((x, y))
        self.pixmap_item.setPixmap(QPixmap.fromImage(self.image))

    def export_canvas(self, file_path, scale_factor=20):
        large_image = self.image.scaled(self.width * scale_factor, self.height * scale_factor, Qt.KeepAspectRatio, Qt.FastTransformation)
        large_image.save(file_path, 'PNG')

    def clear_canvas(self):
        self.image = QImage(self.width, self.height, QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)
        self.drawn_pixels.clear()  # Clear the drawn pixels set
        self.pixmap_item.setPixmap(QPixmap.fromImage(self.image))
        
    def open_save_dialog(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;All Files (*)")
        if file_path:
            self.export_canvas(file_path)
        



