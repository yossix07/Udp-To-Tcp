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
        return 10

    @staticmethod
    def DATA_SIZE_LIMIT():
        return 1024

    @staticmethod
    def ARG_ONE():
        return 1

    @staticmethod
    def ARG_TWO():
        return 2

    @staticmethod
    def ARG_THREE():
        return 3

    @staticmethod
    def FIRST_ID():
        return 0

    @staticmethod
    def STARTING_PORT():
        return 0

    @staticmethod
    def ENDING_PORT():
        return 65535


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
        print("Error - Wrong Patch!")
        sys.exit(1)
    finally:
        s.close()
        file.close()


# check if the received ip address is in correct format.
def check_ip(ip_address):
    ip = ip_address.split(".")

    # in case the address doesnt has 4 ".", it is invalid
    if len(ip) != 4:
        return False
    # in case one of the segments in the address isn't in the wanted range, it is invalid
    for num in ip:
        if int(num) > 255 or int(num) < 0:
            return False
    return True


# runs the client program
if __name__ == '__main__':
    try:
        port_number = sys.argv[CONST.ARG_ONE()]
        ip_address = sys.argv[CONST.ARG_TWO()]
        patch_file = sys.argv[CONST.ARG_THREE()]

        # in case the port or ip address arent valid, exit
        if int(port_number) < CONST.STARTING_PORT() or int(port_number) > CONST.ENDING_PORT() \
                or not check_ip(ip_address):
            raise ValueError

        # run client
        client(ip_address, port_number, patch_file)
    except ValueError:
        print("Error - Wrong Arguments!")
        sys.exit(1)
