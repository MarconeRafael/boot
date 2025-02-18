import openai
import sys
import pandas as pd
from keys import chave_openai  # Supondo que a chave da API está em um arquivo separado

openai.api_key = chave_openai  # Definindo a chave da API para o OpenAI

# Lê a lista de fretes do arquivo XLSX
try:
    fretes_df = pd.read_excel("data/xls/fretes.xlsx", engine="openpyxl")  # Lendo o arquivo

    # Remove espaços extras no nome das colunas
    fretes_df.columns = fretes_df.columns.str.strip()

    # Seleciona apenas as colunas relevantes
    fretes_df = fretes_df[["Origem", "Destino", "Carga", "Preço"]]

    # Substitui vírgula decimal por ponto e remove pontos separadores de milhar
    fretes_df["Preço"] = fretes_df["Preço"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)

    # Converte "Preço" para número (agora que está corrigido)
    fretes_df["Preço"] = pd.to_numeric(fretes_df["Preço"], errors="coerce")

    # Remove linhas com preço inválido
    fretes_df = fretes_df.dropna(subset=["Preço"])

    # Cria o dicionário de fretes
    fretes_dict = {
        (row["Origem"], row["Destino"], row["Carga"]): row["Preço"]
        for _, row in fretes_df.iterrows()
    }

    lista_fretes_str = ", ".join(
        f"De {origem} para {destino}, transportando {carga} por R${preco:.2f}"
        for (origem, destino, carga), preco in fretes_dict.items()
    )

except Exception as e:
    fretes_dict = {}  # Se houver erro, não há destinos disponíveis
    lista_fretes_str = "Nenhuma viagem disponível no momento."
    print(f"Erro ao ler a lista de fretes: {e}")

def chat_with_trucker(prompt, conversation_history=[]):
    system_message = (
        "Fale informalmente com bom humor. "
        "Responda de forma descontraída, curta como um caminhoneiro conversando e negociando. "
        "Se perguntarem sobre fretes, use os seguintes valores: {lista}. "
        "Caso perguntem sobre um destino que não está na lista, avise que só temos essas opções disponíveis. "
        "Mantenha o contexto da conversa para que as respostas façam sentido dentro do diálogo em andamento. "
        "Se o usuário confirmar um negócio, reconheça e finalize a negociação com uma resposta apropriada."
    ).format(lista=lista_fretes_str)
    
    conversation_history.append({"role": "user", "content": prompt})

    # Verifica se o usuário está perguntando sobre um frete e retorna o valor correspondente
    for (origem, destino, carga), preco in fretes_dict.items():
        if destino.lower() in prompt.lower() or origem.lower() in prompt.lower():
            reply = (
                f"Olha, parceiro, tem um frete de {origem} pra {destino}, "
                f"levando {carga}, pagando R${preco:.2f}. Se topar, é só falar!"
            )
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
