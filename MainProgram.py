import socket
import ssl
import sqlite3
import pickle
import BackupDevices
import schedule
import gzip
from io import BytesIO
import requests
import time
import paramiko
from elasticsearch import Elasticsearch, helpers
import threading
from pysnmp.hlapi import *
import matplotlib.pyplot as plt
from github import Github

ip = "127.0.0.1"
port = 12345
buffer_size = 2048

server_cert="server.crt"
client_cert="client.crt"
client_key="client.key"

token = "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"
header = {'Authorization': f'token {token}'}
username = "Jownic"
repo_name = "HomeAssignment"
url = f'https://api.github.com/repos/{username}/{repo_name}/commits'


schedule.every(1).minutes.do(BackupDevices.Backup_checker)

def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
schedule_thread.start()

def add_router():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='server.crt')
    context.load_cert_chain(certfile='client.crt',keyfile='client.key')

    s_unencrypted = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s = context.wrap_socket(s_unencrypted,server_side=False,server_hostname="example.com")

    s.connect((ip,port))
    print("Connected to Server",ip,port)


    Name = input("Router name: ")
    IP = input("Router IP: ")
    Username = input("Username: ")
    Password = input("Password: ")
    data_to_send = {'Name': Name, 'IP': IP, 'Username': Username, 'Password': Password}
    messageC = user_input.encode()
    s.send(messageC)
    data = pickle.dumps(data_to_send)
    s.send(data)
    messageC = s.recv(buffer_size)
    messageC = messageC.decode()
    print(messageC)
    s.send("q".encode())
    s.close()

def delete_router():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='server.crt')
    context.load_cert_chain(certfile='client.crt',keyfile='client.key')

    s_unencrypted = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s = context.wrap_socket(s_unencrypted,server_side=False,server_hostname="example.com")

    s.connect((ip,port))
    print("Connected to Server",ip,port)

    IP = input("Input Router IP to Delete: ")
    messageC = user_input.encode()
    s.send(messageC)
    data = pickle.dumps(IP)
    s.send(data)
    messageC = s.recv(buffer_size)
    messageC = messageC.decode()
    print(messageC)
    s.send("q".encode())
    s.close()

def list_router():

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='server.crt')
    context.load_cert_chain(certfile='client.crt',keyfile='client.key')

    s_unencrypted = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s = context.wrap_socket(s_unencrypted,server_side=False,server_hostname="example.com")

    s.connect((ip,port))
    print("Connected to Server",ip,port)

    messageC = user_input.encode()
    s.send(messageC)
    rlist = s.recv(buffer_size)
    rlist = rlist.decode()
    print(rlist)
    s.send("q".encode())
    s.close()

def set_backup_time():
    BackupDevices.Backup()
    BackupDevices.Backup_checker

def set_router_netflow_settings():
    router_ip = input("Input Router Ip: ")
    setnetflow(router_ip)


def remove_router_netflow_settings():
    router_ip = input("Input router ip: ")
    removenetflow(router_ip)

def set_router_snmp_settings():
    router_ip = input("Input Router IP: ")
    setsnmp(router_ip)
def remove_router_snmp_settings():
    router_ip = input("Input Router IP: ")
    removesnmp(router_ip)

def show_router_config():
    router_ip = input("Input Router IP: ")
    get_github_file_contents(router_ip)

def show_changes_router_config():
    router_ip = input("Input Router IP: ")
    file_path = f'Backups/{router_ip}.config'
    first_commit, last_commit = get_first_and_last_commit(username, repo_name, file_path, token)

    print(f"Earlies Backup: {first_commit.commit.author.date}")
    print(f"Latest Backup: {last_commit.commit.author.date}")

def display_netflow_statistics():
        router_ip = input("Input Router IP: ")
        conn = sqlite3.connect('netflow.db')
        cursor = conn.cursor()

        query = "SELECT PROTOCOL, COUNT(*) FROM netflowdata WHERE router_ip = ? GROUP BY protocol"
        cursor.execute(query, (router_ip,))
        data = cursor.fetchall()
        conn.close()

        protocols = [row[0] for row in data]
        packet_counts = [row[1] for row in data]

        plt.pie(packet_counts, labels=protocols, autopct='%1.1f%%', startangle=90, counterclock=False)
        plt.title(f'Packet Distribution for Router {router_ip}')
        plt.axis('equal')
        plt.show()
        
