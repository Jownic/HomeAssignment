import sqlite3
from scapy.all import *
from scapy.all import IP, UDP,  sniff, Ether
from scapy.layers import netflow
from scapy.layers.netflow import NetflowHeaderV9
from datetime import datetime, timezone


def extract_netflow_info(packet):
    if NetflowHeaderV9 in packet and netflow.NetflowDataflowsetV9 in packet:
        netflow_header = packet[NetflowHeaderV9]
        flowset = packet[netflow.NetflowDataflowsetV9]


        for record in flowset.records:
            try:
                # Extract fields with error handling
                datetimes = packet[NetflowHeaderV9].unixSecs
                date_time = datetime.fromtimestamp(datetimes)
                date = date_time.date()
                time = date_time.time()
                router_ip = packet[IP].src
                num_packets = packet[NetflowHeaderV9].count
                source_ip = packet[IP].src
                destination_ip = packet[IP].dst
                protocol = packet[IP].proto
                source_port = packet[UDP].sport
                destination_port = packet[UDP].dport
                # Print or process the extracted information
                con = sqlite3.connect("netflow.db")
                cur = con.cursor()
                con.execute("INSERT INTO Netflowdata(DATE, TIME, ROUTER_IP, NO_OF_PACKETS, SRC_IP, DES_IP, PROTOCOL, SRC_PRT, DES_PRT) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                            (str(date), str(time), str(router_ip), num_packets, str(source_ip), str(destination_ip), str(protocol), str(source_port), str(destination_port) ))
                con.commit()
                cur.close()
                con.close()

            except AttributeError as e:
                print(f"Error in parsing record: {e}")

if __name__ == "__main__":
    print("Starting NetFlow packet capture...")
    sniff(prn=extract_netflow_info, store=0, filter="udp and port 2055", iface="tap0")