import pymysql
import sys
if(sys.version[:1] == "3"):
    import _thread as thread
import time
# import thread
import socket

#来自客户端的请求列表
def req_handler(params, connection):
    switcher = {
        'req_login': req_login,
        'req_sign': req_sign,
        'req_refresh_list': req_refresh_list,
        'req_change_nick': req_change_nick,
        'req_send_text': req_send_text,
        'req_acquire_chatrecord': req_acquire_chatrecord,
        'req_acquire_more_chatrecord': req_acquire_more_chatrecord,
        'req_send_pyq': req_send_pyq,
        'req_comment_pyq': req_comment_pyq,
        'req_acquire_pyq': req_acquire_pyq,
        'req_pyq_good': req_pyq_good,
    }
    try:
        func = switcher.get(params[0], lambda:"nothing")
    except Exception:
        print('proto error!')
        return
    return func(params, connection)

#以下为各种变量的定义
#id_conn: id对conn, nick的映射
#conn_id: conn对id, nick的映射，与id_conn组成在线列表
#user_list: 所有成员，包括在线和不在线的列表 映射关系 id : nick
#conn 为本地mysql的连接
id_conn = {}
conn_id = {}
user_list = {}
sqlconn = pymysql.connect(user = 'root', password = '123', database = 'socket_project', charset = 'utf8')
cursor = sqlconn.cursor()

#以下为服务器内部操作的接口
def init_user_list():
    sql = "select * from users;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for id, password, nick in result:
        user_list[id] = nick

#以下为各种客户端请求的协议------------------------------------------------------------------------
def req_login(params, conn):
    id = params[1]
    password = params[2]
    if id in id_conn:
        data = '||'.join(['ack_login', 'not'])
        conn.send(data.encode('utf-8'))
        return
    sql = "select * from users where id = '%s' and pass = '%s';"%(id, password)
    cursor.execute(sql)
    result = cursor.fetchall()
    if(len(result) > 0):
        nick = result[0][2]
        data = '||'.join(['ack_login', 'ok', id, nick])
        id_conn[id] = (conn, nick)
        conn_id[conn] = (id, nick)
        conn.send(data.encode('utf-8'))
    else:
        data = '||'.join(['ack_login', 'not'])
        conn.send(data.encode('utf-8'))

def req_sign(params, conn):
    id = params[1]
    password = params[2]
    nick = params[3]
    sql = "select * from users where id = '%s';"%id
    cursor.execute(sql)
    result = cursor.fetchall()
    if(len(result) > 0):
        data = '||'.join(['ack_sign', 'not'])
        conn.send(data.encode('utf-8'))
    else:
        sql = "insert into users values('%s', '%s', '%s');"%(id, password, nick)
        cursor.execute(sql)
        sqlconn.commit()
        user_list[id] = nick
        data = '||'.join(['ack_sign', 'ok'])
        conn.send(data.encode('utf-8'))

#发送的格式：id, nickname, is_online
def req_refresh_list(params, conn):
    ret_list = []
    for id, nick in user_list.items():
        if id in id_conn:
            data = '##'.join([id, nick, 'yes'])
        else:
            data = '##'.join([id, nick, 'no'])
        ret_list.append(data)
    ret_data = '||'.join(ret_list)
    ret_data = '||'.join(['ack_refresh_list', ret_data])
    conn.send(ret_data.encode('utf-8'))

#修改昵称
def req_change_nick(params, conn):
    id = params[1]
    new_nick = params[2]
    id_conn[id] = (conn, new_nick)
    conn_id[conn] = (id, new_nick)
    user_list[id] = new_nick
    sql = "update users set nick_name = '%s' where id = '%s';"%(new_nick, id)
    cursor.execute(sql)
    sqlconn.commit()

    ret_data = '||'.join(['ack_change_nick', new_nick])
    conn.send(ret_data.encode('utf-8'))

