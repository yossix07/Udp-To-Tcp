import socket
import sys


def main(port_number):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port_number)))
    package_id = 0
    while True:
        data, addr = s.recvfrom(1024)
        header = int.from_bytes(data[:2], 'little')
        info = data[2:100]
        # check if this the required package
        if package_id == header:
            print(info.decode('utf-8'), end='')
            package_id += 1
            s.sendto(info, addr)
        while header < package_id:
            s.sendto(info, addr)
            data, addr = s.recvfrom(1024)
            header = int.from_bytes(data[:2], 'little')


if __name__ == '__main__':
    port_number = sys.argv[1]
    main(port_number)
