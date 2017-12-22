import asyncore
import socket
import threading
from ORMDataBase import CurrentTasks


class ReadHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        try:
            data = self.recv(64)
            if data:
                if str(data.decode()) == "What your state?":
                    self.send(EventManager.PowerSourceStatus.encode())
                    EventManager.resetUDP()
                else:
                    if data.decode().find("Task:") != -1:
                        self.send(EventManager.task_handler(data))
                        EventManager.resetUDP()
                    else:
                        self.send('Unknown command!'.encode())

        except socket.error:
            print('socket.error - ' + str(socket.error.args))


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
            EventManager.resetUDP()
            print('>>> Connected with ' + address[0] + ':' + str(address[1]))
            ReadHandler(connected_socket)


class UDPBroadcaster(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.event = threading.Event()
        self.daemon = True
        EventManager.resetUDP()
        self.port = port
        self.data = "Hello!"
        self.start()

    def run(self):
        while True:
            while EventManager.UDPCallCounter > 0:
                EventManager.UDPCallCounter -= 1
                self.event.wait(1)

            for time in range(0, 5):
                self.UDPSocket.sendto(bytes(self.data.encode()), ('255.255.255.255', self.port))

            print('UDP message was send!')
            EventManager.resetUDP()


class EventManager:
    UDPCallCounter = 0

    PowerSourceStatus = "Idle"

    CurrentTaskId = 0
    CurrentTaskName = ''
    CurrentTaskUUID = 0
    CurrentTaskArgument = 0
    CurrentTaskProgress = 0

    @staticmethod
    def resetUDP():
        EventManager.UDPCallCounter = 5

    @staticmethod
    def task_handler(task):
        if EventManager.CurrentTaskId == 0:
            EventManager.CurrentTaskId = int(task.decode().split(":", 1)[1])
            Task = CurrentTasks.get(CurrentTasks.id == EventManager.CurrentTaskId, CurrentTasks.IsCompleted == False)
            EventManager.CurrentTaskName = Task.Name.Name
            EventManager.CurrentTaskUUID = Task.UUID.UUID
            EventManager.CurrentTaskArgument = float(Task.Value)
            return ('Beginning Task: ' + str(EventManager.CurrentTaskId)).encode()
        else:
            return ('Already busy with task: ' + str(EventManager.CurrentTaskId)
                    + ' current progress: ' + str(EventManager.CurrentTaskProgress)).encode()

    @staticmethod
    def task_completed(task_id):
        print('Task ', task_id, ' Completed!')
        CurrentTasks.update(IsCompleted=True).where(CurrentTasks.id == task_id).execute()
        EventManager.CurrentTaskId = 0
        EventManager.CurrentTaskUUID = 0
        EventManager.CurrentTaskArgument = 0
        EventManager.CurrentTaskProgress = 0
        EventManager.PowerSourceStatus = "Idle"


class ProgressUpdater(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
