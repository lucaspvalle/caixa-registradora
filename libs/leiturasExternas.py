import socket

# Este arquivo contém as leituras externas que podem ser utilizadas para a venda de produtos, considerando:
#   1. leitura de código de barras para contas externas a pagar,
#   2. leitura de peso de produtos vendidos internamente.


def ler_codigo_de_barras(output_codigo):
    """
    Função para ler códigos de barras, conforme o padrão da Febraban.

    :param output_codigo: código de barras da conta a pagar
    :return: a categoria da conta paga e o valor
    """

    contas = {"1": "Prefeitura",
              "2": "Saneamento",
              "3": "Energia Elétrica e Gás",
              "4": "Telecomunicações",
              "5": "Órgãos Governamentais",
              "6": "Carnes e Assemelhados ou demais",
              "7": "Multas de trânsito",
              "9": "Uso exclusivo do banco"}

    if output_codigo[1] in contas:
        produto_comprado = f"Código de barras: {contas[output_codigo[1]]}"
        valor_produto = float(output_codigo[5:11] + output_codigo[12:16]) / 100

        print(produto_comprado)
        print(f"Valor a pagar: R$ {valor_produto}")
    else:
        produto_comprado = ""
        valor_produto = 0

        print("Código não reconhecido.")

    return produto_comprado, valor_produto


def ler_peso_da_balanca():
    """
    Função para se conectar com o servidor de balança, replicado neste projeto.

    :return: valor pesado para o produto
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 8888))
        print("Conexão estabelecida com a balança.")

        reply = s.recv(4096)
        peso = round(float(reply.decode()), 3)

        print(f"Peso: {peso} kg")
        return peso
