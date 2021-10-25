import socket
import sys


def main(port_number):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port_number)))
    id = 1
    while True:
        data, addr = s.recvfrom(1024)
        header = int.from_bytes(data[:2], 'little')
        data = data[2:100]
        if id == header:
            print(data.decode('utf-8'))
            s.sendto(data, addr)
        else:
            s.sendto(b'^again^', addr)
        id = id + 1


if __name__ == '__main__':
    port_number = sys.argv[1]
    main(port_number)
