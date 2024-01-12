def add_router():
    print("Hello world")

def delete_router():
    print("Hello world")

def list_router():
    print("Hello world")

def set_backup_time():
    print("Hello world")

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
        break

    if user_input in Menu:
        Menu[user_input]()
    else:
        print("Invalid choice. Try again.")