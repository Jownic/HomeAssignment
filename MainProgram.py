import socket
import ssl
import sqlite3
import pickle
import BackupDevices
import schedule
import time
import threading

ip = "127.0.0.1"
port = 12345
buffer_size = 2048

server_cert="server.crt"
client_cert="client.crt"
client_key="client.key"

schedule.every(1).minutes.do(BackupDevices.Backup_checker)

def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
schedule_thread.start()

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='server.crt')
context.load_cert_chain(certfile='client.crt',keyfile='client.key')

s_unencrypted = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s = context.wrap_socket(s_unencrypted,server_side=False,server_hostname="example.com")
s.connect((ip,port))
print("Connected to Server",ip,port)


def add_router():

    messageC = user_input.encode()
    s.send(messageC)

    Name = input("Router name: ")
    IP = input("Router IP: ")
    Username = input("Username: ")
    Password = input("Password: ")
    data_to_send = {'Name': Name, 'IP': IP, 'Username': Username, 'Password': Password}
    data = pickle.dumps(data_to_send)
    s.send(data)
    messageC = s.recv(buffer_size)
    messageC = messageC.decode()
    print(messageC)

def delete_router():
    IP = input("Input Router IP to Delete: ")
    messageC = user_input.encode()
    s.send(messageC)
    data = pickle.dumps(IP)
    s.send(data)
    messageC = s.recv(buffer_size)
    messageC = messageC.decode()
    print(messageC)

def list_router():
    messageC = user_input.encode()
    s.send(messageC)
    rlist = s.recv(buffer_size)
    rlist = rlist.decode()
    print(rlist)

def set_backup_time():
    BackupDevices.Backup()

def set_router_netflow_settings():
    print("Hello world")

def remove_router_netflow_settings():
    print("Hello world")

def set_router_snmp_settings():
    print("Hello world")

def remove_router_snmp_settings():
    print("Hello world")

def show_router_config():
    print("Hello world")

def show_changes_router_config():
    print("Hello world")

def display_netflow_statistics():
    print("Hello world")

def show_router_syslog():
    print("Hello world")



Menu = {
    "a": add_router, 
    "b": delete_router, 
    "c": list_router, 
    "d": set_backup_time, 
    "e": set_router_netflow_settings,
    "f": remove_router_netflow_settings, 
    "g": set_router_snmp_settings, 
    "h": remove_router_snmp_settings,
    "i": show_router_config, 
    "j": show_changes_router_config, 
    "k": display_netflow_statistics,
    "l": show_router_syslog
    } 

while True:
    print("Choose an option: ")
    for key, value in Menu.items():
        print(f"{key}. {value.__name__.replace('_', ' ')}")
        

    user_input = input("Enter the choice (q: Quit): ").lower()

    if user_input == 'q':
        s.send("q".encode())
        s.close()
        break

    if user_input in Menu:
        Menu[user_input]()
        
    else:
        print("Invalid choice. Try again.")


