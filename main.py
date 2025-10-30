import game
import threading
import p2p
import global_vars
from p2p import *

def main():
    if(len(sys.argv) < 4 ):
        print("ERROR WRONG NUMBER OF ARGUMENTS")
        print("usage: p2p.py <host/connect> <ip> <port>")
        print("ex: p2p.py host 0.0.0.0  2020")
        return

    conn_type = sys.argv[1].strip()
    if(conn_type != "connect" or conn_type != "host"):
        print("connection type needs to be host or connect")
    ip = sys.argv[2].strip()
    port = int(sys.argv[3])
    #TODO: check for valid ports automatically instead
    #TODO: if host then just automatically set it to 0.0.0.0


    global_vars.init_vars() 

    newgame = game.game(conn_type, ip, port)
    #conn_thread = threading.Thread(target=run_socket, args=(conn_type, ip, port, send_event))
    conn_thread = newgame.get_conn_thread()

    newgame.display()
    newgame.new_p2p.close_all()
    conn_thread.join()
    print("FINISHED PROGRAM")
    #add something to trigger and stop host listening instead of on init
    
main()
