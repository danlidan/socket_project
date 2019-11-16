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
        'req_refresh_list': req_refresh_list
    }
    func = switcher.get(params[0], lambda:"nothing")
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
    sock.bind(('172.100.96.163', 8998))  # 配置soket，绑定IP地址和端口号
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

