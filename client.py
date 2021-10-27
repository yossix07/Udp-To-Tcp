import socket
import sys


# constants
class CONST:
    @staticmethod
    def DATA_SIZE():
        return 98

    @staticmethod
    def ID_SIZE():
        return 2

    @staticmethod
    def TIME_DELAY():
        return 0.5

    @staticmethod
    def DATA_SIZE_LIMIT():
        return 1024

    @staticmethod
    def ARG_ONE():
        return 1

    @staticmethod
    def ARG_TWO():
        return 1

    @staticmethod
    def ARG_THREE():
        return 1

    @staticmethod
    def FIRST_ID():
        return 0


# read the received file's text and
# send it to application with the revived port, on the server with the received ip address
def client(ip_address, port_number, patch_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        with open(patch_file, "rb") as file:

            # read first 98 bytes from the file
            chunk = file.read(CONST.DATA_SIZE())
            header_id = CONST.FIRST_ID()

            # send all the text bytes from the file to the relevant application on the relevant server
            while chunk != b'':

                # stores the package number and it's text data
                id_chunk = header_id.to_bytes(CONST.ID_SIZE(), 'little') + chunk

                # sends the package to the server until the server approval of getting it
                while True:
                    s.sendto(id_chunk, (ip_address, int(port_number)))
                    s.settimeout(CONST.TIME_DELAY())
                    try:
                        data, address = s.recvfrom(CONST.DATA_SIZE_LIMIT())

                        # when server approve getting current package, move to the next one and increase the id count
                        if data == chunk:
                            header_id += 1
                            break
                        else:
                            continue
                    except socket.timeout:

                        # in case of failed delivery, try again
                        continue
                chunk = file.read(CONST.DATA_SIZE())
    except ValueError:
        print("Error - wrong patch")
        sys.exit(1)
    finally:
        s.close()
        file.close()


# runs client's program - user enters ip address of a server, an application's port number and a patch to text file
# and send it to the relevant application on the relevant server
if __name__ == '__main__':
    try:
        ip_address = sys.argv[CONST.ARG_ONE()]
        port_number = sys.argv[CONST.ARG_TWO()]
        patch_file = sys.argv[CONST.ARG_THREE()]
        client(ip_address, port_number, patch_file)
    except ValueError:
        print("Error - wrong arguments")
        sys.exit(1)
