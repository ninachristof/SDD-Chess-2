import game
import threading
import p2p
import global_vars
from p2p import *
#TEMP
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

def OLD_main():
    if(len(sys.argv) < 4 ):
        print("ERROR WRONG NUMBER OF ARGUMENTS")
        print("usage: python main.py <host/connect> <ip> <port>")
        print("ex: python main.py host 0.0.0.0 2020 for host/white and ")
        print("python main.py connect 127.0.0.1 2020 for connector/black")
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
    conn_thread = newgame.get_conn_thread()

    newgame.OLD_main_loop()
    print("------- FINISHED MAIN LOOP -------")
    if(newgame.new_p2p):
        newgame.new_p2p.close_all()
        conn_thread.join()
    print("FINISHED PROGRAM")
    #TODO:add something to trigger and stop host listening instead of on init
    
def main():
    global_vars.init_vars() 
    newgame = game.game(0,0,0)#this will be removed later
    conn_thread = newgame.get_conn_thread()
    newgame.main_loop()
    print("------- FINISHED MAIN LOOP -------")
    if(newgame.new_p2p):
        newgame.new_p2p.close_all()
        conn_thread.join()
    print("FINISHED PROGRAM")

#OLD_main()
main()
