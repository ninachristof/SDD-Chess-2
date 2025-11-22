import game
import threading
import p2p
import global_vars
from p2p import *
#TEMP
import warnings
import argparse
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

def main_menu():
    global_vars.init_vars() 
    newgame = game.game(0,0,0)
    conn_thread = newgame.get_conn_thread()
    newgame.main_loop_menu()
    if(newgame.new_p2p):
        newgame.new_p2p.closeAll()
        conn_thread.join()

def main():

    parser = argparse.ArgumentParser(prog="Chess 2")
    parser.add_argument("-m" "--menu", action="store_true", help = "takes player to main menu")
    parser.add_argument("-H" "--host", action="store_true", help = "skip main menu and host a game")
    parser.add_argument("-c" "--connect", action="store_true", help = "skip main menu and try to connect to host")
    parser.add_argument("-i",type=str, default="127.0.0.1",help = "ip address of host")
    parser.add_argument("-p",type=int, default = 2020, help = "port number")
    parser.add_argument("-b", type=str,help = "filename")# does nothing right now
    args = parser.parse_args()

    if args.m__menu:
        main_menu()
        return
    conn_type = ""
    ip = args.i
    port = args.p
    if args.c__connect:
        conn_type = "connect"
    elif args.H__host:
        conn_type = "host"
    else:
        parser.print_help()

    global_vars.init_vars() 

    newgame = game.game(conn_type, ip, port)
    newgame.setup_game()
    newgame.conn_thread.start()
    conn_thread = newgame.get_conn_thread()

    newgame.main_loop()
    if(newgame.new_p2p):
        newgame.new_p2p.closeAll()
        conn_thread.join()

main()
