import sqlite3
from datetime import datetime, time, timedelta
import paramiko
import time
from github import Github
import schedule
import threading

token = "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"
gusername = "Jownic"
repo_name = "HomeAssignment" 
routers_to_backup = []

def is_valid_time(time_str):
    try:
        # Attempt to parse the input as HH:MM
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False
    

def Backup():
    IP = input("Input Router IP: ")
    Time = input("Input the time for backup in HH:MM: ")

    con = sqlite3.connect("routers.db")
    cur = con.cursor()

    try:
        cur.execute("SELECT NAME, IP, USERNAME, PASSWORD FROM routers WHERE IP=?", (IP,))
        result = cur.fetchall()

        if result:
            if is_valid_time(Time):
                con.execute("UPDATE routers SET BACKUP_TIME=? WHERE IP=?", (Time, IP,))
                con.commit()
            else:
                print("Invalid Time format")
        else:
            print("Router doesn't exist")
    except sqlite3.Error as e:
        print(f"Error checking database")

    finally:
        cur.close()
        con.close()


def upload_file_to_github(token, username, repo_name, router_ip):
    # Authenticate using your personal access token
    g = Github(token)
    file_path = f"Backups/{router_ip}.config"
    print(router_ip)
    # Get the user
    user = g.get_user(username)

    # Get the repository
    repo = user.get_repo(repo_name)

    # Specify the branch 
    branch_name = "main"

    try:
        # Get the branch reference
        branch = repo.get_branch(branch_name)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Branch '{branch_name}' not found. Please check the branch name.")
        return

    # Read the content of the file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Create a new file on GitHub
    try:
        contents = repo.get_contents(file_path, ref=branch_name)
        # If the file already exists, update its content
        repo.update_file(contents.path, "Update file", file_content, contents.sha, branch=branch_name)

    except Exception as e:
        # If the file doesn't exist, create a new file
        repo.create_file(file_path, "Create file", file_content, branch=branch_name)


def perform_backup(router_ip, username, password):
    try:
        filename = f"Backups/{router_ip}.config"

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=username, password=password, timeout=10)
        stdin, stdout, stderr = ssh_client.exec_command("show running-config")
        running_config = stdout.read().decode()
        

        with open(filename, "w") as file:
            file.write(running_config)

        upload_file_to_github(token, gusername, repo_name, router_ip)

    except paramiko.AuthenticationException:
        print(f"Authentication failed.")
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
    except Exception as e:
        print(f"Error retrieving running configuration: {e}")
    finally:
        # Close the SSH connection
        ssh_client.close()

def Backup_checker():
    # Gets current time
    current_time = datetime.now().time()

    con = sqlite3.connect("routers.db")
    cur = con.cursor()

    try:
        cur.execute("SELECT IP, USERNAME, PASSWORD, BACKUP_TIME FROM routers")
        routers_info = cur.fetchall()

        for router_info in routers_info:
            router_ip, username, password, backup_time_str = router_info
 
            # Convert the stored time from the database to a time object
            backup_time = datetime.strptime(backup_time_str, "%H:%M").time()

            # Check if it's time to perform the backup for this router
            if current_time.hour == backup_time.hour and current_time.minute == backup_time.minute:
                routers_to_backup.append((router_ip, username, password))

        for router_to_backup in routers_to_backup:
            router_ip, username, password = router_to_backup
            perform_backup(router_ip, username, password)
                

    except sqlite3.Error as e:
        print(f"Error querying database: {e}")

    finally:
        cur.close()
        con.close()

