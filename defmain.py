import sys
import pymysql
from ui import  Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

def push(ui):
    ui.pushButton.setText('ashdui')

conn = pymysql.connect(user = 'root', password = '123', database = 'database_project1', charset = 'utf8')
cursor = conn.cursor()

def push2():
    query = ('select * from books;')
    cursor.execute(query)
    for(book_id, book_name, author, publisher, num) in cursor:
        print(book_id, book_name, author, publisher, num)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.pushButton.clicked.connect(lambda:push(ui))
    ui.pushButton_2.clicked.connect(lambda:push2())
    MainWindow.show()

sys.exit(app.exec_())