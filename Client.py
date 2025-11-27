################################################################################

import random
import threading, datetime, socket, time

################################################################################

class Client:
    def __init__(self, idx:int, port:int, diffs:float=0, speed:float=1):
        self.idx = idx
        self.current_time = datetime.datetime.now()
        self.times:list[datetime.datetime] = [self.current_time]
        
        self.diffs = diffs  # Atraso, diferença <- clock skew
        self.speed = speed  # Velocidade <- drift rate
        
        print(f'OKAY: Cliente {idx+1} configurado.')

        self.server = socket.socket()
        self.server.connect(('127.0.0.1', port))
        print('OKAY: Cliente conectado.')

        self.sendingThread = threading.Thread(target=self.sendTime)
        self.sendingThread.start()
        print('OKAY: Thread de envio de tempo criada.')

        self.receivingThread = threading.Thread(target=self.receiveTime)
        self.receivingThread.start()
        print('OKAY: Thread de recebimento de tempo criada.')
    
    # Atraso/adiante aleatório
    def clockSkew(self):
        self.diffs = 2 * random.random() - 1
    
    # Velocidade aleatória
    def driftRate(self):
        self.speed = 2 * random.random()
    
    # Envia tempo ao servidor do mestre
    def sendTime(self):
        while True:
            increment = datetime.datetime.now() - self.current_time
            self.current_time += increment * self.speed + datetime.timedelta(seconds=self.diffs)
            self.times.append(self.current_time)

            self.server.send(str(self.current_time).encode())
            print('INFO: Horas enviadas:', self.current_time)
            time.sleep(1)
    
    # Recebe tempo/segundos de correção
    def receiveTime(self):
        while True:
            delta = float(self.server.recv(1024).decode())
        
            self.current_time += datetime.timedelta(seconds=delta)
            self.times.append(self.current_time)
        
            print('INFO: Horas sincronizadas:', self.current_time)
            time.sleep(1)

################################################################################
