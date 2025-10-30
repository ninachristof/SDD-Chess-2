import socket
import sys
from struct import *
import global_vars

ERROR = 1
PKT_HDR = b"C2PKT"
PKT_HDR_SIZE = 12 #len(PKT_HDR) + 7 #idk why 
#can have different packet types to define different actions easily
#also probably a sent and response packet
#maybe dont want to close socket if there is a disconnect and or handle the disconnect to 
#be able to allow a reconnect
#reconnecting needs to update board correctly so the whole board will need to be sent in that case as well as the turn


class p2p:
#return arguments for valid instruction, else return None
    conn_type = None
    sock = None
    conn = None
    ip = None
    port = None
    def __init__(self, conn_type, ip, port):
        self.conn_type = conn_type
        self.ip = ip
        if(conn_type == "host"):
            self.ip = ""
        self.port = port
        
    def close_all(self):
        if(self.conn != None):
            self.conn.close()
        if(self.sock != None):
            self.sock.close()
    def recv_instruction_2(self):
        print("host:", self.conn)
        data = self.conn.recv(PKT_HDR_SIZE)
        if not data:
            print("empty packet")
            return ERROR
        recvd_hdr, instruction_size = unpack("5si",data)
        if(recvd_hdr != PKT_HDR or len(data) != PKT_HDR_SIZE):
            print("header error")
            return ERROR
        print(f"Received header {data}")
        print(f"size {instruction_size}")
        instruction = self.conn.recv(instruction_size)
        if not instruction:
            print("empty packet")
            return ERROR
        print(f"Received  instruction {data}")
        #instruction should be validated before sending. this should only parse
        x1,y1,x0,y0,color = unpack("iiii5s", instruction)
        return (x1,y1,x0,y0,color)

    def send_instruction_2(self):
        #TODO: not make the current instruction global
            print(f"sending {global_vars.current_instruction}")
            #test_pkt = pack("5ci",PKT_HDR,len(instruction))
            hdr = pack("5si", PKT_HDR, len(global_vars.current_instruction))
            #sock.sendall(b"help me")
            bytes_sent = self.conn.sendall(hdr)
            #if(bytes_sent != len(hdr)):
            #    self.sock.send(hdr[bytes_sent:])
                
            self.conn.sendall(global_vars.current_instruction)

    #host is host ip probably 0.0.0.0 so that it listens to inconming traffic
    def host_game_2(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(5)
        self.conn, addr = self.sock.accept()
        self.conn.setblocking(True)
        self.conn.settimeout(None)
        print("HOST ACCEPTED")
        #with conn:
        # do a few retries for packet maybe add a timeout
        #make sure it recieved all data, add header and maybe footer
        #TODO: how ot handle disconnections/ bad wifi?
        #TODO: how are the timers going to be synced up? 
        #todo: if error on receiving end, send a request to resend mesage
        #TODO: timestamp
        #    print(f"HOST: Connected to {addr}")
        #    while True:
        #        if(ERROR == recv_instruction(conn)):
        #            break
        #        
                #response = b"fucki"
                #conn.sendall(response)
    def connect_to_game_2(self):
        #TODO: have a loop of connection retries
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip,self.port))
        self.conn = self.sock
        print("CLIENT CONNECTED")

    def init_p2p(self):
        if(self.conn_type == "host"):
            print("hosting")
            self.host_game_2()
        else:
            print("connecting")
            self.connect_to_game_2()
    
