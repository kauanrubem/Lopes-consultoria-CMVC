import pandas as pd
import requests
from io import BytesIO

def carregar_dados_drive(sheet_name='PROJECAO CMVC'):
    file_id = "1BlsI5-SKdl2O-N_LED64EuwIRDTiJuEA"
    url = f"https://drive.google.com/uc?export=download&id=1BlsI5-SKdl2O-N_LED64EuwIRDTiJuEA"  # <-- Aqui está o correto!
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_excel(BytesIO(response.content), sheet_name=sheet_name, engine='openpyxl')
    else:
        raise Exception(f"Erro ao baixar planilha do Google Drive: {response.status_code}")
