import asyncore
import socket
import threading


class ReadHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(1450)
        if data:
            if not EventManager.data:
                EventManager.data = data
            else:
                print('Busy!')


class ListenerServer(threading.Thread, asyncore.dispatcher):
    def __init__(self, host='', port=10235):
        threading.Thread.__init__(self)
        self.daemon = True
        self._thread_sockets = dict()

        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.start()

    def run(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((self.host, self.port))
        self.listen(5)
        asyncore.loop()

    def handle_accept(self):
        accept = self.accept()
        if accept is not None:
            connected_socket, address = accept
            print('>>> Connected with ' + address[0] + ':' + str(address[1]))
            ReadHandler(connected_socket)


class EventManager(object):
    data = 0
