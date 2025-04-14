import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Carregar os dados do arquivo "Projeção folha - CMVC.xlsx"
file_path = 'dataset/Projeção folha - CMVC.xlsx'
df_projecao_2 = pd.read_excel(file_path, sheet_name='Projeção (2)')

# Limpar e processar os dados
df_projecao_2_cleaned = df_projecao_2.iloc[2:].reset_index(drop=True)
df_projecao_2_cleaned.columns = [
    'Regime', 'Qtd', 'Salário Base Total (R$)', 'Outros Vencimentos (R$)', 'H. Extras', 
    'Diárias', '1/3 de Férias', 'Total de Vencimentos (R$)', 'INSS', 'IRRF', 'Outros Descontos', 'Total de Descontos'
]

# Limpar a coluna 'Regime' para verificar os períodos
df_projecao_2_cleaned['Regime'] = df_projecao_2_cleaned['Regime'].str.strip()

# Filtrando os dados do "Total"
df_total = df_projecao_2_cleaned[df_projecao_2_cleaned['Regime'] == 'Total']
# Excluir a linha 207 (Total geral)
df_total = df_total[df_total.index != 207]

# Verificar se há 13 entradas para "Total"
if len(df_total) == 0:
    print("Erro: Não há dados para 'Total'. Verifique se o regime 'Total' está correto na planilha.")
