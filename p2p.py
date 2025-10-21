import socket
import sys
from struct import *

PKT_SIZE = 16
PKT_HDR = "C2PKT"
#can have different packet types to define different actions easily
#also probably a sent and response packet
def host_game(host,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            # do a few retries for packet maybe add a timeout
            #make sure it recieved all data, add header and maybe footer
            print(f"HOST: Connected to {addr}")
            while True:
                data = conn.recv(len(PKT_HDR))
                print(f"CLIENT: Received {data}")
                if not data:
                    break
                conn.sendall(data)

def connect_to_game(host, port):
    # have a loop of connection retries
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host,port))
        #instruction = "a6,b1"
        #test_pkt = pack("5ci",PKT_HDR,len(instruction))
        sock.sendall(b"help me")
        data = sock.recv(PKT_SIZE)

    print(f"CLIENT: Received {data}")
def main():
    print("p2p.py <host/connect> <ip> <port>")
    ip = "0.0.0.0"
    port = 5432
    print((sys.argv))
    if(len(sys.argv) == 4):
        conn_type = sys.argv[1].strip()
        ip = sys.argv[2].strip()
        port = int(sys.argv[3])
        if(conn_type == "host"):
            print("hosting")
            host_game(ip,port)
        else:
            print("connecting")
            connect_to_game(ip,port)
    else:
        print("hosting")
        host_game(ip, port)


main()
