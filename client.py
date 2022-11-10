import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5806))

nickname = input("Choose a nickname:  ")


def recieve():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'Provide Nickname':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)

        except:
            print("An error Occured")
            client.close()
            break 

def write():

    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))




recv_thread = threading.Thread(target = recieve)
recv_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()


