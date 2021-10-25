import socket
import sys

def main(ip_address, port_number, patch_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        with open(patch_file, "rb") as file:
            while True:
                chunk = file.read(100)
                if chunk == b'':
                    break
                s.sendto(chunk, (ip_address, int(port_number)))
                data, addr = s.recvfrom(1024)
                print(str(data), addr)
    except ValueError:
        print("Error - wrong patch")
        sys.exit(1)
    finally:
        s.close()
        file.close()


if __name__ == '__main__':
    try:
        ip_address = sys.argv[1]
        port_number = sys.argv[2]
        patch_file = sys.argv[3]
        main(ip_address, port_number, patch_file)
    except ValueError:
        print("Error - wrong arguments")
        sys.exit(1)
