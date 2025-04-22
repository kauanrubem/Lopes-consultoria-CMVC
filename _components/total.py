from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

def layout_total():
    return dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='fig1_total', style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='fig0_total', style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='fig2_total', style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='fig3_total', style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='fig4_total', style={'height': '400px', 'width': '100%', 'padding': '0'})
        ])), xs=12, md=12),
    ])

def registrar_callbacks_total(app):
    @app.callback(
        [Output('fig0_total', 'figure'),
         Output('fig1_total', 'figure'),
         Output('fig2_total', 'figure'),
         Output('fig3_total', 'figure'),
         Output('fig4_total', 'figure')],
        Input('data-store', 'data')
    )
    def atualizar_graficos_total(data):
        # Limpa e prepara os dados
        df = pd.DataFrame(data)
        df = df.iloc[2:208].reset_index(drop=True)  # Corte explícito até a linha 216
        df.columns = [
            'Regime', 'Qtd', 'Salário Base Total (R$)', 'Outros Vencimentos (R$)', 'H. Extras',
            'Diárias', '1/3 de Férias', 'Total de Vencimentos (R$)', 'INSS', 'IRRF',
            'Outros Descontos', 'Total de Descontos'
        ]
        df['Regime'] = df['Regime'].str.strip()

        # Filtra o regime Total
        df = df[df['Regime'] == 'Total'].copy()

        # Atribui os meses conforme o número de linhas válidas
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
                 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro', '13º Mês']
        df['Mês'] = meses[:len(df)]

        # Gráfico 1: Quantidade
        fig0 = go.Figure()
        fig0.add_trace(go.Bar(x=df['Mês'], y=df['Qtd'], name='Qtd', marker=dict(color='blue')))
        fig0.update_layout(title='Quantidade por Mês', xaxis_title='Meses', yaxis_title='Quantidade')

        # Gráfico 2: Total de Vencimentos
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=df['Mês'], y=df['Total de Vencimentos (R$)'], name='Total de Vencimentos', marker=dict(color='orange')))
        fig1.update_layout(title='Total de Vencimentos por Mês', xaxis_title='Meses', yaxis_title='Valores (R$)')

        # Gráfico 3: Composição dos Vencimentos
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=df['Mês'], y=df['Outros Vencimentos (R$)'], name='Outros Vencimentos', marker=dict(color='green')))
        fig2.add_trace(go.Bar(x=df['Mês'], y=df['H. Extras'], name='H. Extras', marker=dict(color='red')))
        fig2.add_trace(go.Bar(x=df['Mês'], y=df['Diárias'], name='Diárias', marker=dict(color='blue')))
        fig2.add_trace(go.Bar(x=df['Mês'], y=df['1/3 de Férias'], name='1/3 de Férias', marker=dict(color='purple')))
        fig2.update_layout(title='Comparação de Vencimentos por Mês', xaxis_title='Meses', yaxis_title='Valores (R$)')

        # Gráfico 4: Total de Descontos
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=df['Mês'], y=df['Total de Descontos'], name='Total de Descontos', marker=dict(color='pink')))
        fig3.update_layout(title='Total de Descontos por Mês', xaxis_title='Meses', yaxis_title='Descontos (R$)')

        # Gráfico 5: Composição dos Descontos
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=df['Mês'], y=df['INSS'], name='INSS', marker=dict(color='cyan')))
        fig4.add_trace(go.Bar(x=df['Mês'], y=df['IRRF'], name='IRRF', marker=dict(color='yellow')))
        fig4.add_trace(go.Bar(x=df['Mês'], y=df['Outros Descontos'], name='Outros Descontos', marker=dict(color='gray')))
        fig4.update_layout(title='Descontos (INSS, IRRF, Outros) por Mês', xaxis_title='Meses', yaxis_title='Descontos (R$)')

        return fig0, fig1, fig2, fig3, fig4