else:
    # Adicionando uma nova coluna 'Período' para associar os dados ao período correspondente
    df_total['Período'] = pd.NA

    # Iterar sobre as linhas para associar o período a cada valor
    current_period = None
    for index, row in df_total.iterrows():
        if pd.notna(row['Regime']) and '2025' in str(row['Regime']):  # Identificando um período válido
            current_period = row['Regime']
        if current_period:
            df_total.at[index, 'Período'] = current_period  # Atribuindo o período correspondente

    # Definir os meses (de Janeiro a Dezembro + 13º mês)
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 
             'Outubro', 'Novembro', 'Dezembro', '13º Mês']

    # Garantir que temos exatamente 13 entradas para o 'Total'
    if len(df_total) == 13:
        df_total['Mês'] = meses  # Atribuindo os meses à coluna 'Mês'
    else:
        # Caso o número de entradas não seja 13, distribuir os meses proporcionalmente
        df_total['Mês'] = meses[:len(df_total)]  # Atribuindo os meses com base na quantidade de dados

    # Verificando se a coluna 'Mês' foi corretamente adicionada
    print(f"\nDataFrame com 'Mês' adicionado para Total:")
    print(df_total.head())

    # Gráfico de Qtd e Total de Vencimentos (R$), agora com meses no eixo X (fig1_total)
    fig1_total = go.Figure()

    fig1_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['Total de Vencimentos (R$)'],  # Total de Vencimentos (R$) no eixo Y
        name='Total de Vencimentos',  # Nome para a legenda
        marker=dict(color='orange')  # Cor da barra de Total de Vencimentos
    ))

    # Gráfico de Qtd (novo gráfico) (fig0_total)
    fig0_total = go.Figure()

    fig0_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['Qtd'],  # Qtd no eixo Y
        name='Qtd',  # Nome para a legenda
        marker=dict(color='blue')  # Cor da barra de Qtd
    ))

    # Gráfico de Outros Vencimentos (R$), H. Extras, Diárias, 1/3 de Férias, Total de Vencimentos (R$) (fig2_total)
    fig2_total = go.Figure()

    fig2_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['Outros Vencimentos (R$)'],  # Outros Vencimentos (R$) no eixo Y
        name='Outros Vencimentos',  # Nome para a legenda
        marker=dict(color='green')  # Cor da barra de Outros Vencimentos
    ))

    fig2_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['H. Extras'],  # H. Extras no eixo Y
        name='H. Extras',  # Nome para a legenda
        marker=dict(color='red')  # Cor da barra de H. Extras
    ))

    fig2_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['Diárias'],  # Diárias no eixo Y
        name='Diárias',  # Nome para a legenda
        marker=dict(color='blue')  # Cor da barra de Diárias
    ))

    fig2_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['1/3 de Férias'],  # 1/3 de Férias no eixo Y
        name='1/3 de Férias',  # Nome para a legenda
        marker=dict(color='purple')  # Cor da barra de 1/3 de Férias
    ))

    # Gráfico de Total de Descontos (fig3_total)
    fig3_total = go.Figure()

    fig3_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['Total de Descontos'],  # Total de Descontos no eixo Y
        name='Total de Descontos',  # Nome para a legenda
        marker=dict(color='pink')  # Cor da barra de Total de Descontos
    ))

    # Gráfico de INSS, IRRF e Outros Descontos (fig4_total)
    fig4_total = go.Figure()

    fig4_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['INSS'],  # INSS no eixo Y
        name='INSS',  # Nome para a legenda
        marker=dict(color='cyan')  # Cor da barra de INSS
    ))

    fig4_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['IRRF'],  # IRRF no eixo Y
        name='IRRF',  # Nome para a legenda
        marker=dict(color='yellow')  # Cor da barra de IRRF
    ))

    fig4_total.add_trace(go.Bar(
        x=df_total['Mês'],  # Usando os meses no eixo X
        y=df_total['Outros Descontos'],  # Outros Descontos no eixo Y
        name='Outros Descontos',  # Nome para a legenda
        marker=dict(color='gray')  # Cor da barra de Outros Descontos
    ))

    # Atualizar o layout para incluir título e ajustar a legenda para o fig1_total
    fig1_total.update_layout(
        title='Comparação Total de Vencimentos (R$) por Mês',  # Título do gráfico
        xaxis_title='Meses',  # Título do eixo X
        yaxis_title='Valores (R$)',  # Título do eixo Y
        barmode='group',  # Agrupar as barras lado a lado
        legend_title='Categorias',  # Título da legenda
        showlegend=True  # Mostrar a legenda
    )

    # Atualizar o layout para incluir título e ajustar a legenda para o fig0_total
    fig0_total.update_layout(
        title='Quantidade por Mês',  # Título do gráfico
        xaxis_title='Meses',  # Título do eixo X
        yaxis_title='Qtd',  # Título do eixo Y
        barmode='group',  # Agrupar as barras lado a lado
        legend_title='Categorias',  # Título da legenda
        showlegend=True  # Mostrar a legenda
    )

    # Atualizar o layout para incluir título e ajustar a legenda para o fig2_total
    fig2_total.update_layout(
        title='Comparação de Vencimentos por Mês',  # Título do gráfico
        xaxis_title='Meses',  # Título do eixo X
        yaxis_title='Valores (R$)',  # Título do eixo Y
        barmode='group',  # Agrupar as barras lado a lado
        legend_title='Categorias',  # Título da legenda
        showlegend=True  # Mostrar a legenda
    )

    # Atualizar o layout para incluir título e ajustar a legenda para o fig3_total
    fig3_total.update_layout(
        title='Total de Descontos por Mês',  # Título do gráfico
        xaxis_title='Meses',  # Título do eixo X
        yaxis_title='Descontos (R$)',  # Título do eixo Y
        barmode='group',  # Agrupar as barras lado a lado
        legend_title='Categorias',  # Título da legenda
        showlegend=True  # Mostrar a legenda
    )

    # Atualizar o layout para incluir título e ajustar a legenda para o fig4_total
    fig4_total.update_layout(
        title='Descontos (INSS, IRRF, Outros) por Mês',  # Título do gráfico
        xaxis_title='Meses',  # Título do eixo X
        yaxis_title='Descontos (R$)',  # Título do eixo Y
        barmode='group',  # Agrupar as barras lado a lado
        legend_title='Categorias',  # Título da legenda
        showlegend=True  # Mostrar a legenda
    )

    # Layout de Total, com todos os gráficos
    total_layout = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([  
            dcc.Graph(id='fig1_total', figure=fig1_total, style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),

        dbc.Col(dbc.Card(dbc.CardBody([  
            dcc.Graph(id='fig0_total', figure=fig0_total, style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),

        dbc.Col(dbc.Card(dbc.CardBody([  
            dcc.Graph(id='fig2_total', figure=fig2_total, style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),

        dbc.Col(dbc.Card(dbc.CardBody([  
            dcc.Graph(id='fig3_total', figure=fig3_total, style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),

        dbc.Col(dbc.Card(dbc.CardBody([  
            dcc.Graph(id='fig4_total', figure=fig4_total, style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),
    ])
