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

# o restante do código está privado :(
