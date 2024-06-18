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
        self.image = QImage(width, height, QImage.Format_ARGB32)
        self.current_color = QColor(0, 0, 0)

        # create checker pattern on canvas
        for y in range(height):
            for x in range(width):
                pixel = x + y
                if (pixel % 2 == 0):
                    color = QColor(255, 255, 255)
                else: 
                    color = QColor(200, 200, 200)
                self.image.setPixelColor(x, y, color)

        self.pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(self.pixmap_item)

        self.setRenderHint(QPainter.Antialiasing, False)
        self.setRenderHint(QPainter.SmoothPixmapTransform, False)

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

    def setPixel(self, event):
        print('hi')
        pos = self.mapToScene(event.pos())
        x = int(pos.x())
        y = int(pos.y())
        self.image.setPixelColor(x, y, self.current_color)
        self.pixmap_item.setPixmap(QPixmap.fromImage(self.image))
        
        



