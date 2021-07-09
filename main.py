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

    erro = ["", lambda: print("Comando desconhecido. Tente novamente.")]

    print("Operações disponíveis:")
    for chave, (descricao, _) in comandos.items():
        print(f"{chave}) {descricao}")

    while True:
        operacao = db.valida_tipo_de_input("\nDigite o ID da operação desejada", "inteiro")
        _, acao = comandos.get(operacao, erro)
        acao()


if __name__ == "__main__":
    main()
