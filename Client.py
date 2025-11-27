################################################################################

import random
import threading, datetime, socket, time

################################################################################

class Client:
    def __init__(self, idx:int, port:int, diffs:float=0, speed:float=1):
        self.idx = idx
        self.current_time = datetime.datetime.now()
        
        self.diffs = diffs
        self.speed = speed

        self.times:list[datetime.datetime] = []

        self.server = socket.socket()
        self.server.connect(('127.0.0.1', port))
        print('OKAY: Cliente conectado.')

        self.sendingThread = threading.Thread(target=self.sendTime)
        self.sendingThread.start()
        print('OKAY: Thread de envio de tempo criada.')

        self.receivingThread = threading.Thread(target=self.receiveTime)
        self.receivingThread.start()
        print('OKAY: Thread de recebimento de tempo criada.')
    
    def clockSkew(self):
        self.diffs = random.random()
    
    def driftRate(self):
        self.speed = 2 * random.random()
    
    def sendTime(self):
        while True:
            increment = datetime.datetime.now() - self.current_time
            self.current_time += increment * self.speed + datetime.timedelta(seconds=self.diffs)
            self.times.append(self.current_time)

            self.server.send(str(self.current_time).encode())
            print('INFO: Horas enviadas:', self.current_time)
            time.sleep(1)
    
    def receiveTime(self):
        while True:
            delta = float(self.server.recv(1024).decode())
        
            # if (delta > 0):
            self.current_time += datetime.timedelta(seconds=delta)
            self.times.append(self.current_time)
        
            print('INFO: Horas sincronizadas:', self.current_time)
            time.sleep(0.125)

################################################################################
