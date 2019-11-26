from PyQt5.QtGui import QColor
from ui import  Ui_MainWindow
from login_ui import  Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QLineEdit, QDialog, QGroupBox, QPushButton, \
    QVBoxLayout, QListWidgetItem
from PyQt5.QtCore import *
import socket,sys
import time
if(sys.version[:1] == "3"):
    import _thread as thread

#全局变量定义区
HOST = '10.222.201.44'
PORT = 8998
ADDR =(HOST,PORT)
BUFSIZE = 8192
LOGGED_IN = False   #是否已登录
ID = ''
NICK = ''
CUR_CHAT = ('聊天大厅', '0')
CUR_PYQ = ('', '')
FIRST_LOG = True    #是否刚登录
CHAT_BUFF = {}  #聊天记录的缓存区 id : ((text, time, sender_id, sender_nick),()...),id当前聊天的id，‘0’为聊天大厅
LAST_SEND_TIME = time.time()
LAST_RECORD_TIME = time.time()
LAST_PYQ_SEND_TIME = time.time()
LAST_GOOD_TIME = time.time()
ID_LEN = 6
MAX_PASS_LEN = 15
MIN_PASS_LEN = 6
MAX_NICK_LEN = 10

#以下为各种客户端操作的协议
#登录操作
def login_in():
    id = ui_login.lineEdit.text()
    password = ui_login.lineEdit_2.text()
    if(len(id) != ID_LEN  or len(password) < MIN_PASS_LEN or len(password) > MAX_PASS_LEN or id.isdigit() == False):
        ui_login.label_state.setText('请输入合法的用户名和密码！')
    else:
        data = '||'.join(['req_login', id, password])
        sock.sendall(data.encode('utf-8'))

#是否合法
def is_legal_text(s):
    if len(s) == 0:
        return False
    if s.find(' ') != -1 or s.find('&&') != -1 or s.find('**') != -1 or s.find('||') != -1 or s.find('^^') != -1:
        return False
    if s.find('#') != -1 or s.find('|') != -1:
        return False
    return True

#注册操作
def sign_in():
    id = ui_login.lineEdit.text()
    password = ui_login.lineEdit_2.text()
    nick = ui_login.lineEdit_3.text()
    password2 = ui_login.lineEdit_4.text()
    if(len(id) != ID_LEN or len(password) < MIN_PASS_LEN or len(password) > MAX_PASS_LEN or len(nick) == 0 or len(nick) > MAX_NICK_LEN):
        ui_login.label_state.setText('部分内容长度错误！')
    elif(id.isdigit() == False):
        ui_login.label_state.setText("用户名必须是%s位数字！"%ID_LEN)
    elif(not is_legal_text(nick)):
        ui_login.label_state.setText("昵称包含非法字符！('|' or '#' or ' ')")
    elif(id == '0' or nick == '聊天大厅'):
        ui_login.label_state.setText('用户名和昵称违法！')
    elif(password2 != password):
        ui_login.label_state.setText('两次输入密码不一致！')
    else:
        data = '||'.join(['req_sign', id, password, nick])
        sock.sendall(data.encode('utf-8'))

#刷新聊天列表
def refresh_list():
    data = '||'.join(['req_refresh_list'])
    sock.sendall(data.encode('utf-8'))

#修改昵称操作
def change_nick():
    new_name = ui.lineEdit_nick.text()
    if(not is_legal_text(new_name)):
        ui.label_change.setText('昵称违法！')
    elif(new_name == '聊天大厅'):
        ui.label_change.setText('昵称不能为聊天大厅！')
    else:
        data = '||'.join(['req_change_nick', ID, new_name])
        sock.sendall(data.encode('utf-8'))

def acquire_more_chatrecord(id_other):
    data = '||'.join(['req_acquire_more_chatrecord', ID, id_other])
    sock.sendall(data.encode('utf-8'))

#获取聊天记录
def acquire_chatrecord(id_other):
    data = '||'.join(['req_acquire_chatrecord', ID, id_other])
    sock.sendall(data.encode('utf-8'))

#发送消息
def send_text(id_other, text):
    data = '||'.join(['req_send_text', ID, id_other, text])
    sock.sendall(data.encode('utf-8'))

