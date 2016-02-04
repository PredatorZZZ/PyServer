import socket
import threading
import sys

BUFFER_SIZE = 100
addr_list = []
curr_addr = None
data = None
flag = False
file = None


class Server(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        threading.Thread.__init__(self)

    def run(self):
        global addr_list
        global curr_addr
        global data
        global flag
        log = 'Connection address: {}\n'.format(self.addr)
        file = open('file', 'a')
        file.write(log)
        file.close()
        #print 'Connection address: {}'.format(self.addr)
        while True:
            if curr_addr == self.addr and flag == True:
                self.conn.send(data)
                flag = False
                if data == 'exit':
                    addr_list.remove(self.addr)
                    break
        log = 'Address disconnected {}\n'.format(self.addr)
        file = open('file', 'a')
        file.write(log)
        file.close()
        #print 'Address disconnected {}'.format(self.addr)
        self.conn.close()


class Selector(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global addr_list
        global curr_addr
        global data
        global flag
        while True:
            data = raw_input('Enter message: ')
            for i in range(len(addr_list)):
                print '{0} - {1}'.format((i + 1), addr_list[i])
            index = int(raw_input('Choose address: '))
            curr_addr = addr_list[index - 1]
            flag = True


if __name__ == '__main__':
    if len(sys.argv) == 3:
        file = open('file', 'w')
        file.close()
        Selector().start()
        print 'Server deployed on {0}:{1}'.format(sys.argv[1], sys.argv[2])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.bind((sys.argv[1], int(sys.argv[2])))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            addr_list.append(addr)
            Server(conn, addr).start()
    else:
        print 'Incorrect count of params({} need)'.format(2)