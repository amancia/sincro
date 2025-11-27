################################################################################

import math
from Client import Client
import threading, datetime, dateutil, socket, time

################################################################################

class Master:
    def __init__(self, port:int, clients:list[Client]):
        self.tolerance = 1000 / 1000
        self.current_time = datetime.datetime.now()
        print('OKAY: Referências de tempos registradas.')
        
        self.clients = clients
        self.clientLogs = {}
        print('OKAY: Lista de clientes inicializada.')

        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', port))
        self.server.listen(10)
        print('OKAY: Servidor mestre criado.')

        self.connectingThread = threading.Thread(target=self.loopConnecting)
        self.connectingThread.start()
        print('OKAY: Thread de novas conexões criada.')

        self.syncingThread = threading.Thread(target=self.syncClocks)
        self.syncingThread.start()
        print('OKAY: Thread de sincronização criada.')


    # Conexão automática com clientes
    def loopConnecting(self):
        while True:
            connector, master_addr = self.server.accept()
            client_addr = f'{master_addr[0]}:{master_addr[1]}'

            current_thread = threading.Thread(target=self.receiveTime, 
                                              args=(connector, client_addr))
            current_thread.start()
            print('OKAY: Thread de conexão com', client_addr, 'criada.')


    # Escuta do tempo dos clientes
    def receiveTime(self, connector, address):
        while True:
            self.current_time = datetime.datetime.now()

            clock_time_string = connector.recv(1024).decode()
            clock_time = dateutil.parser.parse(clock_time_string)
            clock_time_diff = (clock_time - self.current_time).total_seconds()

            self.clientLogs[address] = {   
                                        "connector": connector,
                                        "clock_time": clock_time,
                                        "time_difference": clock_time_diff
                                    }
            
            time.sleep(1)


    # Sincronização
    def syncClocks(self):
        while True:
            print("Sincronização iniciada.")
            print("Clientes conectados: " + str(len(self.clientLogs)))

            if len(self.clientLogs) > 0:
                average_diff = self.calcAverageClockDiff()
                self.current_time += datetime.timedelta(seconds=average_diff)
                
                print('master:realtime', datetime.datetime.now(), '-'*30)

                for client_addr, client in self.clientLogs.items():
                    try:
                        synchronized_time = (self.current_time - client['clock_time']).total_seconds()
                        client['connector'].send(str(synchronized_time).encode())
                    except Exception as e:
                        print("ERRO: Não foi possível se comunicar com o cliente", str(client_addr) + '.')
            else:
                print("INFO: Nenhum cliente conectado.")

            print("\n\n")
            time.sleep(1)
    
    
    def calcAverageClockDiff(self):
        if len(self.clientLogs) > 0:
            client_diffs = [client['time_difference'] for _, client in self.clientLogs.items()]
            filtered_client_diffs = list(filter(lambda diff: abs(diff) <= self.tolerance, client_diffs))
            
            if len(filtered_client_diffs) > 0:
                average_diff = sum(filtered_client_diffs) / len(filtered_client_diffs)
                return average_diff
            else:
                return 0
        else:
            return 0

################################################################################
