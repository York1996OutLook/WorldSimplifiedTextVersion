from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QMessageBox,QPushButton


class YesNoDialog(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.yes_button = QPushButton('Yes')
        self.yes_button.clicked.connect(self.on_yes_clicked)
        layout.addWidget(self.yes_button, 0, 0)

        self.no_button = QPushButton('No')
        self.no_button.clicked.connect(self.on_no_clicked)
        layout.addWidget(self.no_button, 0, 1)

        self.setLayout(layout)
        self.reply=None
    def on_yes_clicked(self):
        self.reply = QMessageBox.Yes
        self.close()

    def on_no_clicked(self):
        self.reply = QMessageBox.No
        self.close()


dialog = YesNoDialog()
dialog.exec_()
print(dialog.reply)
