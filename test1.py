import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSvgWidgets import *
from PySide6.QtSvg import *


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)

        self.setWindowTitle("WeatherReport")


        self.bg = QFrame()
        self.bg.setStyleSheet("background-color: lightblue")
        self.bg_layout = QVBoxLayout(self.bg)



        self.bg_layout.addWidget(QLabel('Обед'))


        #SVG Виджеты
        clouds = "assets/Clouds.svg"
        rain = "assets/rain.svg"
        self.get_size = QSvgRenderer(clouds)
        self.svg_widget = QSvgWidget(clouds)
        self.svg_widget.setFixedSize(200,200)


        self.bg_layout.addWidget(self.svg_widget)

        self.setCentralWidget(self.bg)
        self.show()


if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())