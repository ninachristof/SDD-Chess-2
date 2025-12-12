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
    new_game = game.game(0,0,0)
    conn_thread = new_game.get_conn_thread()
    new_game.main_loop_menu()
    if(new_game.new_p2p):
        new_game.new_p2p.close_all()
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

    new_game = game.game(conn_type, ip, port)
    new_game.setup_game()
    new_game.conn_thread.start()
    conn_thread = new_game.get_conn_thread()

    new_game.main_loop()
    if(new_game.new_p2p):
        new_game.new_p2p.close_all()
        conn_thread.join()

main()
