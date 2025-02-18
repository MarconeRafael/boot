import os
import pandas as pd
import openpyxl

# Caminho do arquivo de entrada (Excel) e do arquivo de saída (CSV)
xlsx_dir = 'data/xls'
xlsx_file_path = os.path.join(xlsx_dir, 'fretes.xlsx')
csv_dir = 'data/csv'
csv_file_path = os.path.join(csv_dir, 'fretes.csv')

# Verifica se o diretório "csv" existe, caso contrário, cria-o
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

try:
    # Verifica se o arquivo .xlsx existe
    if not os.path.exists(xlsx_file_path):
        raise FileNotFoundError(f"Arquivo .xlsx não encontrado: {xlsx_file_path}")
    
    # Verifica se o arquivo Excel é válido
    try:
        wb = openpyxl.load_workbook(xlsx_file_path)
        print(f"Arquivo Excel carregado com sucesso: {xlsx_file_path}")
    except Exception as e:
        raise ValueError(f"Erro ao abrir o arquivo Excel: {e}")

    # Remove as 9 primeiras linhas de cada planilha
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        ws.delete_rows(1, 9)  # Exclui as 9 primeiras linhas

    # Salva o arquivo Excel limpo
    cleaned_xlsx_file_path = os.path.join(xlsx_dir, 'fretes_limpo.xlsx')
    wb.save(cleaned_xlsx_file_path)
    print(f"Arquivo Excel limpo e salvo como: {cleaned_xlsx_file_path}")

    # Tente carregar o arquivo .xlsx limpo
    try:
        df = pd.read_excel(cleaned_xlsx_file_path, header=9)  # O cabeçalho agora está na linha 10 (índice 9)
        print(f"Arquivo Excel lido com sucesso: {cleaned_xlsx_file_path}")
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo Excel com pandas: {e}")

    # Converte para CSV
    df.to_csv(csv_file_path, index=False)
    print(f"Arquivo CSV criado com sucesso: {csv_file_path}")

except Exception as e:
    print(f"Erro ao processar o arquivo Excel ou criar o CSV: {e}")
