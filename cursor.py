import sys
import ctypes
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor
import win32gui
import win32con

class TransparentOverlay(QMainWindow):
    def __init__(self, check_interval=20, hide_threshold=10, show_threshold=80, delay_before_show=800):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
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

        self.initWinAPI()

    def initWinAPI(self):
        hwnd = self.winId().__int__()  # Retrieve the handle to the window
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

    def checkMousePosition(self):
        self.mouse_x, self.mouse_y = pyautogui.position()

        screen_height = pyautogui.size().height
        if self.mouse_y > screen_height - self.hide_threshold:
            if self.delayTimer.isActive():
                self.delayTimer.stop()
            self.hide()
        elif self.mouse_y < screen_height - self.show_threshold and not self.isVisible():
            if not self.delayTimer.isActive():
                self.delayTimer.start(self.delay_before_show)
        self.update()

    def showOverlay(self):
        if not self.isVisible():
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(0, 255, 0, 127)))
        painter.drawRect(50, 50, 100, 100)
        painter.setBrush(QBrush(QColor(255, 0, 0, 127)))
        circle_radius = 20
        painter.drawEllipse(QPoint(self.mouse_x, self.mouse_y), circle_radius, circle_radius)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = TransparentOverlay()
    overlay.showFullScreen()
    sys.exit(app.exec_())