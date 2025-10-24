import socket
import sys
from struct import *

ERROR = 1
PKT_HDR = b"C2PKT"
PKT_HDR_SIZE = 12 #len(PKT_HDR) + 7 #idk why 
#can have different packet types to define different actions easily
#also probably a sent and response packet
#maybe dont want to close socket if there is a disconnect and or handle the disconnect to 
#be able to allow a reconnect
#reconnecting needs to update board correctly so the whole board will need to be sent in that case as well as the turn

#return arguments for valid instruction, else return None
def parse_instruction(instruction):
    pass
def recv_instruction(conn):
    data = conn.recv(PKT_HDR_SIZE)
    if not data:
        print("empty packet")
        return ERROR
    recvd_hdr, instruction_size = unpack("5si",data)
    if(recvd_hdr != PKT_HDR or len(data) != PKT_HDR_SIZE):
        print("header error")
        return ERROR
    print(f"HOST: Received {data}")
    instruction = conn.recv(instruction_size)
    if not instruction:
        print("empty packet")
        return ERROR
    print(f"HOST: Received {data}")
    #instruction should be validated before sending. this should only parse
    x1,y1,x0,y0,color = parse_instruction(instruction)
    if(validate_instruction):
        movePiece(x1,y,x0,y0,color):
    return 0

def send_instruction(sock,str_instruction):
        instruction = bytes(str_instruction, "utf-8")
        #test_pkt = pack("5ci",PKT_HDR,len(instruction))
        hdr = pack("5si", PKT_HDR, len(instruction))
        #sock.sendall(b"help me")
        sock.sendall(hdr)
        sock.sendall(instruction)

def host_game(host,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        conn, addr = sock.accept()
        conn.setblocking(True)
        conn.settimeout(None)
        with conn:
        # do a few retries for packet maybe add a timeout
        #make sure it recieved all data, add header and maybe footer
        #TODO: how ot handle disconnections/ bad wifi?
        #TODO: how are the timers going to be synced up? 
        #todo: if error on receiving end, send a request to resend mesage
        #TODO: timestamp
            print(f"HOST: Connected to {addr}")
            while True:
                if(ERROR == recv_instruction(conn)):
                    break
                
                #response = b"fucki"
                #conn.sendall(response)

def connect_to_game(host, port):
    #TODO: have a loop of connection retries
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host,port))
        for i in range(10):
            str_instruction = f"{i}"
            send_instruction(sock,str_instruction)
def main():
    print("p2p.py <host/connect> <ip> <port>")
    ip = "0.0.0.0"
    port = 5432
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
