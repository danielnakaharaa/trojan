import socket

ip = "60.111.183.77"
porta = 135
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip,porta))