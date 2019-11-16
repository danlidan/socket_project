from ui import  Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import *
import socket,sys
if(sys.version[:1] == "3"):
    import _thread as thread

HOST = '172.100.96.163'
PORT = 8998
ADDR =(HOST,PORT)
BUFSIZE = 1024

class My_Recv_Thread(QThread):
    _signal = pyqtSignal(str)
    def __init__(self):
        super(My_Recv_Thread, self).__init__()
    def run(self):
        try:
            while True:
                recv_data = sock.recv(BUFSIZE).decode('utf-8')
                self._signal.emit(recv_data)
        except Exception:
            print("QThread error!")

def handle_recv(s):
    ui.textEdit.setText(s)


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

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.pushButton.clicked.connect(lambda:push())
sock = socket.socket()
sock.connect(ADDR)
ui.pushButton_2.clicked.connect(lambda :push2(sock))

recv_thread = My_Recv_Thread()
recv_thread._signal.connect(handle_recv)
recv_thread.start()

MainWindow.show()
app.exec_()
sock.close()
sys.exit()




