import sys
from ui import  Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

def push(ui):
    ui.pushButton.setText('ashdui')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.pushButton.clicked.connect(lambda:push(ui))
    MainWindow.show()

sys.exit(app.exec_())