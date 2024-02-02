from scapy.all import SNMP, IP, sniff
from datetime import datetime
import sqlite3

# Define the SNMP trap handler function
def handle_trap(pkt):

    if pkt.haslayer(SNMP):
        if "SNMPtrapv2" in pkt:
            varbindlist = pkt["SNMPtrapv2"].varbindlist
            interface_index = None
            for SMNPvarbind in varbindlist:
                trap_oid = str(SMNPvarbind.oid.val)
                trap_value = str(SMNPvarbind.value.val)

                if trap_value == '1.3.6.1.4.1.9.9.43.2.0.1':
                    # SYSLOG trap
                    date = datetime.utcfromtimestamp(pkt.time).strftime('%Y-%m-%d')
                    times = datetime.utcfromtimestamp(pkt.time).strftime('%H:%M:%S')
                    router_ip = pkt[IP].src
                    message = "PLACEHOLDER"
                    # Save the data to the database
                    con = sqlite3.connect("syslog.db")
                    cur = con.cursor()
                    con.execute("INSERT INTO syslog (DATE, TIME, ROUTER_IP, MESSAGE) VALUES (?, ?, ?, ?) ",
                                (date, times, router_ip, message))
                    con.commit()
                    cur.close()
                    con.close()
                elif trap_value == "1.3.6.1.6.3.1.1.5.4":
                    # LINK UP trap
                    date = datetime.utcfromtimestamp(pkt.time).strftime('%Y-%m-%d')
                    times = datetime.utcfromtimestamp(pkt.time).strftime('%H:%M:%S')
                    router_ip = pkt[IP].src
                    interface_name = trap_value
                    state = 'UP'
                    # Save the data to the database
                    con = sqlite3.connect("linupdown.db")
                    cur = con.cursor()
                    con.execute("INSERT INTO link_up_down (DATE, TIME, ROUTER_IP, INT_NAME, STATE) VALUES (?, ?, ?, ?, ?) ",
                                (date, times, router_ip, interface_name, state))
                    con.commit()
                    cur.close()
                    con.close()
                elif trap_value == '1.3.6.1.6.3.1.1.5.3':
                    # LINK DOWN trap
                    date = datetime.utcfromtimestamp(pkt.time).strftime('%Y-%m-%d')
                    times = datetime.utcfromtimestamp(pkt.time).strftime('%H:%M:%S')
                    router_ip = pkt[IP].src
                    interface_name = trap_value
                    state = 'DOWN'
                    # Save the data to the database
                    con = sqlite3.connect("linupdown.db")
                    cur = con.cursor()
                    con.execute("INSERT INTO link_up_down (DATE, TIME, ROUTER_IP, INT_NAME, STATE) VALUES (?, ?, ?, ?, ?) ",
                                (date, times, router_ip, interface_name, state))
                    con.commit()
                    cur.close()
                    con.close()
# Start the sniffer
print("Starting SNMP Sniffing")
sniff(filter="udp and port 161", prn=handle_trap, iface="tap0")
