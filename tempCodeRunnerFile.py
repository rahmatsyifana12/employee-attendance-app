def runSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        self.refreshAll()
        print(self.Videocapture_)
        ui.hide()  # hide the main window
        self.outputWindow_()  # Create and open new output window

    def outputWindow_(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = UI_Dialog()
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)
        print("Video Played")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())