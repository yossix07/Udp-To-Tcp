import socket
import sys

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    file = open(sys.argv[3])
    if (len(file.read())) > 100:
        n = 100
        chunks = [str[i:i + n] for i in range(0, len(str), n)]
        for chunk in chunks:
            s.sendto(bytes(chunk), (sys.argv[0], sys.argv[1]))
            data, addr = s.recvfrom(1024)

    else:
        s.sendto(bytes(file.read()), (sys.argv[0], sys.argv[1]))
        data, addr = s.recvfrom(1024)

    print(str(data), addr)
    s.close()
