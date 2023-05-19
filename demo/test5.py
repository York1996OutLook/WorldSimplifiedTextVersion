import sys
from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QVBoxLayout, QApplication


class ScrollArea(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Scroll Area widget contents
        widget = QWidget()
        vbox = QVBoxLayout()
        for i in range(50):
            vbox.addWidget(QLabel(f'Line {i}'))
        widget.setLayout(vbox)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidget(widget)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.setLayout(layout)

        # Window
        self.setWindowTitle('ScrollArea')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScrollArea()
    sys.exit(app.exec_())
