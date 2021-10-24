import socket
import sys


def main(ip_address, port_number, patch_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        file = open(patch_file, "r")
        file_string = file.read().replace('\n', ' ')
        size = 100
        if len(file_string) >= size:
            chunks = [file_string[i:i + size] for i in range(0, len(file_string), size)]
            for chunk in chunks:
                s.sendto(bytes(chunk, 'utf-8'), (ip_address, int(port_number)))
                data, addr = s.recvfrom(1024)
                print(str(data), addr)
            # TODO change print method need to include new lines.
        else:
            s.sendto(bytes(file_string, 'utf-8'), (ip_address, int(port_number)))
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
