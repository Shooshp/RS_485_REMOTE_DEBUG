import asyncore
import socket
import threading
from  ORMDataBase import power_source_current_tasks


class ReadHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        try:
            data = self.recv(1024)
            if data:
                if str(data.decode()) == "What your state?":
                    self.send(EventManager.PowerSourceStatus.encode())
                    EventManager.ResetUDP()

                else:
                    if (data.decode().find("Task:") != -1):
                        if  EventManager.CurrentTaskId == 0:
                            task = data.decode().split(":",1)[1]
                            EventManager.CurrentTaskId = int(task)
                            reply = 'Beginning Task: ' + task
                            self.send(reply.encode())
                        else:
                            reply = 'Already busy with task: ' + str(EventManager.CurrentTaskId)
                            self.send(reply.encode())

                        EventManager.ResetUDP()
                    else:
                        reply = 'Unknown command!'
                        self.send(reply.encode())

        except Exception:
            print(Exception.args)


class ListenerServer(threading.Thread, asyncore.dispatcher):
    def __init__(self, port, host=''):
        self.host = host
        self.port = port

        threading.Thread.__init__(self)
        self.daemon = True
        self._thread_sockets = dict()
        asyncore.dispatcher.__init__(self)
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
            EventManager.ResetUDP()
            print('>>> Connected with ' + address[0] + ':' + str(address[1]))
            ReadHandler(connected_socket)


class UDPBroadcaster(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.daemon = True
        EventManager.ResetUDP()
        self.port = port
        self.data = "Hello!"
        self.start()

    def run(self):
        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while EventManager.UDPCallCounter > 0:
            EventManager.UDPCallCounter -= 1
            self.event.wait(1)

        for time in range(0, 5):
            self.UDPSocket.sendto(bytes(self.data.encode()), ('255.255.255.255',self.port))

        print('UDP message was send!')
        EventManager.ResetUDP()
        self.run()


class EventManager:
    UDPCallCounter = 0

    PowerSourceStatus = "Idle"
    CurrentTaskId = 0
    TaskArgument = 0
    Progress = 0

    @staticmethod
    def ResetUDP():
        EventManager.UDPCallCounter = 5

    @staticmethod
    def TaskCompleted(id):
        power_source_current_tasks.update(power_source_current_task_completed = True).\
            where(power_source_current_tasks.power_source_current_task_id == id)
        EventManager.CurrentTaskId = 0
        EventManager.TaskArgument = 0
        EventManager.PowerSourceStatus = "Idle"

