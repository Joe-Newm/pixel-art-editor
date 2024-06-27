import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt, QEvent, QBuffer, QFileInfo
from PIL import Image, ImageFilter
import usb1
from escpos.printer import Dummy
import io

class PixelArtEditor(QGraphicsView):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(-50, -50, width +100, height+100)
        self.drawn_pixels = set()
        self.image = QImage(width, height, QImage.Format_ARGB32)
        self.current_color = QColor(0, 0, 0)
        self.last_directory = ""

        # keep track of which tool is being used
        self.states = ["draw_mode_on", "eraser_mode_on", "fill_mode_on"]
        self.state = self.states[0]

        # create checkerboard pattern pixmap
        self.backgroundPixmap = self.create_checkerboard_pattern(width, height)
        self.background_item = QGraphicsPixmapItem(self.backgroundPixmap)
        self.scene.addItem(self.background_item)

        # pixmap for what i draw on the canvas
        self.image.fill(Qt.transparent)
        self.pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(self.pixmap_item)

        # add scale
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.scale(10,10)

        self.grabGesture(Qt.PinchGesture)
        
    def wheelEvent(self, event):
        if event.modifiers() == Qt.AltModifier:
            zoom_in_factor = 1.1
            zoom_out_factor = 1 / zoom_in_factor
            delta_x = event.angleDelta().x()
            delta_y = event.angleDelta().y()
            if delta_x > 0 or delta_y > 0:
                self.scale(zoom_in_factor, zoom_in_factor)
            else:
                self.scale(zoom_out_factor, zoom_out_factor)  
        else:
            super().wheelEvent(event)

    # adds pinch gesture for zooming in and out
    def gestureEvent(self, event):
        if event.gesture(Qt.PinchGesture):
            self.pinchTriggered(event.gesture(Qt.PinchGesture))
        return super().event(event)
    # determines scale for zooming with pinch
    def pinchTriggered(self, gesture):
        if gesture.changeFlags() & QPinchGesture.ScaleFactorChanged:
            factor = gesture.scaleFactor()
            self.scale(factor, factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
                self.setPixel(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
                self.setPixel(event)
        super().mouseMoveEvent(event)

    def create_checkerboard_pattern(self, width, height):
        size = 4
        pixmap = QPixmap(width, height)
        with QPainter(pixmap) as painter:
            color1 = QColor(240, 240, 240)
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

        # brush tool
        if self.state == "draw_mode_on":
            self.image.setPixelColor(x, y, self.current_color)
            self.drawn_pixels.add((x, y))

        # eraser tool
        elif self.state == "eraser_mode_on":
            self.image.setPixelColor(x,y,QColor(0,0,0,0))
            if (x,y) in self.drawn_pixels:
                self.drawn_pixels.remove((x, y))

        # fill tool
        elif self.state == "fill_mode_on":
            self.flood_fill(x,y,self.current_color)

        self.pixmap_item.setPixmap(QPixmap.fromImage(self.image))


    def flood_fill(self, x, y, new_color):
        target_color = self.image.pixelColor(x, y)
        if target_color == new_color:
            return

        stack = [(x, y)]
        while stack:
            current_x, current_y = stack.pop()
            if self.image.pixelColor(current_x, current_y) == target_color:
                self.image.setPixelColor(current_x, current_y, new_color)
                if current_x > 0:
                    stack.append((current_x - 1, current_y))
                if current_x < self.image.width() - 1:
                    stack.append((current_x + 1, current_y))
                if current_y > 0:
                    stack.append((current_x, current_y - 1))
                if current_y < self.image.height() - 1:
                    stack.append((current_x, current_y + 1))

    def export_canvas(self, file_path, scale_factor=20):
        large_image = self.image.scaled(self.width * scale_factor, self.height * scale_factor, Qt.KeepAspectRatio, Qt.FastTransformation)
        if file_path.endswith(".png"):
            large_image.save(file_path, 'PNG')
        if file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            # Create a new image with a white background
            white_background = QImage(large_image.size(), QImage.Format_RGB32)
            white_background.fill(Qt.white)
            
            # paint image on the white background
            painter = QPainter(white_background)
            painter.drawImage(0, 0, large_image)
            painter.end()
            
            # Save image as JPEG
            white_background.save(file_path, 'JPEG')
            

        

    def clear_canvas(self):
        self.image = QImage(self.width, self.height, QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)
        self.drawn_pixels.clear()  # Clear the drawn pixels set
        self.pixmap_item.setPixmap(QPixmap.fromImage(self.image))
        
    def open_save_dialog(self):
        file_dialog = QFileDialog(self)
        if self.last_directory != "":
            file_dialog.setDirectory(self.last_directory)
        file_path, _ = file_dialog.getSaveFileName(self, "Save Image", "untitled", "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)")
        if file_path:
            self.last_directory = QFileInfo(file_path).path()
            self.export_canvas(file_path)

    def draw_switch(self):
        self.state = self.states[0]
    
    def eraser_switch(self):
        self.state = self.states[1]

    def fill_switch(self):
        self.state = self.states[2]

    # for printing on the receipt printer
    def print(self):
        # Vendor ID and Product ID from your lsusb output
        VENDOR_ID = 0x0416
        PRODUCT_ID = 0x5011

        context = usb1.USBContext()
        handle = None

        for device in context.getDeviceList(skip_on_error=True):
            if device.getVendorID() == VENDOR_ID and device.getProductID() == PRODUCT_ID:
                handle = device.open()
                print(f"Device found: {device}")
                break

        if handle:
            # The interface number found in the lsusb output
            interface_number = 0 
            handle.claimInterface(interface_number)
            
            # generate commands
            dummy_printer = Dummy()

            #scale image
            printer_width = 576
            scaled_image = self.image.scaledToWidth(printer_width, Qt.SmoothTransformation)

            # change qimage to PIL image
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            scaled_image.save(buffer, "PNG")
            pil_image = Image.open(io.BytesIO(buffer.data()))

            # sharpen the image 
            pil_image = pil_image.filter(ImageFilter.SHARPEN) 
            
            # Print the image
            dummy_printer.image(pil_image)
            dummy_printer.text("## Thanks for using Joseph's pixel editor. ##\n")
            dummy_printer.cut()

            # Get raw data
            escpos_data = dummy_printer.output

            # Perform transfer to endpoint
            endpoint_address = 0x03  # Endpoint
            handle.bulkWrite(endpoint_address, escpos_data)
            print("Printed successfully.")
            
            # Release the interface
            handle.releaseInterface(interface_number)
        else:
            print("No USB device found.")

    def event(self, event):
        if event.type() == QEvent.Gesture:
            return self.gestureEvent(event)
        return super().event(event)
        



