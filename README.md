# Chess 2

Chess 2 is a version of Chess that two players can play on two different computers. Each player can see a Chess board on their screen and can move pieces when it is their turn, and the two computers send updates to the board state through TCP sockets. However, we are also adding in additional features; we are working to add power ups, debuffs, and traps that each player can periodically select, in an attempt to add new depth and variety to Chess.

The project is written using and designed for Python 3.10-3.12 mainly, though other versions may also work, and it also requires Pygame, preferably version 2.6. Since Pygame can have erratic behavior for virtual machines, we recommend you run the program using your default operating system terminal (i.e. on Windows, avoid using WSL and stick to using PowerShell).

To run the program, type "python main.py" to host. For example, one player will host the game on their computer, so they might have "python main.py host 0.0.0.0 2020", while the other player will join the game, so they will type "python main.py connect <ip> 2020" where <ip> is the ipv4 address of the first player/computer.

# setup

1. clone the repo

2. navigate to the repo and run `setup`

# play locally

1. execute `Chess-2-local` . This will popup with 2 windows to play locally. In one window create a game, in the other join the game.
2. in the non-host player, enter the localhost ip address `127.0.0.1` and the port `2020`. then you can join the game.
3. Play Chess 2 !

4. note: when playing on the same machine it is easy to forget which turn it is. make sure to click in the window you want to play in before making a movement.

# play LAN

1. follow the same rules above but run `Chess-2`. one player will create and one player will join
2. player 2 types in the ip of the host and the port is `2020`
