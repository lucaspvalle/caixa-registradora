import socket
import sys
from random import uniform

print("Balança em funcionamento")

HOST = "localhost"
PORT = 8888

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

while 1:
    print ("Aguardando... ")
    conn, addr = s.accept()
    print ("Conectado a " + addr[0] + ':' + str(addr[1]))
    conn.sendall(f"{uniform(0.1,1)}".encode())
    print("Enviado!")

print ("Servidor finalizado")
s.close()
