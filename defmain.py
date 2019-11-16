from ui import  Ui_MainWindow
from login_ui import  Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5.QtCore import *
import socket,sys
if(sys.version[:1] == "3"):
    import _thread as thread

#全局变量定义区
HOST = '172.100.96.163'
PORT = 8998
ADDR =(HOST,PORT)
BUFSIZE = 1024
LOGGED_IN = False
ID = ''
NICK = ''

#以下为各种客户端操作的协议
#登录操作
def login_in():
    id = ui_login.lineEdit.text()
    password = ui_login.lineEdit_2.text()
    if(len(id) == 0 or len(id) > 30 or len(password) == 0 or len(password) > 30):
        ui_login.label_state.setText('请输入合法的用户名和密码！')
    else:
        data = '||'.join(['req_login', id, password])
        sock.sendall(data.encode('utf-8'))

#注册操作
def sign_in():
    id = ui_login.lineEdit.text()
    password = ui_login.lineEdit_2.text()
    nick = ui_login.lineEdit_3.text()
    password2 = ui_login.lineEdit_4.text()
    if(len(id) == 0 or len(id) > 30 or len(password) == 0 or len(password) > 30 or len(nick) == 0 or len(nick) > 30 or len(password2) == 0 or len(password2) > 30):
        ui_login.label_state.setText('部分内容长度过长或未填！')
    elif(password2 != password):
        ui_login.label_state.setText('两次输入密码不一致！')
    else:
        data = '||'.join(['req_sign', id, password, nick])
        sock.sendall(data.encode('utf-8'))

#刷新聊天列表
def refresh_list():
    data = '||'.join(['req_refresh_list'])
    sock.sendall(data.encode('utf-8'))

#接受服务器数据的线程类
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

#以下为处理服务器数据的协议
def ack_login(params):
    ret = params[1]
    if(ret == 'ok'):
        global ID
        ID = params[2]
        global NICK
        NICK = params[3]
        global LOGGED_IN
        LOGGED_IN = True
        app1.closeAllWindows()
    else:
        ui_login.label_state.setText('登录失败！用户名或密码错误')

def ack_sign(params):
    ret = params[1]
    if(ret == 'ok'):
        ui_login.label_state.setText('注册成功！请牢记您的用户名和密码')
    else:
        ui_login.label_state.setText('注册失败！该用户名已被注册')

#处理服务器发来数据的协议
def handle_recv(s):
    params = s.split('||')
    switcher = {
        'ack_login': ack_login,
        'ack_sign': ack_sign,
    }
    func = switcher.get(params[0], lambda: "nothing")
    return func(params)

#开启程序时连接服务器
sock = socket.socket()
try:
    sock.connect(ADDR)
except Exception:
    print("服务器连接失败！")
    sys.exit()

#从服务器接受并处理数据的线程
recv_thread = My_Recv_Thread()
recv_thread._signal.connect(handle_recv)
recv_thread.start()

#登录界面ui
app1 = QApplication(sys.argv)
MainWindow_login = QMainWindow()
ui_login = Ui_Form()
ui_login.setupUi(MainWindow_login)
ui_login.login_button.clicked.connect(lambda :login_in())
ui_login.sign_button.clicked.connect(lambda :sign_in())
MainWindow_login.setWindowTitle('登录')
MainWindow_login.show()
app1.exec_()
if(LOGGED_IN == False):
    sock.close()
    sys.exit()

#主界面ui
app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.setWindowTitle('欢迎使用QQ乞丐版')
MainWindow.show()
ui.label_welcome.setText('欢迎！%s'%NICK)
refresh_list()
app.exec_()
sock.close()
sys.exit()