import socket
import sys


def main(port_number):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port_number)))
    while True:
        data, addr = s.recvfrom(1024)
        info = data[:-98]
        print(info.decode('utf-8'))
        s.sendto(info, addr)


if __name__ == '__main__':
    port_number = sys.argv[1]
    main(port_number)
