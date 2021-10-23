import socket
import sys

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    file = open(sys.argv[3], "r")
    file_string = file.read().replace('\n',' ')
    size = 100
    if len(file_string) >= size:
        chunks = [file_string[i:i+size] for i in range(0,len(file_string),size)]
        for chunk in chunks:
            s.sendto(bytes(chunk, 'utf-8'), (sys.argv[1], int(sys.argv[2])))
            data, addr = s.recvfrom(1024)
    else:
        s.sendto(bytes(file_string, 'utf-8'), (sys.argv[1], int(sys.argv[2])))
        data, addr = s.recvfrom(1024)

    print(str(data), addr)
    s.close()
    file.close()
