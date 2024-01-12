 # GNU nano 6.2                                                                                                                                                                      serverp.py                                                                                                                                                                                
#1 = IP Address
#2 = MAC Address
#3 = CPU Usage
#4 = Virtual  Memory Usage
#5 = Swap Memory Usage
#6 = Exit

import socket
import math
import psutil
import ssl


ip="127.0.0.1"
port=12345
buffer_size = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((ip,port))
s.listen()
print("Listening on port 12345 for client")
client_sock_unencrypted, addr = s.accept()
client_sock = context.wrap_socket(client_sock_unencrypted,server_side=True) 
print("Client connected with address",addr)

while(True):
  print("Waiting for message from client...")
  messageS = client_sock.recv(buffer_size)
  messageS = messageS.decode()
  print("Received from client:",messageS)

  if messageS == "1":
    messageS = socket.gethostbyname(socket.gethostname()+".localdomain")
    messageS = messageS.encode()
    client_sock.send(messageS)

  elif messageS == "3":
    messageS = str(psutil.cpu_percent())
    messageS = messageS.encode()
    client_sock.send(messageS)

  elif messageS == "4":
    messageS = str(psutil.virtual_memory().percent)
    messageS = messageS.encode()
    client_sock.send(messageS)

  elif messageS == "5":
    messageS = str(psutil.swap_memory().percent)
    messageS = messageS.encode()
    client_sock.send(messageS)


  elif messageS == "6":
    print("Closing Connection")
    client_sock.close()
    s.close()
    break

  else:
    print("Wrong command Received")