#发送按钮
def send_clicked():
    ui.pushButton_send.setText('发送')
    text = ui.textEdit_input.toPlainText()
    if(len(text) == 0):
        return
    if(text.find('||') != -1):
        ui.pushButton_send.setText('内容违法！')
        return
    curtime = time.time()
    global  LAST_SEND_TIME
    if(curtime - LAST_SEND_TIME < 1):
        ui.pushButton_send.setText('发送过快！')
        return
    LAST_SEND_TIME = curtime
    id_other = CUR_CHAT[1]
    send_text(id_other, text)
    ui.textEdit_input.clear()

def record_clicked():
    ui.pushButton_record.setText('显示更多记录')
    cur_time = time.time()
    global  LAST_RECORD_TIME
    if(cur_time - LAST_RECORD_TIME < 3):
        ui.pushButton_record.setText('点的太快')
        return
    LAST_RECORD_TIME = cur_time
    id_other = CUR_CHAT[1]
    acquire_more_chatrecord(id_other)

#接收到消息后未点开时该列变色
def set_color(id):
    if(id == '0'):
        ui.listWidget.item(0).setBackground(QColor('pink'))
    else:
        rows = ui.listWidget.count()
        for i in range(1, rows):
            text = ui.listWidget.item(i).text()
            params = text.split('  ')
            if params[1] == id:
                ui.listWidget.item(i).setBackground(QColor('pink'))
                return


#请求聊天记录
def acquire_chatrecord(id_other):
    data = "||".join(['req_acquire_chatrecord', ID, id_other])
    sock.sendall(data.encode('utf-8'))

#刷新聊天界面
def refresh_chat(id_other):
    ui.textEdit_chat.clear()
    if not id_other in CHAT_BUFF:
        acquire_chatrecord(id_other)
    else:
        content = CHAT_BUFF[id_other]
        for text, time, sender_id, sender_nick in content:
            ui.textEdit_chat.append("%s(%s) %s:" % (sender_nick, sender_id, time))
            ui.textEdit_chat.append("   %s\n" % text)

#切换聊天
def switch_chat():
    item = ui.listWidget.currentItem()
    item.setBackground(QColor('white'))
    params = item.text().split('  ')
    nick = params[0]
    if(nick == '聊天大厅'):
        id = '0'
    else:
        id = params[1]
    global CUR_CHAT
    CUR_CHAT = (nick, id)
    ui.label_curchat.setText('当前聊天：%s（%s）'%(nick, id))
    refresh_chat(id)

# comments = [[nick, context],[nick, context]...]
def pyq_addpyq(nick, id, send_time, counter, context, comments):
    newitem = QListWidgetItem()
    text = "%s %s %s\n" \
           "赞: %d\n" \
           "\t%s\n"%(nick, id, send_time, counter, context)
    if len(comments) > 0 and len(comments[0]) > 1:
        for nick, context in comments:
            text = text + "      %s : %s\n"%(nick, context)
    newitem.setText(text)
    ui.listWidget_pyq.insertItem(0, newitem)

def pyq_good():
    ui.pushButton_cool.setText('赞！')
    curitem = ui.listWidget_pyq.currentItem()
    if curitem == None or ui.listWidget_pyq.count() == 0:
        ui.pushButton_cool.setText('点赞失败')
        return

    curtime = time.time()
    global LAST_GOOD_TIME
    if curtime - LAST_GOOD_TIME < 1:
        ui.pushButton_cool.setText('点赞过快')
        return
    LAST_GOOD_TIME = curtime

    text = curitem.text()
    params = text.split('\n')

    params_1 = params[1].split(' ')
    params_user = params[0].split(' ')
    sender_id = params_user[1]
    send_time = params_user[2] + ' ' + params_user[3]
    data = '||'.join(['req_pyq_good', sender_id, send_time])
    sock.sendall(data.encode('utf-8'))

    #客户端点赞数+1
    counter = int(params_1[1]) + 1
    params[1] = "赞: %d"%counter
    text = '\n'.join(params)
    curitem.setText(text)

