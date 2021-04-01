#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bottle import get,post,run,request,template,route,response


import threading
import time
import sys  
import socket
import struct

exitFlag = 0
SEND_BUF_SIZE = 256
 
RECV_BUF_SIZE = 256

@get("/")
def index():
    return template("login")
    
@route('/login', method = 'post')
def index():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username == 'jetta' and password == 'jetta' :
        return template('index')
    return template('login_error')

@route('/cookie')
def cookie(adss):
    global data
    global TcpconnectCount
    response.set_cookie("cookie1",adss)
    if TcpconnectCount == 1:
        response.set_cookie("cookie2","1")
    else:
        response.set_cookie("cookie2","0")

    #print(TcpconnectCount)
    


@post("/cmd")
def cmd():
	global client
	adss=request.body.read().decode()
	client.send(adss.encode('utf-8'))
	#print("按下了按钮" + adss)
	return "OK"
@post("/delay")
def delay():
    adss=request.body.read().decode()
   
    cookie(adss)
    #print(adss)
    #print(int(time.time()*1000))
    return "OK"


class myThread1 (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        run(host="0.0.0.0",port=80,relooader = True,debug = True)

        
class myThread2 (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):        
        ip = '192.168.0.64'
        port = 8080
        count = 0
        clinetlist = [] 
          # create socket
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # bind port
        print("starting listen on ip %s, port %s" % server_address)
        sock.bind(server_address)
        
        
        # start listening, allow only one connection
        try:
        	sock.listen(1)
        except socket.error:
            print("fail to listen on port %s" % e)
            sock.close()
            #sys.exit(1)
        try:    
            while True:
                global client
                global TcpconnectCount
                if TcpconnectCount == 0:
                    client, addr = sock.accept()
                    TcpconnectCount = 1
                    print('新用户[%s]连接' % str(addr))
                    print(clinetlist)
                    thread_msg = threading.Thread(target=recv_msg, args=(client, addr))
                    thread_msg.setDaemon(True)
                    thread_msg.start()

        except BaseException as e:
            print(repr(e))
        finally:
            sock.close()

def recv_msg(new_tcp_socket, ip_port):
    global data
    global TcpconnectCount
    count = 0
    # 这个while可以不间断的接收客户端信息
    while True:
        try:
            data = client.recv(1024,0x40)       
        except BlockingIOError as e:
            data = "None"

        if not data:
            print('用户[%s]断开连接' % str(ip_port))
            data = 0
            TcpconnectCount = 0
            break        
        #elif data != "None":
            #response.set_cookie("cookie2","1")
        if data != "None":
            count = 0
        else:
            count = count + 1
        if count >= 10:
            count = 0
            print('用户[%s]断开连接' % str(ip_port))
            TcpconnectCount = 0
            data = "None"
            break
        time.sleep(1)
    # 关闭客户端连接    
    new_tcp_socket.close()

data = "None"
okcount = 0
ngcount = 0
TcpconnectCount = 0

# 创建新线程
thread1 = myThread1()
thread2 = myThread2()

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("退出主线程")
