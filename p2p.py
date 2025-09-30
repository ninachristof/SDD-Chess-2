import socket
import sys
from struct import *

PKT_SIZE = 16
PKT_HDR = "C2PKT"
#can have different packet types to define different actions easily
#also probably a sent and response packet
def host_game():
    host = "127.0.0.1"
    port = 2000
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
                if not data:
                    break
                if
                conn.sendall(data)

def connect_to_game():
    host = "127.0.0.1"
    port = 2000#prob do a scan for available ports or smth idk
    # have a loop of connection retries
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host,port))
        #instruction = "a6,b1"
        #test_pkt = pack("5ci",PKT_HDR,len(instruction))
        sock.sendall(b"Hello, world")
        data = sock.recv(PKT_SIZE)

    print(f"CLIENT: Received {data}")
def main():
    if(len(sys.argv) > 1):
        conn_type = sys.argv[1].strip()
        if(conn_type == "host"):
            print("hosting")
            host_game()
        else:
            print("connecting")
            connect_to_game()
    else:
        print("connecting")
        connect_to_game()


main()
