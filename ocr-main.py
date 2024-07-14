import sys
import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QFileDialog
from PIL import Image
import pytesseract
import os
import clipboard

if os.path.exists(r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'):
    tesseract_path = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
    tesseract_path = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else :
    raise FileNotFoundError(f'tesseract.exe is not found')

class ScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Screenshot Text Extractor')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.textEdit = QTextEdit(self)
        self.layout.addWidget(self.textEdit)

        self.captureButton = QPushButton('Capture Screenshot', self)
        self.captureButton.clicked.connect(self.initiate_capture)
        self.layout.addWidget(self.captureButton)

        self.uploadButton = QPushButton('Upload Image', self)
        self.uploadButton.clicked.connect(self.upload_image)
        self.layout.addWidget(self.uploadButton)

        self.copyButton = QPushButton('Copy Text', self)
        self.copyButton.clicked.connect(self.copy_text)
        self.layout.addWidget(self.copyButton)

    def initiate_capture(self):
        self.hide()
        self.snipper = SnippingWidget(self)
        self.snipper.show()

    def process_screenshot(self, screenshot_path):
        text = self.extract_text_from_image(screenshot_path)
        self.textEdit.setText(text)
        os.remove(screenshot_path)
        self.show()

    def upload_image(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if filePath:
            text = self.extract_text_from_image(filePath)
            self.textEdit.setText(text)

    def copy_text(self):
        text = self.textEdit.toPlainText()
        clipboard.copy(text)

    def extract_text_from_image(self, image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text


class SnippingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 3))
        qp.setBrush(QtGui.QBrush(QtCore.Qt.white, 50))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.close()
        self.capture()

    def capture(self):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.parent.show()
        QtCore.QThread.sleep(1)  # To ensure the snipping widget is closed
        screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))

        screenshot_path = 'screenshot.png'
        screenshot.save(screenshot_path)

        self.parent.process_screenshot(screenshot_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ScreenshotApp()
    mainWin.show()
    sys.exit(app.exec_())