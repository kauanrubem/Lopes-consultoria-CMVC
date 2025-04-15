import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Carregar a planilha
from utils import carregar_dados_drive
df_projecao_2 = carregar_dados_drive()

# --- DADOS DO GRÁFICO DE PIZZA E TOTALIZADORES ---
# Acessando o valor da estimativa total e apuração
valor_estimativa_total = pd.to_numeric(df_projecao_2.iloc[214, 7], errors='coerce')  # linha 216
valor_apuracao = pd.to_numeric(df_projecao_2.iloc[215, 7], errors='coerce')  # Linha 216 (índice 215), para "Apuração CF art. 29-A"

valor_apuracao_percent = round(valor_apuracao * 100, 2)
complemento = round(100 - valor_apuracao_percent, 2)

fig_pizza = go.Figure()
fig_pizza.add_trace(go.Pie(
    labels=['Apuração CF art. 29-A', 'Não Apurado'],
    values=[valor_apuracao_percent, complemento],
    hole=0.3
))
fig_pizza.update_layout(
    title_text='Estimativa Não Considerando INSS Patronal dos Agentes Políticos',
    margin=dict(t=40, b=0, l=0, r=0),
    height=350
)

# --- DADOS MENSAIS DAS TABELAS ---
df_tabelas = df_projecao_2.iloc[195:211].reset_index(drop=True)
df_tabelas.columns = ['Comp_Agentes', 'Agentes_Politicos', 'C2',
                      'Servidores', 'C4', 'C5',
                      'Comp_Estimativa', 'Estimativa_Total', 'C8',
                      'Comp_Apuracao', 'Apuracao_29A', 'C11']

df_dados = df_tabelas[df_tabelas['Comp_Agentes'].astype(str).str.contains("2025")].copy()

df_dados['Agentes_Politicos'] = pd.to_numeric(df_dados['Agentes_Politicos'], errors='coerce')
df_dados['Servidores'] = pd.to_numeric(df_dados['Servidores'], errors='coerce')
df_dados['Estimativa_Total'] = pd.to_numeric(df_dados['Estimativa_Total'], errors='coerce')
df_dados['Apuracao_29A'] = pd.to_numeric(df_dados['Apuracao_29A'], errors='coerce')
df_dados['Comp'] = pd.to_datetime(df_dados['Comp_Agentes']).dt.strftime('%b/%Y')

# --- TOTAIS (linha 211) ---
linha_total = df_projecao_2.iloc[209]
total_agentes = pd.to_numeric(linha_total[1], errors='coerce')
total_servidores = pd.to_numeric(linha_total[3], errors='coerce')
total_estimativa = pd.to_numeric(linha_total[7], errors='coerce')
total_apuracao = pd.to_numeric(linha_total[10], errors='coerce')

# --- GRÁFICO DE BARRAS 1: AGENTES x SERVIDORES (EIXO INVERTIDO) ---
fig_inss = go.Figure()
fig_inss.add_trace(go.Bar(
    y=df_dados['Comp'],
    x=df_dados['Agentes_Politicos'],
    name='Agentes Políticos',
    marker_color='indianred',
    orientation='h'
))
fig_inss.add_trace(go.Bar(
    y=df_dados['Comp'],
    x=df_dados['Servidores'],
    name='Servidores',
    marker_color='seagreen',
    orientation='h'
))
fig_inss.update_layout(
    title='INSS Patronal: Agentes Políticos vs Servidores',
    barmode='group',
    height=600
)

# --- GRÁFICO DE BARRAS 2: ESTIMATIVA x APURAÇÃO (EIXO INVERTIDO) ---
fig_apuracao = go.Figure()
fig_apuracao.add_trace(go.Bar(
    y=df_dados['Comp'],
    x=df_dados['Estimativa_Total'],
    name='Estimativa Total da Folha',
    marker_color='orange',
    orientation='h'
))
fig_apuracao.add_trace(go.Bar(
    y=df_dados['Comp'],
    x=df_dados['Apuracao_29A'],
    name='Apuração CF art. 29-A',
    marker_color='blue',
    orientation='h'
))
fig_apuracao.update_layout(
    title='Estimativa vs Apuração CF art. 29-A',
    barmode='group',
    height=600
)

# --- LAYOUT FINAL ---
apuracao_layout = dbc.Row([
    # Gráfico de Pizza + Totalizadores
    dbc.Col(dbc.Card(dbc.CardBody([
        dcc.Graph(figure=fig_pizza, id='grafico-pizza'),
        html.H6(
            f"Estimativa da Folha: R$ {valor_estimativa_total:,.2f} | "
            f"Apuração: {valor_apuracao_percent:.2f}%",
            style={"textAlign": "left", "marginTop": "15px"}
        )
    ])), width=12),

    # Gráfico INSS Patronal + Total
    dbc.Col(dbc.Card(dbc.CardBody([
        dcc.Graph(figure=fig_inss, id='grafico-inss'),
        html.H6(
            f"Total - Agentes Políticos: R$ {total_agentes:,.2f} | "
            f"Servidores: R$ {total_servidores:,.2f}",
            style={"textAlign": "center", "marginTop": "15px"}
        )
    ])), width=6),

    # Gráfico Estimativa x Apuração + Total
    dbc.Col(dbc.Card(dbc.CardBody([
        dcc.Graph(figure=fig_apuracao, id='grafico-apuracao'),
        html.H6(
            f"Total - Estimativa: R$ {total_estimativa:,.2f} | "
            f"Apuração: R$ {total_apuracao:,.2f}",
            style={"textAlign": "center", "marginTop": "15px"}
        )
    ])), width=6),
])
