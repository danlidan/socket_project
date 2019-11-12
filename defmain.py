from ui import  Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import socket,sys
if(sys.version[:1] == "3"):
    import _thread as thread

HOST = '10.222.162.87'
PORT = 8998
ADDR =(HOST,PORT)
BUFSIZE = 1024

def push():
    ui.pushButton.setText('ashdui')
    ui.textEdit.setText('sahdiuagsdiuahsiud')

def push2(sock):
    data = ui.textEdit.toPlainText()
    if len(data) > 0:
        try:
            sock.sendall(data.encode('utf-8'))
        except Exception:
            print('error')

def recv(sock):
    try:
        while True:
            recv_data = sock.recv(BUFSIZE).decode('utf-8')
            print(recv_data)
    except Exception:
        thread.exit_thread()

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.pushButton.clicked.connect(lambda:push())
sock = socket.socket()
sock.connect(ADDR)
ui.pushButton_2.clicked.connect(lambda :push2(sock))
thread.start_new_thread(recv, (sock,))
MainWindow.show()
app.exec_()
sock.close()
sys.exit()




