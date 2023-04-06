import socket
import threading
import queue

def start_server():
    global messages
    global server
    global clients
    global names
    global names_str

    messages = queue.Queue()
    clients = []
    names = {}
    names_str = ''

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', 9999))


    def receive():
        global messages
        global server
        

        while True:
            try:
                message, addr = server.recvfrom(1024)
                messages.put((message, addr))
            except:
                pass

    def broadcast():
        global messages 
        global clients
        global names
        global names_str

        clients = []
        names = {}
        names_str = ''

        attende_joueur = True
        choisit_le_mot = 0

        while True:
            while not messages.empty():
                message, addr = messages.get()
                #print(message.decode())
                if addr not in clients and attende_joueur:
                    clients.append(addr)
                    print(addr)
                #print(clients)
                if message.decode().startswith('USER_NAME:'):
                    #print('c')
                    name = message.decode()[message.decode().index(':')+1:]
                    names[addr] = name
                    names_str += f'{name},'
                    
                    server.sendto(f'ATTENDRE_JOUEURS_FIRST:{names_str}'.encode(), clients[-1])

                    for client in clients[:-1]:
                            server.sendto(f'ATTENDRE_JOUEURS:{names_str}'.encode(), client)

                elif message.decode().startswith('START_GAME'):
                        #print('d')
                        attende_joueur = False
                        for i in range(len(clients)):
                            if i == (choisit_le_mot%(len(clients))):
                                server.sendto(f'START_GAME_CHOIX:{names[addr]}'.encode(), clients[i])
                            else:
                                server.sendto(f'START_GAME_WAIT:{names[addr]}, {names[clients[choisit_le_mot]]}'.encode(), clients[i])
                        choisit_le_mot += 1

                elif message.decode().startswith('MOT:'):
                        mot = message.decode()[message.decode().index(':')+1:]
                        for client in clients:
                            server.sendto(f'PLAY_GAME:{mot}'.encode(), client)
                            print(f'PLAY_GAME:{mot}', client)
                elif message.decode().startswith('PLAY_GAME'):
                    if message.decode().startswith('PLAY_GAME_LETTRE:'):
                        lettre = message.decode()[message.decode().index(':')+1:]
                        for client in clients:
                            server.sendto(f'PLAY_GAME_LETTRE:{lettre}, {addr}'.encode(), client)
                            print(f'PLAY_GAME_LETTRE:{lettre}, {addr}', client)
                    elif message.decode().startswith('PLAY_GAME_ERROR:'):
                        lettre = message.decode()[message.decode().index(':')+1:]
                        for client in clients:
                            server.sendto(message, client)
                            print(message.decode(), client)


                            #server.sendto(message, client)
                    #server.sendto(message, client)
                    #except:
                    #clients.remove(client)
                    #print('error')

    t1 = threading.Thread(target = receive)
    t2 = threading.Thread(target = broadcast)

    t1.start()
    t2.start()    

start_server()   