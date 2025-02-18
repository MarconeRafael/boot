import openai
import sys
import pandas as pd
from keys import chave_openai  # Supondo que a chave da API está em um arquivo separado
from calcula import calcula_fretes  # Importando a função calcula_fretes

openai.api_key = chave_openai  # Definindo a chave da API para o OpenAI

# Lê a lista de fretes do arquivo Excel
try:
    # Usando openpyxl para ler arquivos .xlsx
    fretes_df = pd.read_excel("data/xls/fretes.xlsx", engine="openpyxl")
    
    # Garantir que a coluna 'Preço' seja numérica
    fretes_df["Preço"] = pd.to_numeric(fretes_df["Preço"], errors="coerce")  # Converte para numérico, substituindo erros por NaN
    
    # Remover valores NaN da coluna de preço
    fretes_df = fretes_df.dropna(subset=["Preço"])
    
    # Criando o dicionário de destinos e preços
    fretes_dict = dict(zip(fretes_df["Destino"].dropna(), fretes_df["Preço"].dropna()))
    
    # Gerar a lista de fretes
    lista_fretes_str = ", ".join(f"{destino} (R${preco:.2f})" for destino, preco in fretes_dict.items())
except Exception as e:
    fretes_dict = {}  # Se houver erro, não há destinos disponíveis
    lista_fretes_str = "Nenhuma viagem disponível no momento."
    print(f"Erro ao ler a lista de fretes: {e}")

def chat_with_trucker(prompt, conversation_history=[]):
    system_message = (
        "Você é um caminhoneiro experiente que adora imitar pessoas e tem um jeito bem típico de falar. "
        "Responda de forma descontraída, curta e divertida, como um caminhoneiro conversando e negociando. "
        "Se perguntarem sobre fretes, use os seguintes valores: {lista}. "
        "Caso perguntem sobre um destino que não está na lista, avise que só temos essas opções disponíveis. "
        "Mantenha o contexto da conversa para que as respostas façam sentido dentro do diálogo em andamento. "
        "Se o usuário confirmar um negócio, reconheça e finalize a negociação com uma resposta apropriada."
    ).format(lista=lista_fretes_str)
    
    conversation_history.append({"role": "user", "content": prompt})

    # Perguntar os detalhes do caminhão (tipo, comprimento, etc.)
    if 'informações do caminhão' in prompt.lower():
        reply = "Claro, parceiro! Me fala aí o tipo do seu caminhão (aberto ou baú) e o comprimento dele. A largura é sempre 2,2 metros e a altura você também pode me dizer se tiver uma diferente de 2,2 metros."
        conversation_history.append({"role": "assistant", "content": reply})
        return reply

    # Processar as informações do caminhão
    if 'tipo_caminhao' in prompt.lower() and 'comprimento' in prompt.lower():
        # Extrair dados do prompt (simplificando o processo aqui, mas pode ser feito com regex ou outro método)
        tipo_caminhao = "aberto"  # Exemplo, isso precisa ser extraído da conversa do usuário
        comprimento_caminhao = 10.0  # Exemplo, esse valor precisa ser extraído
        altura_caminhao = 2.2  # Valor fixo
        largura_caminhao = 2.2  # Valor fixo

        # Chama a função calcula_fretes
        fretes_possiveis = calcula_fretes(fretes_df.to_dict(orient='records'), tipo_caminhao, comprimento_caminhao, largura_caminhao, altura_caminhao)

        if fretes_possiveis:
            fretes_resposta = "\n".join([f"Tipo de telha: {frete['tipo_telha']}, Quantidade: {frete['quantidade_telhas']}, Comprimento das telhas: {frete['comprimento_telha']} metros" for frete in fretes_possiveis])
            reply = f"Esses são os fretes que seu caminhão pode realizar:\n{fretes_resposta}"
        else:
            reply = "Infelizmente, o seu caminhão não comporta os fretes disponíveis no momento."
        conversation_history.append({"role": "assistant", "content": reply})
        return reply

    # Se confirmar um negócio
    if any(term in prompt.lower() for term in ["fechado", "concordo", "topo", "negócio fechado"]):
        reply = "Maravilha, compadre! Negócio fechado! Vou ajeitar o caminhão e partir pra estrada. Valeu pela confiança!"
    else:
        # Envia o prompt para a API do OpenAI para gerar a resposta
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_message}] + conversation_history
        )
        reply = response.choices[0].message['content']  # Pegando a resposta gerada pela API
    
    conversation_history.append({"role": "assistant", "content": reply})  # Adiciona a resposta à conversa
    return reply

if __name__ == "__main__":
    # Quando o script for chamado diretamente, o prompt é passado como argumento na linha de comando
    prompt = sys.argv[1]
    print(chat_with_trucker(prompt))
