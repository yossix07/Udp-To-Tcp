import socket
import sys


def main(ip_address, port_number, patch_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        with open(patch_file, "rb") as file:
            header_id = 1
            while True:
                chunk = file.read(98)
                if chunk == b'':
                    break
                id_chunk = header_id.to_bytes(2, 'little') + chunk
                s.sendto(id_chunk, (ip_address, int(port_number)))
                data, addr = s.recvfrom(1024)
                if data != chunk:
                    s.sendto(id_chunk, (ip_address, int(port_number)))
                    data, addr = s.recvfrom(1024)
                print(str(data), addr)
                header_id += 1
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
