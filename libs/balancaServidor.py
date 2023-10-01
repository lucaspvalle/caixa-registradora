import socket
from random import uniform


class Balanca:
    """
    Esta classe replica o funcionamento de uma balança externa, que esteja acoplada
    ao sistema da caixa registradora.

    Por conta disso, ela funciona como um servidor (fonte externa) para o nosso cliente
    (isto é, a caixa em si).
    """
    HOST = "localhost"
    PORT = 8888

    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen(10)
            self.aguardar_pesagem(s)

    @staticmethod
    def aguardar_pesagem(s):
        """
        Espera indefinidamente até que o cliente acione a balança para pesagem de algum produto.

        :param s: 'socket' instanciado da balança
        :return: peso do produto
        """
        while True:
            print("Aguardando pesagem...")

            conn, addr = s.accept()
            with conn:
                print("Conectado a " + addr[0] + ':' + str(addr[1]))
                print("Iniciando pesagem!")

                peso = uniform(0.1, 1)
                conn.sendall(f"{peso}".encode())

                print("Peso enviado!")


if __name__ == "__main__":
    Balanca()
