'''
Author: Mrx
Date: 2023-01-25 13:18:48
LastEditors: Mrx
LastEditTime: 2023-01-27 10:56:19
FilePath: \CS271_project1\client.py
Description: 
Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''


import socket
import threading, time
from sys import exit
import json
from blockchain import *

print("client")

usertable = {'Alice' : 10882, 'Bob' : 10884, 'Carl' : 10886} 
user = { ('192.168.0.167', 10882) : 'Alice', ('192.168.0.167', 10884) : 'Bob', ('192.168.0.167', 10886) : 'Carl'}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True :
    username = input("Please input your username : ")
    if usertable.get(username) == None :
        print("wrong username!")
        continue
    break

PORT = usertable[username]
HOST = '192.168.0.167'
s.bind((HOST, PORT))

s.sendto(username.encode('utf-8'), (HOST, 10888))
time.sleep(3)
# for key, value in usertable.items():
#     if key != username:
#         s.sendto(username.encode('utf-8'), (HOST, usertable[key]))
#         time.sleep(3)

g_count = 0
g_flag = -1
g_b =-1
chain = None
g_time = 0

PORT = 10888
flag = True
def RECV():
    global g_count
    global g_flag
    global chain
    global g_time
    while flag:
      (data, addr) = s.recvfrom(1024)
    #   if usertable.get(data.decode('utf-8')) :
    #         print("connected to client(%s)" % (data.decode('utf-8')))
    #   elif data.decode('utf-8') == 'Transfer' :
    #     print('User(%s) is requesting a transfer' % (user[addr]))
    #     data = "OK"
    #     s.sendto(data.encode('utf-8'), addr)
    #     time.sleep(3)
    #   elif data.decode('utf-8') == "OK" :
    #     print('User(%s) agreed to the request' % (user[addr]))
    #     g_count += 1
    #     time.sleep(3)
    #   elif data.decode('utf-8') == "Denied" :
    #     g_flag = 0
    #   elif data.decode('utf-8') == "Approved" :
    #     g_flag = 1
      try :
        if isinstance(json.loads(data.decode('utf-8')), dict) :
            rev = {}
            rev = json.loads(data.decode('utf-8'))
            # del trans['status']
            if rev.get('status') :
                if chain == None:
                    chain = BlockChain(1, data.decode('utf-8'))
                else :
                    chain.new_block(None, data.decode('utf-8'))
                g_time = max(g_time, int(rev[user[addr]]))
                g_time += 1
                print("Local Lamport time(%d)\n" %(g_time))
            elif rev['info'] == 'Transfer' :
                print('User(%s) is requesting a transfer' % (user[addr]))
                g_time = max(g_time, int(rev[user[addr]]))
                g_time += 1
                data2 ={}
                data2['info'] = "OK"
                data2[username] = g_time
                data22 = json.dumps(data2)
                s.sendto(data22.encode('utf-8'), addr)
                time.sleep(3)
            elif rev['info'] == "OK" :
                print('User(%s) agreed to the request' % (user[addr]))
                g_count += 1
                g_time = max(g_time, int(rev[user[addr]]))
                g_time += 1
                print("Local Lamport time(%d)\n" %(g_time))
                time.sleep(3)
            # elif data.decode('utf-8') == "Denied" :
            #     g_flag = 0
            # elif data.decode('utf-8') == "Approved" :
            #     g_flag = 1
      except : 
        if data.decode('utf-8') == "Denied" :
            g_flag = 0
        if data.decode('utf-8') == "Approved" :
            g_flag = 1
        print(data.decode('utf-8'))
        time.sleep(3)
        # pass
    #   if usertable.get(data.decode('utf-8')) :
    #         print("connected to client(%s)" % (data.decode('utf-8')))
    #   elif data.decode('utf-8') == 'Transfer' :
    #     print('User(%s) is requesting a transfer' % (user[addr]))
    #     data = "OK"
    #     s.sendto(data.encode('utf-8'), addr)
    #     time.sleep(3)
    #   elif data.decode('utf-8') == "OK" :
    #     print('User(%s) agreed to the request' % (user[addr]))
    #     g_count += 1
    #     time.sleep(3)
    #   elif data.decode('utf-8') == "Denied" :
    #     g_flag = 0
    #   elif data.decode('utf-8') == "Approved" :
    #     g_flag = 1
    #   else:
    #     print(data.decode('utf-8'))
    #     time.sleep(3)
      
# def SEND():
#    while True:
#       data = input("")
#       s.sendto(data.encode('utf-8'), (HOST, PORT))
#       time.sleep(3)

def UI():
    global g_count
    global g_flag
    global g_b
    global chain
    global g_time
    while True :
        print("1. Transfer money to other clients")
        print("2. Query balance transaction")
        print("3. Print out blockchain")
        print("0. Exit application")
        a = input("please insert command\n")
        if a == "0" :
            flag = False
            # to server
            break
        elif a == "1" :
            while True:
                cl = input("please insert client's username : ")
                if usertable.get(cl) == None :
                    print("wrong username!")
                    continue
                break
            am = input("please insert transfer amount : ")
            g_time += 1
            t = {}
            t[username] = g_time 
            t['recipient'] = cl
            t['amount'] = am
            # print(t)
            status = ''
            trans = json.dumps(t)
            data1 = {}
            data1['info'] = 'Transfer'
            data1[username] = g_time
            data11 = json.dumps(data1)
            # info = 'Transfer'
            for key, value in usertable.items():
                if key != username:
                    s.sendto(data11.encode('utf-8'), (HOST, usertable[key]))
                    time.sleep(3)
            if g_count == 2 :
                g_count = 0
                # data = 'Query balance'
                print('send request to server')
                s.sendto(trans.encode('utf-8'), (HOST, 10888))
                time.sleep(3)
            if g_flag == 0 :
                g_time += 1
                t[username] = g_time
                status = 'Aborted'
                t['status'] = status
                trans = json.dumps(t)
                if chain == None:
                    # status = 'Aborted'
                    chain = BlockChain(1, trans)
                    g_b = 0
                else :
                    # status = 'Aborted'
                    chain.new_block(None, trans)
                print('transaction aborted\n')
                g_flag = -1
            if g_flag == 1 :
                g_time += 1
                t[username] = g_time
                status = 'Success'
                t['status'] = status
                trans = json.dumps(t)
                if chain == None:
                    status = 'Success'
                    chain = BlockChain(1, trans)
                    g_b = 0
                else :
                    status = 'Success'
                    chain.new_block(None, trans)
                print('transaction success\n')
                g_flag = -1
            # t['status'] = status
            # trans = json.dumps(t)
            for key, value in usertable.items():
                if key != username:
                    s.sendto(trans.encode('utf-8'), (HOST, usertable[key]))
                    time.sleep(3)

        elif a == "2" :
            g_time += 1
            data = 'Query balance'
            s.sendto(data.encode('utf-8'), (HOST, 10888))
            print("Local Lamport time(%d)\n" %(g_time))
            time.sleep(3)

        elif a == "3" :
            g_time += 1
            if chain == None :
                print('No blockchain now!')
            else :
                chain.show_chain()
            print("Local Lamport time(%d)\n" %(g_time))
        else :
            print("ERROR! Please insert correct command")


t1 = threading.Thread(target=RECV)
t2 = threading.Thread(target=UI)

t1.start()
t2.start()
t1.join()
t2.join()
