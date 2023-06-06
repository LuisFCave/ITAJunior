import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get("https://finance.yahoo.com/most-active?count=25&offset=0")
soup = BeautifulSoup(response.content, 'html.parser')
linhas1 = soup.find_all('tr', class_='simpTblRow')

response = requests.get("https://finance.yahoo.com/most-active?count=25&offset=25")
soup = BeautifulSoup(response.content, 'html.parser')
linhas2 = soup.find_all('tr', class_='simpTblRow')

response = requests.get("https://finance.yahoo.com/most-active?count=25&offset=50")
soup = BeautifulSoup(response.content, 'html.parser')
linhas3 = soup.find_all('tr', class_='simpTblRow')

response = requests.get("https://finance.yahoo.com/most-active?count=25&offset=75")
soup = BeautifulSoup(response.content, 'html.parser')
linhas4 = soup.find_all('tr', class_='simpTblRow')

linhas = linhas1 + linhas2 + linhas3 + linhas4

dados = []
for linha in linhas:
    nome_element = linha.find('td', attrs={'aria-label': 'Name'})
    sigla_element = linha.find('td', attrs={'aria-label': 'Symbol'})
    variacao_porcentagem_element = linha.find('td', attrs={'aria-label': '% Change'})
    variacao_nominal_element = linha.find('td', attrs={'aria-label': 'Change'})
    volume_element = linha.find('td', attrs={'aria-label': 'Volume'})
    valor_mercado_element = linha.find('td', attrs={'aria-label': 'Market Cap'})

    nome = nome_element.get_text()
    sigla = sigla_element.get_text()
    variacao_nominal = variacao_nominal_element.get_text()
    variacao_porcentagem = variacao_porcentagem_element.get_text()
    volume = volume_element.get_text()
    valor_mercado = valor_mercado_element.get_text()

    dados.append([nome, sigla, variacao_nominal, variacao_porcentagem, volume, valor_mercado])

df = pd.concat([pd.DataFrame([dados[i]], columns=["Nome", "Sigla", "Variação Nominal", "Variação Porcentagem", "Volume", "Valor Mercado"]) for i in range(len(dados))], ignore_index=True)
df.to_excel("dados.xlsx")
print(df)