def show_router_syslog():
        router_ip = input("Input Router IP: ")
        con = sqlite3.connect("linupdown.db")
        cur = con.cursor()
        query = "SELECT * FROM LINK_UP_DOWN WHERE ROUTER_IP = ?"
        cur.execute(query, (router_ip,))
        data = cur.fetchall()

        CLOUD_ID = "ba0df661e93441398ed2a0c01c195ce7:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDA4NjgzMThlZjQzZDQ1NWU5OTc5MDU2NWQ0NzdiMzRiJDU2ZWY2NGM1NWMxYzQzYjk5NTNkMTUzMjA4OTNhYmM3"
        API_KEY = "V1JTUmFZMEI3empvdlQwVHdVdzQ6bllaRGdkMUpTLW0ybThMWmYwRngtUQ=="


        es =  client = Elasticsearch(
                cloud_id=CLOUD_ID,
                api_key=API_KEY,
            )

        actions = [
            {
            "_op_type": "index",
            "_index": 'syslog',
            "_source": {
                "ID": row[0],
                "date": row[1],
                "time": row[2],
                "router_ip": row[3],
                "int_name": row[4],
                "message": row[5]
                }
            }
        for row in data
        ]
        helpers.bulk(es, actions)


        search_querydown = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"router_ip": router_ip}},
                        {"match": {"message": "DOWN"}}
                    ]
                }
            }
        }
        search_queryup = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"router_ip": router_ip}},
                        {"match": {"message": "UP"}}
                    ]
                }
            }
        }



        search_result = es.search(index='syslog', body=search_querydown)
        search_result2 = es.search(index='syslog', body=search_queryup)
        if 'hits' in search_result and 'hits' in search_result['hits']:
            for hit in search_result.get('hits', {}).get('hits', []):
                print(f"Timestamp: {hit['_source']['time']}, Message: {hit['_source']['message']}")
        if 'hits' in search_result and 'hits' in search_result['hits']:
            for hit in search_result2['hits']['hits']:
                print(f"Timestamp: {hit['_source']['time']}, Message: {hit['_source']['message']}")

        es.transport.close()


def get_first_and_last_commit(username, repo_name, file_path, token):
    # Authenticate using your personal access token
    g = Github(token)

    # Get the repository
    repo = g.get_repo(f"{username}/{repo_name}")

    # Get the list of commits for the specified file
    repo = g.get_repo(f"{username}/{repo_name}")

    # Get the list of commits for the specified file
    commits = list(repo.get_commits(path=file_path))

    # Check if there are any commits for the file
    if len(commits) == 0:
        print(f"No commits found for '{file_path}'.")
        return None, None

    # Get the first and last commits if there are commits present
    first_commit = commits[-1]
    last_commit = commits[0]

    return first_commit, last_commit

def get_github_file_contents(router_ip):
    username = "JowniC"
    repository = "HomeAssignment" 
    file_path = f"Backups/{router_ip}.config"
    branch='main'
    token = "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"

    raw_url = f'https://raw.githubusercontent.com/{username}/{repository}/{branch}/{file_path}'

    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    response = requests.get(raw_url, headers=headers)

    if response.status_code == 200:
        # Check if the content is gzip-encoded
        if 'Content-Encoding' in response.headers and response.headers['Content-Encoding'] == 'gzip':
            compressed_data = BytesIO(response.content)
            try:
                with gzip.GzipFile(fileobj=compressed_data, mode='rb') as f:
                    file_contents = f.read().decode('utf-8')
            except gzip.BadGzipFile:
                # If it's not a valid gzip file, treat it as plain text
                file_contents = response.content.decode(response.encoding)
        else:
            # If not gzip-encoded, treat it as plain text
            file_contents = response.content.decode(response.encoding)

        # Print the content
        print(f"Contents of {file_path}:\n")
        print(file_contents)
    elif response.status_code == 404:
        # If the file is not found, print an error message
        print(f"\nFile not found. Status code: {response.status_code}")
        print(f"Double-check the file path: {raw_url}")
    else:
        # For other errors, print the status code and response content
        print(f"\nFailed to retrieve file. Status code: {response.status_code}")
        print(response.text)

def setsnmp(router_ip):
        commands = ['enable','conf t', 'logging history debugging', 'snmp-server community trap RO R0', 'snmp-server location R1', 'snmp-server host 192.168.1.1 comaccess', 'snmp-server host 192.168.1.1 version 2c trap udp-port 161', 'snmp-server enable traps', 'do copy run start', '', '']
        con = sqlite3.connect("routers.db")
        cur = con.cursor()

        cur.execute("SELECT USERNAME, PASSWORD FROM routers WHERE IP=?", (router_ip,))
        username, password = cur.fetchone()
        
        cur.close()
        con.close()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=username, password=password, timeout=10)

        try:
            # Connect to the router
            ssh_client.connect(router_ip, username=username, password=password, timeout=5)

            # Create a shell session
            ssh_shell = ssh_client.invoke_shell()

            # Send commands
            for command in commands:
                ssh_shell.send(command + '\n')
                time.sleep(1)  # Wait for the command to be executed
                output = ssh_shell.recv(65535).decode('utf-8')
                print("Setting SNMP Please wait...")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Done!")
            # Close the SSH connection
            if ssh_client:
                ssh_client.close()

