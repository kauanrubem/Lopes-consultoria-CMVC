import pandas as pd
import requests
from io import BytesIO

def carregar_dados_drive(sheet_name='Projeção (2)'):
    file_id = "1ZWRPA-HB8ynhCBtKU6YvG1y5TuagMvr3"  # ID correto da sua planilha
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_excel(BytesIO(response.content), sheet_name=sheet_name, engine='openpyxl')
    else:
        raise Exception(f"Erro ao baixar planilha do Google Drive: {response.status_code}")
