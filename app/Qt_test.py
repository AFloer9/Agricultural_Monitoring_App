# Author: Anna Hyer Spring 2023 Class: Intro to Programming

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QWidget, QFormLayout, QApplication, QPushButton, QHBoxLayout
import sys

class textGUIBox(QWidget):
    def __init__(self, parent=None):
        super(). __init__(parent)
        a1 = QLineEdit()
        a1.textChanged.connect(self.textchanged)
        
    def textchanged(self, text):
        print("Changed: " + text)
        
    def enterPress(self):
        print("Enter pressed")

if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    layout = QHBoxLayout()
    button = QPushButton("push me")
    layout.addWidget(button)
    widget.setLayout(layout)
    display = textGUIBox()
    display.resize(200, 500)
    display.move(50, 50)
    display.show()
    widget.resize(200, 500)
    widget.move(50, 50)
    widget.show()
    sys.exit(app.exec_())