#发送一条朋友圈
def pyq_send():
    ui.pushButton_sendpyq.setText('发送动态')
    text = ui.textEdit_pyqinput.toPlainText()
    ui.textEdit_pyqinput.clear()
    if(len(text) == 0):
        return
    if(not is_legal_text(text)):
        ui.pushButton_sendpyq.setText('内容违法')
        return
    global LAST_PYQ_SEND_TIME
    cur_time = time.time()
    if cur_time - LAST_PYQ_SEND_TIME < 3:
        ui.pushButton_sendpyq.setText('发送过快')
        return
    LAST_PYQ_SEND_TIME = cur_time
    cur_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
    if CUR_PYQ[1] == '0' or CUR_PYQ[1] == ID:
        pyq_addpyq(NICK, ID, cur_time_str, 0, text, [])
    data = '||'.join(['req_send_pyq', ID, cur_time_str, text])
    sock.sendall(data.encode('utf-8'))

#发送一条评论
def pyq_comment():
    ui.pushButton_comment.setText('评论')
    curitem = ui.listWidget_pyq.currentItem()
    if ui.listWidget_pyq.count() == 0 or curitem == None:
        ui.pushButton_comment.setText('评论失败')
        return
    text = ui.textEdit_pyqinput.toPlainText()
    ui.textEdit_pyqinput.clear()
    if (len(text) == 0):
        return
    if not is_legal_text(text):
        ui.pushButton_comment.setText('内容违法')
        return
    global LAST_PYQ_SEND_TIME
    cur_time = time.time()
    if cur_time - LAST_PYQ_SEND_TIME < 3:
        ui.pushButton_comment.setText('评论过快')
        return
    LAST_PYQ_SEND_TIME = cur_time

    #获取该评论的信息
    item_content = curitem.text()
    params = item_content.split('\n')
    params_sender = params[0].split(' ')
    sender_id = params_sender[1]
    send_time = params_sender[2] + ' ' + params_sender[3]

    data = '||'.join(['req_comment_pyq', sender_id, send_time, ID, text])
    sock.sendall(data.encode('utf-8'))
    #更新该项
    item_content = item_content + '      %s : %s\n'%(NICK, text)
    curitem.setText(item_content)

#刷新朋友圈
def acquire_pyq():
    item = ui.listWidget.currentItem()
    params = item.text().split('  ')
    nick = params[0]
    if (nick == '聊天大厅'):
        id = '0'
    else:
        id = params[1]
    global  CUR_PYQ
    CUR_PYQ = (nick, id)
    ui.label_curpyq.setText('当前朋友圈：%s(%s)'%(nick, id))
    data = '||'.join(['req_acquire_pyq', id])
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

#一下是每10秒请求刷新一次列表的线程类
class My_Timer_Thread(QThread):
    _signal = pyqtSignal(str)
    def __init__(self):
        super(My_Timer_Thread, self).__init__()
    def run(self):
        try:
            while True:
                time.sleep(10)
                self._signal.emit('1')
        except Exception:
            print("Timer error!")

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
        ui_login.label_state.setText('登录失败！用户名或密码错误或已被登陆')

def ack_sign(params):
    ret = params[1]
    if(ret == 'ok'):
        ui_login.label_state.setText('注册成功！请牢记您的用户名和密码')
    else:
        ui_login.label_state.setText('注册失败！该用户名已被注册')

def ack_refresh_list(params):
    ui.listWidget.clear()
    ui.listWidget.addItem("聊天大厅")
    for s in params[1:]:
        users = s.split('##')
        #users: id, nick, is_online
        id = users[0]
        nick = users[1]
        is_online = users[2]
        if(is_online == 'yes'):
            ui.listWidget.addItem("%s  %s  在线"%(nick, id))
        else:
            ui.listWidget.addItem("%s  %s  离线"%(nick, id))
    global FIRST_LOG
    if(FIRST_LOG == True):
        FIRST_LOG = False
        ui.listWidget.setCurrentRow(0)

def ack_change_nick(params):
    new_nick = params[1]
    ui.label_change.setText('修改成功！')
    ui.label_welcome.setText('欢迎！%s（%s）'%(new_nick, ID))
    global NICK
    NICK = new_nick
    refresh_list()

