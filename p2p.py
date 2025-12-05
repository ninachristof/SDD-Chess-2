import socket
import sys
from struct import *
import global_vars

ERROR = 1
SUCCESS = 0
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
    waiting = False

    def __init__(self, conn_type, ip, port):
        self.conn_type = conn_type
        self.ip = ip
        if(conn_type == "host"):
            self.ip = ""
        self.port = port
        
    def closeAll(self):
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_WR)
            except Exception as e:
                print("self.sock.shutdown(socket.SHUT_WR) Exception:", e)

            try:
                self.sock.close()
            except Exception as e:
                print("self.sock.close() Exception:", e)
            self.sock = None
        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                print("self.conn.close() Exception:", e)

            self.conn = None

    def recvInstruction(self):
        print("host:", self.conn)
        self.waiting = True

        try:
            data = self.conn.recv(PKT_HDR_SIZE)
        except Exception as e:
            print("recv header exception:", e)
            self.waiting = False
            return ERROR

        self.waiting = False

        if not data:
            print("empty packet (no header)")
            return ERROR

        try:
            recvd_hdr, instruction_size = unpack("5si", data)
        except Exception as e:
            print("unpack header exception:", e)
            return ERROR

        if recvd_hdr != PKT_HDR or len(data) != PKT_HDR_SIZE:
            print("header error: bad magic or wrong header size")
            return ERROR

        self.waiting = True
        try:
            instruction = self.conn.recv(instruction_size)
        except Exception as e:
            print("recv body exception:", e)
            self.waiting = False
            return ERROR

        self.waiting = False

        if not instruction:
            print("empty packet (no body)")
            return ERROR

        return instruction

    def sendInstruction(self, current_instruction):
            print(f"sending {current_instruction}")
            hdr = pack("5si", PKT_HDR, len(current_instruction))
            bytes_sent = self.conn.sendall(hdr)
                
            self.conn.sendall(current_instruction)

    #host is host ip probably 0.0.0.0 so that it listens to inconming traffic
    def hostGame(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(5)
        print(self.sock)
        self.conn, addr = self.sock.accept()
        self.conn.setblocking(True)
        self.conn.settimeout(None)
        print("HOST ACCEPTED")
        #TODO: how ot handle disconnections/ bad wifi?
        #TODO: how are the timers going to be synced up? 
        #todo: if error on receiving end, send a request to resend mesage
        #TODO: timestamp

    def connectToGame(self):
        #TODO: try to connect, if it cant then call close socket because itll leave an open socket
        #TODO: have a loop of connection retries
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.ip,self.port))
        self.conn = self.sock
        print("CLIENT CONNECTED")

    def initP2p(self):
        if(self.conn_type == "host"):
            print("hosting")
            self.hostGame()
        else:
            print("connecting")
            self.connectToGame()
    
