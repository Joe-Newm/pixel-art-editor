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

        # create checker pattern on canvas
        for y in range(height):
            for x in range(width):
                pixel = x + y
                if (pixel % 2 == 0):
                    color = QColor(255, 255, 255)
                else: 
                    color = QColor(200, 200, 200)
                self.image.setPixelColor(x, y, color)

        self.pixelMap = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(self.pixelMap)

        # add scale
        self.scale(self.scaleNum, self.scaleNum)
        
        



