from chesspiece import *
import tkinter as tk
import os #need this for the images if we want to use relative paths?

def printout():
    print("hello world")
class game:
    board = None
    turn = None

    def __init__(self):
        self.board = [ [None for j in range(8)] for i in range(8)]
        for i in range (8):
            self.board[1][i] = pawn(1,i)
            self.board[6][i] = pawn(6,i)
        self.board[7][1] = knight(7,1)
        self.board[7][6] = knight(7,6)
        self.board[0][1] = knight(0,1)
        self.board[0][6] = knight(0,6)

        self.board[7][0] = rook(7,0)
        self.board[7][7] = rook(7,7)
        self.board[0][0] = rook(0,0)
        self.board[0][7] = rook(0,7)

        self.board[7][2] = bishop(7,2)
        self.board[7][5] = bishop(7,5)
        self.board[0][2] = bishop(0,2)
        self.board[0][5] = bishop(0,5)

    def selectsquare(self,i,j):
        print("selected square ", i , "," , j)
        # if (self.board[i][j] == None):
        #     pass


    def display(self):
        root = tk.Tk()
        root.geometry("800x800")
        frm = tk.Frame(root)
        frm.grid()

        print(self.board)

        # #Specify Grid
        # tk.Grid.rowconfigure(root,0,weight=1)
        # tk.Grid.columnconfigure(root,0,weight=1)

        for i in range(10):
            tk.Grid.columnconfigure(root,i,weight=1)
            tk.Grid.rowconfigure(root,i,weight=1)

        buttons = []
        for i in range(8):
            newrow = []
            for j in range(8):
                button = None
                if (self.board[i][j] != None):
                    #Attempt at PNGs, they don't work too well D:
                    # base_path = os.path.dirname(__file__)
                    # img_path = os.path.join(base_path,self.board[i][j].image)
                    # photo = tk.PhotoImage(file = img_path)
                    # photo = photo.subsample(50,50) 
                    # button = tk.Button(root, image = photo)                        #need lambda to pass args for the command function
                    button = tk.Button(root, text = self.board[i][j].name, command = lambda a = i, b = j:self.selectsquare(a,b))
                else:
                    button = tk.Button(root, text = "", command = lambda a = i, b = j:self.selectsquare(a,b))
                newrow.append(button)
                button.grid(row = i,column = j, sticky = "NSEW")
            buttons.append(newrow)

        root.mainloop()