#!/bin/env python3


'''Server for multithreaded (asynchronouse) chat application.'''

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


clients = {}
addresses = {}

HOST = ''
PORT = 33000    # PORT that we will use.
BUFSIZE = 1024  # 1GB
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)   # Create socket object.
SERVER.bind(ADDR)                       # Bind the socket to ADDR.


def accept_incoming_connections():
    '''Sets up handling for incoming clients.'''
    # Constant loop until user exits.
    while True:
        client, client_address = SERVER.accept()
        print(f'{client_address} has connected.')
        client.send(bytes('Greetings from the cave! \
                        Now type your name and press enter!', 'utf-8'))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    '''Handles a sigle client connection.'''
    name = client.recv(BUFSIZ).decode('utf-8')
    welcome = f'Welcome {name}! If you ever want to quit, type [quit] \
            to exit.'
    client.send(bytes(welcome, 'utf-8'))
    msg = f'{name} has joined the chat!'
    broadcast(bytes(msg, 'utf-8'))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZE)
        if msg != bytes(f'{quit}', 'utf-8'):
            broadcast(msg, name+': ')
        else:
            client.send(bytes('{quit}', 'utf-8'))
            client.close()
            del clients[client]
            broadcast(bytes(f'{name} has left the chat.', 'utf-8'))
            break


# This broadcast to everyone in the network.
def broadcast(msg, prefix=''):  # Prefix is for the name identification.
    '''Broadcasts a message to all the clients.'''
    for sock in clients:
        sock.send(bytes(prefix, 'utf-8')+msg)


# Code to start our server and listen for incoming connections.
if __name__ == '__main__':
    server.listen(5)  # Listens for 5 connections at max.
    print('Waiting for connection...')
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
