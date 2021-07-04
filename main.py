from users.cliente import Caixa


def main():
    db = Caixa()
    print("Bem vindo ao sistema!\n")

    comandos = {1: ["Entrada", db.entrada],
                2: ["Atualização de Produto", db.atualizar_produto],
                3: ["Vendas", db.vendas],
                4: ["Relatório Gerencial", db.relatorio_gerencial],
                5: ["Relatório de Baixo Estoque", db.relatorio_de_baixo_estoque],
                6: ["Sair", db.fechar]}

    print("Operações disponíveis:")
    for chave, (descricao, _) in comandos.items():
        print(f"{chave}) {descricao}")

    while True:
        operacao = db.valida_tipo_de_input("Digite o ID da operação desejada", "inteiro")
        comandos.get(operacao, ["Tratamento de erro", lambda: print("Comando desconhecido. Tente novamente.")])[1]()


if __name__ == "__main__":
    main()
