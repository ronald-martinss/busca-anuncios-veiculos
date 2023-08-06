from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime
import math
import time
import pandas as pd
import os
import openpyxl

# definindo um pequeno delay para aplicar ao longo do script
delay = time.sleep(1)

# definindo os estados de captura
estados = ['am-manaus', 'go-goiania', 'pe-recife', 'pr-curitiba', 'ce-fortaleza',
           'mg-belo-horizonte', 'ba-salvador', 'df-brasilia', 'rj-rio-de-janeiro', 'sp-sao-paulo']

# lista onde serão armazenados os dados referente a cada anuncio
anuncios = []

# captura de anuncios propriamente dita para cada estado
for estado in estados:

    url = f'https://www.site.com.br/{estado}?page=0'

    # "criando" o navegador
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    # identificando quantos anuncios estão disponiveis
    quantidade = driver.find_element(
        By.XPATH, '//*[@id="__next"]/main/div/div/div/div[2]/div[2]/div/div[3]/h2').text
    i = quantidade.find(' ')
    quantidade = quantidade[0:i]
    quantidade = int(quantidade.replace('.', ''))

    # calculando a quantidade de paginas a serem passadas
    qtd_paginas = quantidade/24
    qtd_paginas = math.ceil(qtd_paginas)
    qtd_paginas = int(qtd_paginas)

    for i in range(qtd_paginas - 1):
        try:
            cards = WebDriverWait(driver, 60).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'deal-card')))
            delay
        except:
            break
        for card in cards:
            datetime_captura = datetime.now().strftime('%d/%m/%Y %H:%M')
            marca = card.find_element(By.TAG_NAME, 'h2').text
            modelo = card.find_element(By.TAG_NAME, 'h3').text
            fab_mod = card.find_elements(
                By.CLASS_NAME, 'mui-style-1i3bo6b')[0].text
            km = card.find_elements(By.CLASS_NAME, 'mui-style-1i3bo6b')[1].text
            try:
                estado_uf = card.find_elements(
                    By.CLASS_NAME, 'mui-style-1i3bo6b')[2].text
            except:
                pass
            valor = card.find_element(By.CLASS_NAME, 'mui-style-1at8yrz').text
            link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            dados = {"data_captura": datetime_captura, "marca": marca, 'modelo': modelo,
                     "fab_mod": fab_mod, "km": km, "estado": estado_uf, "valor": valor, "link": link}
            anuncios.append(dados)
        if i % 15 == 0 and i != 0:
            time.sleep(30)
            driver.get(
                f'https://www.site.com.br/{estado}?page={i+1}')
        else:
            driver.get(
                f'https://www.site.com.br/{estado}?page={i+1}')

    driver.quit()
    delay

# armazenando os dados coletados em um arquivo excel
dia_captura = date.today().strftime('%d-%m-%Y')
path = os.getcwd()
df = pd.DataFrame(anuncios)
df.to_excel(path + r'/dataset/Captura {}.xlsx'.format(dia_captura), index=False)
