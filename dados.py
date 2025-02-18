from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from keys import email_, senha_

# Configuração do Selenium para usar o ChromeDriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": os.path.abspath("./data")}
options.add_experimental_option("prefs", prefs)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Para depuração, remova o headless se estiver ativado
# options.add_argument("--headless")

# Inicializa o navegador
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URLs
url_login = (
    "https://sso-external.fretebras.com.br/realms/companies/protocol/openid-connect/auth?"
    "state=ea61138d7983caf7813ce0462afbde55&scope=profile%20email%20openid&response_type=code&"
    "approval_prompt=auto&redirect_uri=https%3A%2F%2Ffretebras.com.br%2Fsso%2Fsrc%2Findex.php&"
    "client_id=central-assinante#/"
)
url_fretes = "https://novacentral.fretebras.com.br/meus-fretes"

try:
    print("Abrindo a página de login...")
    driver.get(url_login)
    time.sleep(2)

    print("Aguardando o campo de e-mail (input real) ficar visível...")
    username_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    time.sleep(1)
    print("Campo de e-mail visível. Enviando e-mail...")
    username_input.clear()
    time.sleep(1)
    username_input.send_keys(email_)
    print("E-mail inserido.")
    time.sleep(1)

    print("Aguardando o campo de senha (input real) ficar visível...")
    password_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    time.sleep(1)
    print("Campo de senha visível. Enviando senha...")
    password_input.clear()
    time.sleep(1)
    password_input.send_keys(senha_ + Keys.RETURN)
    print("Senha inserida e login enviado.")
    time.sleep(3)

    print("Aguardando redirecionamento após login...")
    WebDriverWait(driver, 15).until(
        EC.url_contains("fretebras.com.br")
    )
    print("Redirecionamento detectado.")
    time.sleep(2)

    print("Acessando a página de fretes...")
    driver.get(url_fretes)
    time.sleep(2)

    print("Aguardando o botão 'Download da listagem' ficar presente...")
    # Seleciona o elemento pelo seletor do componente customizado
    download_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fuel-button[variant='secondary']"))
    )
    time.sleep(1)
    print("Botão 'Download da listagem' encontrado. Tentando clicar via JavaScript...")
    driver.execute_script("arguments[0].click();", download_button)
    print("Clique efetuado.")
    
    time.sleep(10)  # Tempo para o download
    print("Download concluído: fretes.xls salvo em ./data")

except Exception as e:
    print(f"Erro ao baixar o arquivo: {e}")

finally:
    driver.quit()
    print("Navegador fechado.")
