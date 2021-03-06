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
    def FIRST_ID():
        return 0

    @staticmethod
    def DATA_SIZE_LIMIT():
        return 1024

    @staticmethod
    def ARG_ONE():
        return 1

    @staticmethod
    def STARTING_PORT():
        return 0

    @staticmethod
    def ENDING_PORT():
        return 65535


# activate the server with the received port number and replay to the client when got a new package and when got
# an already received package accordingly
def server(port_number):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port_number)))

    # set id to the first id number
    current_wanted_id = CONST.FIRST_ID()

    # open server for receiving data from clients while making sure two things - the packages are being received
    # in the correct order, and the client get a massage for every package that has been received
    while True:
        data, address = s.recvfrom(CONST.DATA_SIZE_LIMIT())

        # id of current package
        header = int.from_bytes(data[:CONST.ID_SIZE()], 'little')

        # the current package's data
        info = data[CONST.ID_SIZE():CONST.ID_SIZE() + CONST.DATA_SIZE()]

        # if this the required package, print it, tell client it has been received and move to the next id number
        if current_wanted_id == header:
            print(info.decode('utf-8'), end='')
            current_wanted_id += 1
            s.sendto(info, address)

        # as long as the confirmation of receiving the package is lost, send it again
        while header < current_wanted_id:
            s.sendto(info, address)
            data, address = s.recvfrom(CONST.DATA_SIZE_LIMIT())
            header = int.from_bytes(data[:CONST.ID_SIZE()], 'little')


# runs the server process with the received port number
if __name__ == '__main__':
    try:
        port_number = sys.argv[CONST.ARG_ONE()]

        # in case the port isn't valid, exit
        if int(port_number) < CONST.STARTING_PORT() or int(port_number) > CONST.ENDING_PORT():
            raise ValueError

        # run server
        server(port_number)
    except ValueError:
        print("Error - Wrong Arguments!")
        sys.exit(1)