def req_send_text(params, conn):
    sender_id = params[1]
    recver_id = params[2]
    text = params[3]
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    retdata = '||'.join(['ack_send_text', sender_id, user_list[sender_id], recver_id, text, dt])

    #私聊
    if recver_id != '0':
        sql = "insert into chat_records values('%s', '%s', '%s', '%s');"%(sender_id, recver_id, dt, text)
        cursor.execute(sql)
        sqlconn.commit()
        if sender_id in id_conn:
            id_conn[sender_id][0].send(retdata.encode('utf-8'))
        if recver_id in id_conn:
            id_conn[recver_id][0].send(retdata.encode('utf-8'))
    else:   #聊天大厅
        sql = "insert into chat_global values('%s', '%s', '%s');"%(sender_id, dt, text)
        cursor.execute(sql)
        sqlconn.commit()
        for conn, values in conn_id.items():
            conn.send(retdata.encode('utf-8'))

#params: sender, recver
#retdata : recver_id + (senderid, sendernick, time, text),(),.....
def req_acquire_chatrecord(params, conn):
    sender_id = params[1]
    recver_id = params[2]
    if(recver_id == '0'): #请求聊天大厅的记录
        sql = "select * from chat_global;"
        cursor.execute(sql)
        data = cursor.fetchall()
        tmp = []
        l = len(data)
        if l < 20:
            for sid, t, text in data:
                t_str = t.strftime("%Y-%m-%d %H:%M:%S")
                tmp.append('##'.join([sid, user_list[sid], t_str, text]))
        else:
            for i in range(l - 20, l):
                sid = data[i][0]
                t = data[i][1]
                text = data[i][2]
                t_str = t.strftime("%Y-%m-%d %H:%M:%S")
                tmp.append('##'.join([sid, user_list[sid], t_str, text]))

        tmp2 = '||'.join(tmp)
        ret_data = '||'.join(['ack_acquire_chatrecord', recver_id, tmp2])
        conn.send(ret_data.encode('utf-8'))
    else:
        sql = "select * from chat_records where (sender_id = '%s' and recver_id = '%s') or (sender_id = '%s' and recver_id = '%s') order by send_time"\
              %(sender_id, recver_id, recver_id, sender_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        tmp = []
        l = len(data)
        if l < 20:
            for sid, rid, t, text in data:
                t_str = t.strftime("%Y-%m-%d %H:%M:%S")
                tmp.append('##'.join([sid, user_list[sid], t_str, text]))
        else:
            for i in range(l - 20, l):
                sid = data[i][0]
                t = data[i][2]
                text = data[i][3]
                t_str = t.strftime("%Y-%m-%d %H:%M:%S")
                tmp.append('##'.join([sid, user_list[sid], t_str, text]))
        tmp2 = '||'.join(tmp)
        ret_data = '||'.join(['ack_acquire_chatrecord', recver_id, tmp2])
        conn.send(ret_data.encode('utf-8'))

def req_acquire_more_chatrecord(params, conn):
    sender_id = params[1]
    recver_id = params[2]
    if (recver_id == '0'):  # 请求聊天大厅的记录
        sql = "select * from chat_global;"
        cursor.execute(sql)
        data = cursor.fetchall()
        tmp = []
        l = len(data)
        if l < 80:
            for sid, t, text in data:
                t_str = t.strftime("%Y-%m-%d %H:%M:%S")
                tmp.append('##'.join([sid, user_list[sid], t_str, text]))
        else:
            for i in range(l - 80, l):
                sid = data[i][0]
                t = data[i][1]
                text = data[i][2]
                t_str = t.strftime("%Y-%m-%d %H:%M:%S")
                tmp.append('##'.join([sid, user_list[sid], t_str, text]))

        tmp2 = '||'.join(tmp)
        ret_data = '||'.join(['ack_acquire_chatrecord', recver_id, tmp2])
        conn.send(ret_data.encode('utf-8'))
    else:
        sql = "select * from chat_records where (sender_id = '%s' and recver_id = '%s') or (sender_id = '%s' and recver_id = '%s') order by send_time"\
              %(sender_id, recver_id, recver_id, sender_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        tmp = []
        l = len(data)
        if l < 80:
            for sid, rid, t, text in data:
                t_str = t.strftime("%Y-%m-%d %H:%M:%S")
                tmp.append('##'.join([sid, user_list[sid], t_str, text]))
        else:
            for i in range(l - 80, l):
                sid = data[i][0]
                t = data[i][2]
                text = data[i][3]
                t_str = t.strftime("%Y-%m-%d %H:%M:%S")
                tmp.append('##'.join([sid, user_list[sid], t_str, text]))
        tmp2 = '||'.join(tmp)
        ret_data = '||'.join(['ack_acquire_chatrecord', recver_id, tmp2])
        conn.send(ret_data.encode('utf-8'))

#发朋友圈
def req_send_pyq(params, conn):
    sender_id = params[1]
    send_time = params[2]
    context = params[3]
    sql = "insert into pyq_main values('%s', '%s', '%s', 0);"%(sender_id, send_time, context)
    try:
        cursor.execute(sql)
    except Exception:
        print('send pyq failed!')
        return
    sqlconn.commit()

#评论朋友圈
def req_comment_pyq(params, conn):
    sender_id = params[1]
    send_time = params[2]
    commenter_id = params[3]
    context = params[4]
    sql = "insert into pyq_comment values('%s', '%s', '%s', '%s')"%(sender_id, send_time, commenter_id, context)
    try:
        cursor.execute(sql)
    except Exception:
        print('send pyq comment failed!')
        return
    sqlconn.commit()

#获取/刷新朋友圈
def req_acquire_pyq(params, conn):
    acker_id = params[1]
    if acker_id == '0':
        sql = "select * from pyq_main order by send_time;"
    else:
        sql = "select * from pyq_main where sender_id = '%s' order by send_time"%acker_id

    try:
        cursor.execute(sql)
    except Exception:
        print('db error!')
        return
    result= cursor.fetchall()
    pyqs = []
    i = 0
    for id, dt, content, counter in result:
        if i >= 25:
            break
        send_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        nick = user_list[id]

        #搜索这条朋友圈的评论
        comments = []
        sql = "select * from pyq_comment where sender_id = '%s' and send_time = '%s';"%(id, send_time)
        cursor.execute(sql)
        result_2 = cursor.fetchall()
        for id_cmt, dt_cmt, commenter_id, comment in result_2:
            nick_cmt = user_list[commenter_id]
            comments.append(nick_cmt + '&&' + comment)
        comments_str = '**'.join(comments)

        #data = nick ^^ id ^^ send_time ^^ counter ^^ content ^^ nick1 && cmt1 ** nick2 && cmt2
        one_pyq = [nick, id, send_time, str(counter), content, comments_str]
        pyqs.append('^^'.join(one_pyq))
        i = i + 1

    #data_all =  data1 || data2 || ...
    data = '||'.join(pyqs)
    retdata = '||'.join(['ack_acquire_pyq', data])
    conn.send(retdata.encode('utf-8'))

#点赞
def req_pyq_good(params, conn):
    sender_id = params[1]
    send_time = params[2]
    sql = "update pyq_main set cool_counter = cool_counter + 1 where sender_id = '%s' and send_time = '%s';"%(sender_id, send_time)
    try:
        cursor.execute(sql)
    except Exception:
        print('点赞错误！')
        return
    sqlconn.commit()

##----------------------------------------------------------------------------------------------
def child_connection(index, sock, connection, address):
    try:
        print("begin connecion %d" % index)
        # 获得一个连接，然后开始循环处理这个连接发送的信息
        while True:
            buf = connection.recv(1024).decode('utf-8')
            params = buf.split('||')
            req_handler(params, connection)

    except Exception: # 如果建立连接后，该连接在设定的时间内无数据发来，则time out
        print("closing connection %d" % index)  # 当一个连接监听循环退出后，连接可以关掉
        connection.close()
        if connection in conn_id:
            id = conn_id[connection][0]
            if id in id_conn:
                id_conn.pop(id)
            conn_id.pop(connection)
        # 关闭连接，最后别忘了退出线程
        thread.exit_thread()


'''
建立一个python server，监听指定端口，
如果该端口被远程连接访问，则获取远程连接，然后接收数据，
并且做出相应反馈。
'''
if __name__ == "__main__":

    print("Server is starting")
    init_user_list()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('10.222.201.44', 8998))  # 配置soket，绑定IP地址和端口号
    sock.listen(5)  # 设置最大允许连接数，各连接和server的通信遵循FIFO原则

    index = 0
    while True:  # 循环轮询socket状态，等待访问

        connection, address = sock.accept()
        index += 1
        # 当获取一个新连接时，启动一个新线程来处理这个连接
        thread.start_new_thread(child_connection, (index, sock, connection, address))
        if index > 100:
            break
    sock.close()