'''
Author: Mrx
Date: 2023-01-25 13:18:48
LastEditors: Mrx
LastEditTime: 2023-01-27 02:57:48
FilePath: \CS271_project1\server.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''



import socket
import threading, time
from sys import exit
import json

user = { ('192.168.0.167', 10882) : 'Alice', ('192.168.0.167', 10884) : 'Bob', ('192.168.0.167', 10886) : 'Carl'} 
balancetable = {'Alice' : 10, 'Bob' : 10, 'Carl' : 10}

print("server")
def UI():
    while True :
        print("insert 'p' to print out the balance table")
        print("insert '0' to exit application")
        a = input("please insert command\n")
        if a == "0" :
            break
        elif a == "p" :
            for v,k in balancetable.items():
                print('{v} : ${k}'.format(v = v, k = k))
        else :
            print("ERROR! Please insert correct command")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# HOST = input("Please input IP address: ")
# PORT = 10888

HOST = '192.168.0.167'
PORT = 10888

s.bind((HOST, PORT))

# user = {}

def listen():
    while True:
        (data, addr) = s.recvfrom(1024)
        if balancetable.get(data.decode('utf-8')) :
            print("IP(%s) User(%s) connected to the server" % (addr, data.decode('utf-8')))
        elif data.decode('utf-8') == 'Query balance' :
            print('User(%s) queried its account balance' % (user[addr]))
            data = "You have $ " + str(balancetable[user[addr]]) + " in your account\n"
            # data = str(balancetable[user[addr]])
            s.sendto(data.encode('utf-8'), addr)
            time.sleep(1)
        elif isinstance(json.loads(data.decode('utf-8')), dict) :
            trans = json.loads(data.decode('utf-8'))
            # am = int(trans[user[addr]])
            receiver = trans['recipient']
            am = int(trans['amount'])         
            sum = balancetable[user[addr]]
            # print(am)
            # print(sum)
            if(am > sum) :
                data = "Denied"
                s.sendto(data.encode('utf-8'), addr)
                time.sleep(1)
            else :
                data = "Approved"
                balancetable[user[addr]] -= am
                balancetable[receiver] += am
                s.sendto(data.encode('utf-8'), addr)
                info = 'User ' + user[addr] + ' transferred $' + str(am) + ' to ' + receiver
                print(info)
                time.sleep(1)                                

#    else:
#       print(addr," : ", data.decode('utf-8'))
#       data = user[addr] + " : " + data.decode('utf-8')
#       for key, value in user.items():
#          if key != addr:
#             s.sendto(data.encode('utf-8'), key)

t1 = threading.Thread(target=listen)
t2 = threading.Thread(target=UI)

t1.start()
t2.start()
t1.join()
t2.join()
