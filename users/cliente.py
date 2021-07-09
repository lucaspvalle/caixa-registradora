import sqlite3
import socket


class Caixa:
    def __init__(self):
        self.cnx = sqlite3.connect('caixa.db')
        self.cnx.row_factory = sqlite3.Row

    @staticmethod
    def valida_tipo_de_input(quem, tipo):
        validos = {"inteiro": int,
                   "decimal": float}

        while True:
            operacao = input(f"{quem}: ")
            try:
                return validos[tipo](operacao)
            except ValueError:
                print(f"Comando deve ser um número {tipo}. Tente novamente.")
                continue

    def entrada(self):
        print("\nInserindo novos materiais:")

        while True:
            input_codigo = self.valida_tipo_de_input("Código do material", "inteiro")
            input_qtdade = self.valida_tipo_de_input("Quantidade (kg)", "decimal")

            conteudo = self.cnx.execute("SELECT produto, qtdade FROM estoque where codigo = ?",
                                        (input_codigo,)).fetchone()

            if conteudo is not None:
                novo_estoque = conteudo["qtdade"] + input_qtdade
                self.cnx.execute("UPDATE estoque SET qtdade = ? WHERE codigo = ?", (novo_estoque, input_codigo))
                self.cnx.commit()
            else:
                input_material = input("Descrição do material: ")
                input_valor = self.valida_tipo_de_input("Valor de venda (R$)", "decimal")

                self.cnx.execute("INSERT INTO estoque VALUES (?, ?, ?, ?)",
                                 (input_codigo, input_material, input_qtdade, input_valor))
                self.cnx.commit()

            comando = self.valida_tipo_de_input("\nDeseja adicionar outro produto no sistema? "
                                                "1 caso sim, 0 caso contrário", "inteiro")
            if not comando:
                break

    def atualizar_produto(self):
        print("\nAtualizando produtos:")

        while True:
            produto_atualizado = self.valida_tipo_de_input("Código do material", "inteiro")
            conteudo = self.cnx.execute("SELECT produto FROM estoque WHERE codigo = ?",
                                        (produto_atualizado,)).fetchone()

            if conteudo is not None:
                atualizar_venda = self.valida_tipo_de_input("Novo valor de venda (R$)", "decimal")
                self.cnx.execute("UPDATE estoque SET valor = ? WHERE codigo = ?", (atualizar_venda, produto_atualizado))
                self.cnx.commit()
            else:
                print("Produto inexistente!")

            comando = self.valida_tipo_de_input("\nDeseja adicionar outro produto no sistema? "
                                                "1 caso sim, 0 caso contrário", "inteiro")
            if not comando:
                break

    @staticmethod
    def _ler_codigo_de_barras(output_codigo):
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

            print("Código não reconhecido")

        return produto_comprado, valor_produto

    def _adicionar_produto_no_carrinho(self, output_codigo):
        produto_comprado = ""
        valor_produto = 0

        conteudo = self.cnx.execute("SELECT * FROM estoque WHERE codigo = ?", (output_codigo,)).fetchone()

        if conteudo is not None:
            peso = float(self._balanca())

            if conteudo["qtdade"] >= peso:
                valor_produto = conteudo["valor"] * peso
                produto_comprado = conteudo["produto"]
                print(f"O valor do(a) {produto_comprado} é R$ {valor_produto:.2f}")

                novo_estoque = float(conteudo["qtdade"]) - peso
                self.cnx.execute("UPDATE estoque SET qtdade = ? WHERE codigo = ?", (novo_estoque, output_codigo))
                self.cnx.commit()
            else:
                print("Produto insuficiente")
        else:
            print("Código não reconhecido")

        return produto_comprado, valor_produto

    @staticmethod
    def _balanca():
        host = 'localhost'
        port = 8888
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        print("Conexão estabelecida com a balança")
        reply = s.recv(4096)
        peso = round(float(reply.decode()), 3)
        s.close()

        print(f"Peso: {peso} kg")
        return peso

    def vendas(self):
        lista_compras = []
        valor_carrinho = 0

        print("\nAdicione os produtos a serem vendidos:")
        while True:
            output_codigo = input("Código do material: ")

            if output_codigo[0] == "7":
                produto_comprado, valor_produto = self._adicionar_produto_no_carrinho(output_codigo)
            elif output_codigo[0] == "8":
                produto_comprado, valor_produto = self._ler_codigo_de_barras(output_codigo)
            else:
                valor_produto = 0
                produto_comprado = ""

            if valor_produto > 0:
                lista_compras.append(produto_comprado)
                valor_carrinho += valor_produto

            comando = self.valida_tipo_de_input("\nDeseja adicionar outro produto no sistema? "
                                                "1 caso sim, 0 caso contrário", "inteiro")
            if not comando:
                break

        if valor_carrinho > 0:
            print("\nLista de produtos comprados:")
            for produto in lista_compras:
                print(produto)

            print(f"O valor total da compra foi R$ {valor_carrinho:.2f}")

    @staticmethod
    def _imprime_relatorio(conteudo):
        if len(conteudo) > 0:
            print("\nCódigo\tProduto\tQtdade (kg)\tValor (R$)")

            for codigo, produto, qtdade, valor in conteudo:
                print(f"{codigo}\t{produto}\t{qtdade:.2f}\t{valor}")
        else:
            print("\nNão há produtos para este relatório!")

    def relatorio_gerencial(self):
        print("\nRelatório Gerencial:")

        conteudo = self.cnx.execute("SELECT * FROM estoque").fetchall()
        self._imprime_relatorio(conteudo)

    def relatorio_de_baixo_estoque(self):
        print("\nRelatório de Baixo Estoque:")

        while True:
            limite = self.valida_tipo_de_input("Defina, em kg, o limite de baixo estoque", "decimal")

            conteudo = self.cnx.execute("SELECT * FROM estoque WHERE qtdade <= ?", (limite,)).fetchall()
            self._imprime_relatorio(conteudo)

            comando = self.valida_tipo_de_input("\nDeseja analisar outro limite de estoque? "
                                                "1 caso sim, 0 caso contrário", "inteiro")
            if not comando:
                break

    def fechar(self):
        print("Conexão encerrada!")

        self.cnx.close()
        exit()
