def calcula_fretes(fretes, tipo_caminhao, comprimento_caminhao, largura_caminhao=2.2, altura_caminhao=2.2):
    """
    Função que calcula se o caminhoneiro pode realizar os fretes disponíveis com base no volume das telhas e no
    volume suportado pelo caminhão.

    Parâmetros:
    - fretes: Lista de dicionários contendo as informações dos fretes. Cada dicionário deve ter:
        - 'tipo_telha' (str): Tipo da telha ('filme' ou 'sanduíche')
        - 'quantidade_telhas' (int): Quantidade de telhas
        - 'comprimento_telha' (float): Comprimento das telhas
    - tipo_caminhao: Tipo do caminhão ('aberto' ou 'baú')
    - comprimento_caminhao: Comprimento disponível do caminhão (em metros)
    - largura_caminhao (float): Largura do caminhão, fixada em 2,2 metros
    - altura_caminhao (float): Altura do caminhão, fixada em 2,2 metros

    Retorno:
    - Uma lista de fretes que o caminhoneiro pode ou não fazer com base no volume das telhas e do caminhão.
    """
    fretes_possiveis = []

    # Definindo as dimensões do caminhão
    volume_caminhao = comprimento_caminhao * largura_caminhao * altura_caminhao

    for frete in fretes:
        tipo_telha = frete['tipo_telha']
        quantidade_telhas = frete['quantidade_telhas']
        comprimento_telha = frete['comprimento_telha']

        # Calculando o volume das telhas
        if tipo_telha == 'filme':
            altura_telha = 1.3  # Altura das telhas do tipo filme
            largura_telha = 1.1  # Largura das telhas é fixa
        elif tipo_telha == 'sanduíche':
            altura_telha = 1.2  # Altura das telhas do tipo sanduíche
            largura_telha = 1.1  # Largura das telhas é fixa
        else:
            continue  # Caso o tipo de telha seja inválido, ignoramos este frete

        volume_telhas = quantidade_telhas * largura_telha * altura_telha * comprimento_telha

        # Verificando se o caminhão pode transportar as telhas
        if volume_telhas <= volume_caminhao:
            fretes_possiveis.append(frete)
    
    return fretes_possiveis


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de lista de fretes
    fretes = [
        {"tipo_telha": "filme", "quantidade_telhas": 23, "comprimento_telha": 6.0},
        {"tipo_telha": "sanduíche", "quantidade_telhas": 27, "comprimento_telha": 5.0},
        {"tipo_telha": "filme", "quantidade_telhas": 15, "comprimento_telha": 7.0}
    ]

    tipo_caminhao = "aberto"
    comprimento_caminhao = 10.0  # Comprimento do caminhão em metros

    fretes_possiveis = calcula_fretes(fretes, tipo_caminhao, comprimento_caminhao)
    
    print("Fretes que o caminhoneiro pode realizar:")
    for frete in fretes_possiveis:
        print(f"Tipo de telha: {frete['tipo_telha']}, Quantidade: {frete['quantidade_telhas']}, Comprimento das telhas: {frete['comprimento_telha']} metros")
