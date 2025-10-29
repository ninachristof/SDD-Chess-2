import game
import sys

def main():
    newgame = game.game()
    newgame.display()

def main_2():
    newgame = None
    ip = "0.0.0.0" #defualt
    port = 5432#default
    if(len(sys.argv) == 4):
        conn_type = sys.argv[1].strip()
        ip = sys.argv[2].strip()
        port = int(sys.argv[3])
        newgame = game.game(ip,port,conn_type)
        newgame.display()
    else:
        print("WRONG NUMBER OF ARGUMENTS")
        print("usage: p2p.py <host/connect> <ip> <port>")
        print("ex: p2p.py host 0.0.0.0  2020")
    if(None != newgame):
        newgame.close_all()
#main()
main_2()
