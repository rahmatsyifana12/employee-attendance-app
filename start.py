# This file with main_demo.py contains both face recognition program and GUI
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from main_demo import UIDialog

class UIDialogStart(QDialog):
    def __init__(self):
        super(UIDialogStart, self).__init__()
        loadUi("./start.ui", self)

        self.run_btn.clicked.connect(self.runSlot)

        self.new_window = None
        self.video_capt = None

    @pyqtSlot()
    def runSlot(self):
        self.video_capt = "0"
        print(self.video_capt)
        ui.hide()
        self.outputWindow_()

    def outputWindow_(self):
        self.new_window = UIDialog()
        self.new_window.show()
        self.new_window.startVideo(self.video_capt)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UIDialogStart()
    ui.show()
    sys.exit(app.exec_())