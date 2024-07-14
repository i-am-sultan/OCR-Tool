import sys
import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QFileDialog
from PIL import Image
import pytesseract
import os
import clipboard

# Specify the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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
        self.captureButton.clicked.connect(self.capture_screenshot)
        self.layout.addWidget(self.captureButton)

        self.uploadButton = QPushButton('Upload Image', self)
        self.uploadButton.clicked.connect(self.upload_image)
        self.layout.addWidget(self.uploadButton)

        self.copyButton = QPushButton('Copy Text', self)
        self.copyButton.clicked.connect(self.copy_text)
        self.layout.addWidget(self.copyButton)

    def capture_screenshot(self):
        # Delay to allow user to prepare for screenshot
        self.hide()
        self.repaint()
        QtCore.QThread.sleep(2)
        screenshot = pyautogui.screenshot()
        self.show()

        screenshot_path = 'screenshot.png'
        screenshot.save(screenshot_path)

        text = self.extract_text_from_image(screenshot_path)
        self.textEdit.setText(text)
        os.remove(screenshot_path)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ScreenshotApp()
    mainWin.show()
    sys.exit(app.exec_())