def removesnmp(router_ip):
        commands = ['enable', 'conf t','no logging history debugging', 'no snmp-server community trap RO R0', 'no snmp-server location R1', 'no snmp-server host 192.168.1.1 comaccess', 'no snmp-server host 192.168.1.1 version 2c trap udp-port 161', 'no snmp-server enable traps', 'do copy run start', '', '']
        con = sqlite3.connect("routers.db")
        cur = con.cursor()

        cur.execute("SELECT USERNAME, PASSWORD FROM routers WHERE IP=?", (router_ip,))
        username, password = cur.fetchone()
        
        cur.close()
        con.close()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=username, password=password, timeout=10)

        try:
            # Connect to the router
            ssh_client.connect(router_ip, username=username, password=password, timeout=5)

            # Create a shell session
            ssh_shell = ssh_client.invoke_shell()

            # Send commands
            for command in commands:
                ssh_shell.send(command + '\n')
                time.sleep(1)  # Wait for the command to be executed
                output = ssh_shell.recv(65535).decode('utf-8')
                print("Removing SNMP Please wait...")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Done!")
            # Close the SSH connection
            if ssh_client:
                ssh_client.close()

def setnetflow(router_ip):
        commands = ['enable','conf t', 'flow record NTARecord', 'match ipv4 tos', 'match ipv4 protocol', 'match ipv6 source address', 'match ipv6 destination address', 'match transport source-port', 'match transport destination-port', 'match interface input', 'collect interface output', 'collect counter bytes', 'collect counter packets', 'collect timestamp sys-uptime first', 'collect timestamp sys-uptime last', 'exit', 'flow exporter NTAExport', 'destination 192.168.1.1', 'source FastEthernet0/0', 'transport udp 2055', 'template data timeout 60', 'exit', 'flow monitor NTAMonitor', 'exporter NTAExport', 'cache timeout active 60', 'record NTARecord', 'exit', 'ip flow-export source FastEthernet0/0', 'ip flow-export version 9', 'ip flow-export destination 192.168.1.1 2055', 'int Fa0/0', 'ip flow monitor NTAmonitor input', 'ip flow ingress', 'do copy run start', '', '' ]
        con = sqlite3.connect("routers.db")
        cur = con.cursor()

        cur.execute("SELECT USERNAME, PASSWORD FROM routers WHERE IP=?", (router_ip,))
        username, password = cur.fetchone()
        
        cur.close()
        con.close()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=username, password=password, timeout=10)

        try:
            # Connect to the router
            ssh_client.connect(router_ip, username=username, password=password, timeout=5)

            # Create a shell session
            ssh_shell = ssh_client.invoke_shell()
            print("Setting netflow Please wait...")
            # Send commands
            for command in commands:
                ssh_shell.send(command + '\n')
                time.sleep(1)  # Wait for the command to be executed
                output = ssh_shell.recv(65535).decode('utf-8')


        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Done!")
            # Close the SSH connection
            if ssh_client:
                ssh_client.close()

def removenetflow(router_ip):
        commands = ['enable','conf t', 'int Fa0/0', 'no ip flow monitor NTAMonitor input', 'no ip flow ingress', 'exit', 'no flow monitor NTAMonitor', 'no flow exporter NTAExport', 'no flow record NTARecord', 'no ip flow-export source FastEthernet0/0', 'no ip flow-export version 9', 'no ip flow-export destination 192.168.1.1 2055', 'do copy run start', '', '' ]
        con = sqlite3.connect("routers.db")
        cur = con.cursor()

        cur.execute("SELECT USERNAME, PASSWORD FROM routers WHERE IP=?", (router_ip,))
        username, password = cur.fetchone()
        
        cur.close()
        con.close()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=username, password=password, timeout=10)

        try:
            # Connect to the router
            ssh_client.connect(router_ip, username=username, password=password, timeout=5)

            # Create a shell session
            ssh_shell = ssh_client.invoke_shell()

            # Send commands
            for command in commands:
                ssh_shell.send(command + '\n')
                time.sleep(1)  # Wait for the command to be executed
                output = ssh_shell.recv(65535).decode('utf-8')
                print("Removing netflow please wait...")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Done!")
            # Close the SSH connection
            if ssh_client:
                ssh_client.close()








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
        break

    if user_input in Menu:
        Menu[user_input]()
        
    else:
        print("Invalid choice. Try again.")