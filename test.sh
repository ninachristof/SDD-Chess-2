#/bin/sh

python3 main.py host 0.0.0.0 5555 &

sleep 1

python3 main.py connect 127.0.0.1 5555

