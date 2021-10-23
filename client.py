import socket
import sys

if __name__ == '__main__':
    file = open(sys.argv(2))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(file.read(), (sys.argv(0) , sys.argv(1)))
    data, addr = s.recvfrom(1024)
    print(str(data), addr)
    s.close()

