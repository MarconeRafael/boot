import openai
import sys
from keys import chave_openai  # Supondo que a chave da API está em um arquivo separado

openai.api_key = chave_openai  # Definindo a chave da API para o OpenAI

def chat_with_trucker(prompt, conversation_history=[]):
    system_message = (
        "Você é um caminhoneiro experiente que adora imitar pessoas e tem um jeito bem típico de falar. "
        "Responda de forma descontraída, curta e divertida, como um caminhoneiro conversando e negociando. "
        "Se perguntarem sobre uma viagem até o Ceará, diga que o máximo que podemos pagar é R$1400. "
        "Se perguntarem sobre uma viagem até o Rio de Janeiro, diga que o máximo que podemos pagar é R$5000. "
        "Se perguntar sobre uma viagem não listada, fale que temos apenas essas opções e liste as viagens mencionadas acima."
        "Mantenha o contexto da conversa para que as respostas façam sentido dentro do diálogo em andamento."
        "Se o usuário confirmar um negócio, reconheça e finalize a negociação com uma resposta apropriada."
    )
    
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
    # Quando o script for chamado diretamente
    prompt = sys.argv[1]  # Recebe o prompt que foi passado como argumento
    print(chat_with_trucker(prompt))  # Exibe a resposta do bot
