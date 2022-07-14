
from http import client
import sys
import socket

from _thread import start_new_thread



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



if len(sys.argv) != 3:
    print("O uso correto eh: python server.py [IP] [PORTA]")
    exit()


"""
Pega os parametros passados na linha de comando.
"""
IP_ADDRESS = str(sys.argv[1])
PORT = int(sys.argv[2])

"""
server.bind connecta o servidor no endereco especificado em IP_ADDRESS e port PORT
"""
server.bind( (IP_ADDRESS, PORT) )


"""
Determina o numero de clientes ativos no chat.
"""
server.listen(100)

"""
Lista de clientes ativos
"""
lista_de_clientes = []

print("Servidor Inicializado!")


def remove_cliente(client):
    """
    Esta funcao simplesmente remove o cliente da minha lista de clientes ativos. 
    """
    if client in lista_de_clientes:
        lista_de_clientes.remove(client)




def broadcast(mensagem, conexao):
    """
    Esta função encaminha a mensagem de um cliente para todos
    os clientes ativos conectados ao servidor. 
    """
    for cliente in lista_de_clientes:
        if cliente != conexao:
            try:
                cliente.send(mensagem)
            except:
                cliente.close()

                # Se a conexao estiver quebrada, vamos remover o cliente da minha lista de clientes ativos
                remove_cliente(cliente)




def thread_do_cliente(conexao, endereco):
    
    # mando uma mensagem de boas vindas para o cliente atraves do objeto de conexao
    conexao.send("Bem vindo ao chat master python".encode())

    while True:
        try:

            mensagem = conexao.recv(2048)

            if mensagem:

                """
                print da mensagem que o cliente mandou no terminal do meu servidor
                """
                mensagem_para_encaminhar = "[" + endereco[0] + "]: " + mensagem.decode()

                sys.stdout.write(mensagem_para_encaminhar)

                broadcast(mensagem_para_encaminhar, conexao)
        except Exception as e:
            print(e)
            continue





while True:

    """
    Aceitar conexão de clientes.
     objeto de conexao
     endereco de ip.
    """
    conexao, endereco = server.accept()  


    """
    Salvar cliente no minha lista de clientes ativos
    """
    lista_de_clientes.append(conexao)

    print("Cliente conectado endereço: " + endereco[0])

    start_new_thread( thread_do_cliente, (conexao, endereco)  )








