from libs.caixaCliente import CaixaServices


def main():
    services = CaixaServices()
    print("Bem vindo ao sistema!\n")

    comandos = {1: ["Entrada", services.inserir_entrada_de_estoque],
                2: ["Atualização de Produto", services.atualizar_preco_de_venda_de_produto],
                3: ["Vendas", services.vender_produtos],
                4: ["Relatório Gerencial", services.gerar_relatorio_completo_de_estoque],
                5: ["Relatório de Baixo Estoque", services.gerar_relatorio_de_baixo_estoque],
                6: ["Sair", exit]}

    erro = ["", lambda: print("Comando desconhecido. Tente novamente.")]

    print("Operações disponíveis:")
    for chave, (descricao, _) in comandos.items():
        print(f"{chave}) {descricao}")

    while True:
        operacao_id = services.valida_tipo_de_input("\nDigite o ID da operação desejada")
        _, realizar_acao = comandos.get(operacao_id, erro)
        realizar_acao()


if __name__ == "__main__":
    main()
