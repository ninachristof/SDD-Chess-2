HELP ME PLEASE GOD HELP

Chess 2 is a version of Chess that two players can play on two different computers. Each player can see a Chess board on their screen and can move pieces when it is their turn, and the two computers send updates to the board state through TCP sockets. However, we are also adding in additional features; we are working to add power ups, debuffs, and traps that each player can periodically select, in an attempt to add new depth and variety to Chess.

The project is written using and designed for Python 3.10-3.12 mainly, though other versions may also work, and it also requires Pygame, preferably version 2.6. Since Pygame can have erratic behavior for virtual machines, we recommend you run the program using your default operating system terminal (i.e. on Windows, avoid using WSL and stick to using PowerShell).

To run the program, type "python main.py" to host. For example, one player will host the game on their computer, so they might have "python main.py host 0.0.0.0 2020", while the other player will join the game, so they will type "python main.py connect <ip> 2020" where <ip> is the ipv4 address of the first player/computer.

Testing main
