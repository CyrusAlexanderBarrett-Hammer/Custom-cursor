import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor

class TransparentOverlay(QMainWindow):
    def __init__(self, check_interval=1000, hide_threshold=10, show_threshold=80, delay_before_show=800):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Add Qt.WindowTransparentForInput to the window flags
        self.originalFlags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput
        self.setWindowFlags(self.originalFlags)
        self.setGeometry(QApplication.desktop().screenGeometry())
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.originalFlags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        self.setWindowFlags(self.originalFlags)
        self.setGeometry(QApplication.desktop().screenGeometry())

        # Mouse position
        self.mouse_x = 0
        self.mouse_y = 0

        # Configuration parameters
        self.check_interval = check_interval
        self.hide_threshold = hide_threshold
        self.show_threshold = show_threshold
        self.delay_before_show = delay_before_show

        self.delayTimer = QTimer(self)
        self.delayTimer.setSingleShot(True)
        self.delayTimer.timeout.connect(self.showOverlay)
        
        self.mouseCheckTimer = QTimer(self)
        self.mouseCheckTimer.timeout.connect(self.checkMousePosition)
        self.mouseCheckTimer.start(self.check_interval)

    def checkMousePosition(self):
        self.mouse_x, self.mouse_y = pyautogui.position()  # Update mouse position

        screen_height = pyautogui.size().height
        if self.mouse_y > screen_height - self.hide_threshold:
            if self.delayTimer.isActive():
                self.delayTimer.stop()
            self.hide()
        elif self.mouse_y < screen_height - self.show_threshold and not self.isVisible():
            if not self.delayTimer.isActive():
                self.delayTimer.start(self.delay_before_show)
        self.update()  # Trigger a repaint to update the circle's position

    def showOverlay(self):
        if not self.isVisible():
            self.setWindowFlags(self.originalFlags)
            self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(0, 255, 0, 127)))  # Semi-transparent green for the square
        painter.drawRect(50, 50, 100, 100)  # Draw a green square

        # Draw a red circle at the mouse position
        painter.setBrush(QBrush(QColor(255, 0, 0, 127)))  # Semi-transparent red for the circle
        circle_radius = 20
        painter.drawEllipse(QPoint(self.mouse_x, self.mouse_y), circle_radius, circle_radius)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = TransparentOverlay()
    overlay.showFullScreen()
    sys.exit(app.exec_())