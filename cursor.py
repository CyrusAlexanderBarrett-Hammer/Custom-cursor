# from PIL import Image, ImageFilter, ImageEnhance


# class Samples:
#     base_colour = [232,248,248]

#     glow_source_colour = [(111, 213, 227), (29, 185, 204), (46, 129, 196), (41.4, 116.1, 176.4)]
#     glow_properties = {"iterations": 5, "scale_factor": 1.05, "initial_opacity": 255}
#         # Parameters for the glow effect



# def recolour_base(image, color=(0, 0, 255)):
#     # Open the cursor image
#     if type(image) == str:
#         img = Image.open(image).convert("RGBA")
#     else:
#         img = image
    
#     # Separate the alpha channel and color channels
#     r, g, b, a = img.split()
    
#     # Apply the color effect to the color channels only
#     r = r.point(lambda p: p * color[0] / 255)
#     g = g.point(lambda p: p * color[1] / 255)
#     b = b.point(lambda p: p * color[2] / 255)
    
#     # Re-merge the color channels and alpha channel
#     colored_img = Image.merge("RGBA", (r, g, b, a))

#     return(colored_img)


# def remove_background(image):
#         # Assuming 'image' is your processed image
#     # Check if the image mode is 'RGBA'. If not, convert it.
#     if image.mode != 'RGBA':
#         imgage = image.convert('RGBA')

#     # Replace black background with transparency
#     # This step assumes that you want to convert pure black pixels to transparent ones
#     # Adjust the condition if your image has a different background color
#     data = image.getdata()
#     newData = []
#     for item in data:
#         # Change all pixels that are pure black to transparent
#         if item[0] == 0 and item[1] == 0 and item[2] == 0:
#             newData.append((255, 255, 255, 0))
#         else:
#             newData.append(item)

#     image.putdata(newData)
    
#     return(image)


# def glow(image, properties, colour):
#     iterations, scale_factor, initial_opacity = properties.values()

#     width, height = image.size

#     # Calculate the size of the largest glow layer (which will be the size of our canvas)
#     max_size_increase = scale_factor ** iterations
#     canvas_size = (int(width * max_size_increase), int(height * max_size_increase))

#     # Create a blank image for the canvas with the size of the largest glow layer
#     canvas = Image.new('RGBA', canvas_size, (0, 0, 0, 0))

#     for i in range(iterations, 0, -1):
#         # Apply transformations to create the glow effect (e.g., blur)
#         size_increase = scale_factor ** i
#         new_size = (int(width * size_increase), int(height * size_increase))
#         image = recolour_base(image, colour)
#         glow_layer = image.resize(new_size, Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=i * 2))

#         # Adjust opacity for this layer
#         alpha_layer = Image.new('L', glow_layer.size, color=initial_opacity // i)
#         glow_layer.putalpha(alpha_layer)

#         # Calculate the offset to center this glow layer on the canvas
#         offset_x = (canvas_size[0] - new_size[0]) // 2
#         offset_y = (canvas_size[1] - new_size[1]) // 2
#         offset = (offset_x, offset_y)

#         # Paste the glow layer onto the canvas
#         canvas.paste(glow_layer, offset, glow_layer)

#     # Paste the original image on top of the glow, centered
#     original_offset = ((canvas_size[0] - width) // 2, (canvas_size[1] - height) // 2)
#     canvas.paste(image, original_offset, image)

#     return canvas


# recoulored_image = recolour_base(r"C:\Windows\Cursors\aero_arrow.cur", color=Samples.base_colour)
# pure_image = remove_background(recoulored_image)
# glowed_image = glow(pure_image, Samples.glow_properties, Samples.glow_source_colour[3])

# glowed_image.save(r"C:\Users\Cyrus\Documents\Repositories\Custom-cursor\test.png", "PNG")


# # # Save the image again
# # final_img.save(r"C:\Users\Cyrus\Documents\Repositories\Custom-cursor\customized_cursor_with_transparency_3.png", "PNG")

import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QColor

class TransparentOverlay(QMainWindow):
    def __init__(self, check_interval=100, hide_threshold=10, show_threshold=80, delay_before_show=700):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.originalFlags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        self.setWindowFlags(self.originalFlags)
        self.setGeometry(QApplication.desktop().screenGeometry())

        # Configuration parameters
        self.check_interval = check_interval
        self.hide_threshold = hide_threshold
        self.show_threshold = show_threshold
        self.delay_before_show = delay_before_show

        self.delayTimer = QTimer(self)  # Create a timer for the delay
        self.delayTimer.setSingleShot(True)  # Ensure the timer only triggers once per timeout
        self.delayTimer.timeout.connect(self.showOverlay)  # Connect the timer to the showOverlay method
        
        self.mouseCheckTimer = QTimer(self)  # Timer to check the mouse position
        self.mouseCheckTimer.timeout.connect(self.checkMousePosition)
        self.mouseCheckTimer.start(self.check_interval)  # Start the mouse position check timer

    def checkMousePosition(self):
        screen_height = pyautogui.size().height  # Get the screen height
        y = pyautogui.position().y  # Get the current mouse y-position

        if y > screen_height - self.hide_threshold:  # If near the bottom
            if self.delayTimer.isActive():
                self.delayTimer.stop()
            self.hide()  # Hide the overlay
        elif y < screen_height - self.show_threshold and not self.isVisible():
            # Start the delay timer to show the overlay after a delay
            if not self.delayTimer.isActive():
                self.delayTimer.start(self.delay_before_show)  # Start delay timer

    def showOverlay(self):
        # This method will show the overlay after the delay
        if not self.isVisible():  # Check if the overlay is not visible
            self.setWindowFlags(self.originalFlags)
            self.showFullScreen()  # Show the overlay again

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(0, 255, 0, 127)))  # Semi-transparent green
        painter.drawRect(50, 50, 100, 100)  # Draw a green square

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = TransparentOverlay()
    overlay.showFullScreen()
    sys.exit(app.exec_())