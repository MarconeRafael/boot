import openai
import sys
import pandas as pd
from keys import chave_openai  # Supondo que a chave da API está em um arquivo separado

openai.api_key = chave_openai  # Definindo a chave da API para o OpenAI

# Lê a lista de fretes do arquivo Excel
try:
    fretes_df = pd.read_excel("data/fretes.xls")
    # Supondo que a coluna com os destinos se chame "Viagem"
    lista_fretes = fretes_df["Viagem"].dropna().tolist()
    lista_fretes_str = ", ".join(lista_fretes)
except Exception as e:
    lista_fretes_str = "Ceará, Rio de Janeiro"  # Valores padrão, se houver erro na leitura
    print(f"Erro ao ler a lista de fretes: {e}")

def chat_with_trucker(prompt, conversation_history=[]):
    system_message = (
        "Você é um caminhoneiro experiente que adora imitar pessoas e tem um jeito bem típico de falar. "
        "Responda de forma descontraída, curta e divertida, como um caminhoneiro conversando e negociando. "
        "Se perguntarem sobre uma viagem até o Ceará, diga que o máximo que podemos pagar é R$1400. "
        "Se perguntarem sobre uma viagem até o Rio de Janeiro, diga que o máximo que podemos pagar é R$5000. "
        "Se perguntar sobre uma viagem não listada, fale que temos apenas essas opções: {lista}. "
        "Mantenha o contexto da conversa para que as respostas façam sentido dentro do diálogo em andamento. "
        "Se o usuário confirmar um negócio, reconheça e finalize a negociação com uma resposta apropriada."
    ).format(lista=lista_fretes_str)
    
    conversation_history.append({"role": "user", "content": prompt})
    
    # Checa se o usuário está confirmando um negócio
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