# params = sender_id, sender_nick, recver_id, text, time
#聊天记录的缓存区 id : ((text, time, sender_id, sender_nick),()...),id当前聊天的id，‘0’为聊天大厅
def ack_send_text(params):
    sender_id = params[1]
    sender_nick = params[2]
    recver_id = params[3]
    text = params[4]
    time = params[5]
    global CHAT_BUFF
    if not recver_id in CHAT_BUFF:
        CHAT_BUFF[recver_id] = []
    if not sender_id in CHAT_BUFF:
        CHAT_BUFF[sender_id] = []
    if(recver_id == '0'): #聊天大厅
        CHAT_BUFF[recver_id].append([text, time, sender_id, sender_nick])
        if(CUR_CHAT[1] == recver_id):
            ui.textEdit_chat.append("%s(%s) %s:"%(sender_nick, sender_id, time))
            ui.textEdit_chat.append("   %s\n"%text)
        else:
            set_color('0')
    elif(sender_id == ID):
        CHAT_BUFF[recver_id].append([text, time, sender_id, sender_nick])
        if (CUR_CHAT[1] == recver_id):
            ui.textEdit_chat.append("%s(%s) %s:" % (sender_nick, sender_id, time))
            ui.textEdit_chat.append("   %s\n" % text)
        else:
            set_color(recver_id)
    else:
        CHAT_BUFF[sender_id].append([text, time, sender_id, sender_nick])
        if (CUR_CHAT[1] == sender_id):
            ui.textEdit_chat.append("%s(%s) %s:" % (sender_nick, sender_id, time))
            ui.textEdit_chat.append("   %s\n" % text)
        else:
            set_color(sender_id)

#获取聊天记录
#records: sender, sendernick, time, text
#聊天记录的缓存区 id : ((text, time, sender_id, sender_nick),()...),id当前聊天的id，‘0’为聊天大厅
def ack_acquire_chatrecord(params):
    recver_id = params[1]
    global CHAT_BUFF
    CHAT_BUFF[recver_id] = []
    l = len(params)
    if l > 2 and params[2] != '':
        for s in params[2:]:
            records = s.split('##')
            sender_id = records[0]
            sender_nick = records[1]
            time = records[2]
            text = records[3]
            CHAT_BUFF[recver_id].append([text, time, sender_id, sender_nick])
    if CUR_CHAT[1] == recver_id:
        refresh_chat(recver_id)

#刷新朋友圈界面
def ack_acquire_pyq(params):
    ui.listWidget_pyq.clear()
    if params[1] == '':
        return
    for pyq_one in params[1:]:
        params_1 = pyq_one.split('^^')
        nick = params_1[0]
        sender_id = params_1[1]
        send_time = params_1[2]
        counter = int(params_1[3])
        content = params_1[4]
        comments = []
        comments_str = params_1[5].split('**')
        for s in comments_str:
            comments.append(s.split('&&'))
        pyq_addpyq(nick, sender_id, send_time, counter, content, comments)

#处理服务器发来数据的协议
def handle_recv(s):
    params = s.split('||')
    switcher = {
        'ack_login': ack_login,
        'ack_sign': ack_sign,
        'ack_refresh_list': ack_refresh_list,
        'ack_change_nick': ack_change_nick,
        'ack_send_text': ack_send_text,
        'ack_acquire_chatrecord': ack_acquire_chatrecord,
        'ack_acquire_pyq': ack_acquire_pyq,
    }
    func = switcher.get(params[0], lambda: "nothing")
    return func(params)

def test_thread(s):
    refresh_list()

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
ui_login.lineEdit_2.setEchoMode(QLineEdit.Password)
ui_login.lineEdit_4.setEchoMode(QLineEdit.Password)
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
ui.pushButton_nick.clicked.connect(lambda :change_nick())
ui.listWidget.itemClicked.connect(lambda :switch_chat())
ui.listWidget.itemDoubleClicked.connect(lambda :acquire_pyq())
ui.pushButton_send.clicked.connect(lambda :send_clicked())
ui.pushButton_record.clicked.connect(lambda :record_clicked())
ui.pushButton_cool.clicked.connect(lambda :pyq_good())
ui.pushButton_sendpyq.clicked.connect(lambda :pyq_send())
ui.pushButton_comment.clicked.connect(lambda :pyq_comment())
MainWindow.setWindowTitle('欢迎使用QQ乞丐版')
MainWindow.show()

#主界面ui初始化的工作
ui.label_welcome.setText('欢迎！%s（%s）'%(NICK, ID))
ui.label_curchat.setText('当前聊天：聊天大厅（0）')
ui.label_curpyq.setText('当前朋友圈：无')
refresh_list()
refresh_chat('0')

#启动定时刷新线程
refresh_thread = My_Timer_Thread()
refresh_thread._signal.connect(test_thread)
refresh_thread.start()


app.exec_()
sock.close()
sys.exit()