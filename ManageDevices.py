import socket
import sqlite3
import ssl
import pickle

server_cert = "server.crt"
client_certs = "client.crt"
server_key = "server.key"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.minimum_version = ssl.TLSVersion.TLSv1_3
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
context.load_verify_locations(cafile='client.crt')

token = "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"
gusername = "Jownic"
repo_name = "HomeAssignment"
url = f'https://api.github.com/repos/{gusername}/{repo_name}/commits'

ip = "127.0.0.1"
port = 12345
buffer_size = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen()
print("Listening on port 12345 for client")



while True:
    client_sock_unencrypted, addr = s.accept()
    client_sock = context.wrap_socket(client_sock_unencrypted, server_side=True)
    print("Client connected with address", addr)

    try:
        while True:
            messageS = client_sock.recv(buffer_size).decode()


            if messageS == "a":
                serialized_data = client_sock.recv(buffer_size)
                received_data = pickle.loads(serialized_data)
                print(received_data)
                Name = received_data['Name']
                IP = received_data['IP']
                User = received_data['Username']
                Pass = received_data['Password']
                print(User,Pass,IP,Name)
            
                con = sqlite3.connect("routers.db")
                cur = con.cursor()
                cur.execute('SELECT ID FROM routers WHERE IP = ?', (IP,))
                existing_record = cur.fetchone()

                if existing_record:
                    # Send a message to the client indicating that the IP is not unique
                    client_sock.send("Router already exists!".encode())
                else:
                    con.execute("INSERT INTO routers (Name, IP, Username, Password) VALUES (?, ?, ?, ?) ",
                                (Name, IP, User, Pass))
                    con.commit()
                    cur.close()
                    con.close()
                    messageS = 'Router added successfully'
                    client_sock.send(messageS.encode())
                
            elif messageS == "b":
                serialized_data = client_sock.recv(buffer_size)
                IP = pickle.loads(serialized_data)

                con = sqlite3.connect("routers.db")
                cur = con.cursor()
                IP = str(IP)
                cur.execute('DELETE FROM routers WHERE IP = (?)', (IP,))
                con.commit()
                cur.close()
                con.close()
                Delete = 'Router removed successfully'
                client_sock.send(Delete.encode())
                

            elif messageS == "c":
                con = sqlite3.connect("routers.db")
                cur = con.cursor()
                cur.execute("SELECT NAME, IP, USERNAME, PASSWORD FROM routers")
                rlist = cur.fetchall()
                rlist = str(rlist).encode()
                client_sock.send(rlist)
                cur.close()
                con.close()
                client_sock.close()

            elif messageS == "q":
                print("Client requested disconnect.")
                client_sock.close()

    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_sock.close()
        print("Client Disconnected")