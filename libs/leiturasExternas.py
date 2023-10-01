import socket

# Este arquivo cont�m as leituras externas que podem ser utilizadas para a venda de produtos, considerando:
#   1. leitura de c�digo de barras para contas externas a pagar,
#   2. leitura de peso de produtos vendidos internamente.


def ler_codigo_de_barras(output_codigo):
    """
    Fun��o para ler c�digos de barras, conforme o padr�o da Febraban.

    :param output_codigo: c�digo de barras da conta a pagar
    :return: a categoria da conta paga e o valor
    """

    contas = {"1": "Prefeitura",
              "2": "Saneamento",
              "3": "Energia El�trica e G�s",
              "4": "Telecomunica��es",
              "5": "�rg�os Governamentais",
              "6": "Carnes e Assemelhados ou demais",
              "7": "Multas de tr�nsito",
              "9": "Uso exclusivo do banco"}

    if output_codigo[1] in contas:
        produto_comprado = f"C�digo de barras: {contas[output_codigo[1]]}"
        valor_produto = float(output_codigo[5:11] + output_codigo[12:16]) / 100

        print(produto_comprado)
        print(f"Valor a pagar: R$ {valor_produto}")
    else:
        produto_comprado = ""
        valor_produto = 0

        print("C�digo n�o reconhecido.")

    return produto_comprado, valor_produto


def ler_peso_da_balanca():
    """
    Fun��o para se conectar com o servidor de balan�a, replicado neste projeto.

    :return: valor pesado para o produto
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 8888))
        print("Conex�o estabelecida com a balan�a.")

        reply = s.recv(4096)
        peso = round(float(reply.decode()), 3)

        print(f"Peso: {peso} kg")
        return peso
