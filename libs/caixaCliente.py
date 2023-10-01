import sqlite3
from libs.gerenciadorDeRelatorios import GerenciadorDeRelatorios
from libs.leiturasExternas import ler_codigo_de_barras, ler_peso_da_balanca


class CaixaServices:
    def __init__(self):
        print("Iniciando caixa!")
        self.cnx = sqlite3.connect('caixa.db')
        self.cnx.row_factory = sqlite3.Row

        self.relatorios = GerenciadorDeRelatorios(self.cnx)

    def __del__(self):
        print("Encerrando caixa!")
        self.cnx.close()

    @staticmethod
    def valida_tipo_de_input(quem="", tipo="inteiro"):
        validos = {"inteiro": int, "decimal": float}

        if not quem:
            quem = "\nDeseja continuar a operação? (sim: 1, não: 0)"

        while True:
            operacao = input(f"{quem}: ")
            try:
                return validos[tipo](operacao)
            except ValueError:
                print(f"Comando deve ser um número {tipo}. Tente novamente.")

    def inserir_entrada_de_estoque(self):
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

            comando = self.valida_tipo_de_input()
            if not comando:
                break

    def atualizar_preco_de_venda_de_produto(self):
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

            comando = self.valida_tipo_de_input()
            if not comando:
                break

    def _adicionar_produto_no_carrinho(self, output_codigo):
        produto_comprado = ""
        valor_produto = 0

        conteudo = self.cnx.execute("SELECT * FROM estoque WHERE codigo = ?", (output_codigo,)).fetchone()

        if conteudo is not None:
            peso = float(ler_peso_da_balanca())

            if conteudo["qtdade"] >= peso:
                valor_produto = conteudo["valor"] * peso
                produto_comprado = conteudo["produto"]
                print(f"O valor do(a) {produto_comprado} é R$ {valor_produto:.2f}")

                novo_estoque = float(conteudo["qtdade"]) - peso
                self.cnx.execute("UPDATE estoque SET qtdade = ? WHERE codigo = ?", (novo_estoque, output_codigo))
                self.cnx.commit()
            else:
                print("Produto insuficiente!")
        else:
            print("Código não reconhecido.")

        return produto_comprado, valor_produto

    def vender_produtos(self):
        carrinho = {}
        operacoes = {"7": self._adicionar_produto_no_carrinho, "8": ler_codigo_de_barras}

        print("\nAdicione os produtos a serem vendidos:")
        while True:
            output_codigo = input("Código do material: ")
            produto_comprado, valor_produto = operacoes.get(output_codigo[0], lambda: ("", 0))(output_codigo)

            if valor_produto > 0:
                if produto_comprado not in carrinho.keys():
                    carrinho[produto_comprado] = valor_produto
                else:
                    carrinho[produto_comprado] += valor_produto

            comando = self.valida_tipo_de_input()
            if not comando:
                break

        self.relatorios.gerar_relatorio_de_compras(carrinho)

    def gerar_relatorio_completo_de_estoque(self):
        self.relatorios.gerar_relatorio_de_estoque()

    def gerar_relatorio_de_baixo_estoque(self):
        self.relatorios.gerar_relatorio_de_estoque(5)
