from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

# Layout da seção de apuração
def layout_apuracao():
    return dbc.Row([
        # Gráfico de Pizza
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='grafico-pizza'),
            html.H6(id='texto-pizza', style={"textAlign": "left", "marginTop": "15px"})
        ])), width=12),

        # Gráfico INSS Patronal
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='grafico-inss'),
            html.H6(id='texto-inss', style={"textAlign": "center", "marginTop": "15px"})
        ])), width=6),

        # Gráfico Estimativa x Apuração
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='grafico-apuracao'),
            html.H6(id='texto-apuracao', style={"textAlign": "center", "marginTop": "15px"})
        ])), width=6),
    ])

# Callback que atualiza os gráficos de apuração com base nos dados carregados
def registrar_callbacks_apuracao(app):
    @app.callback(
        [Output('grafico-pizza', 'figure'),
         Output('texto-pizza', 'children'),
         Output('grafico-inss', 'figure'),
         Output('texto-inss', 'children'),
         Output('grafico-apuracao', 'figure'),
         Output('texto-apuracao', 'children')],
        Input('data-store', 'data')
    )
    def atualizar_graficos_apuracao(data):
        df = pd.DataFrame(data)

        # Valores principais
        valor_estimativa_total = pd.to_numeric(df.iloc[214, 7], errors='coerce')
        valor_apuracao = pd.to_numeric(df.iloc[215, 7], errors='coerce')
        valor_apuracao_percent = round(valor_apuracao * 100, 2)
        complemento = round(100 - valor_apuracao_percent, 2)

        # Gráfico de pizza
        fig_pizza = go.Figure()
        fig_pizza.add_trace(go.Pie(
            labels=['Apuração CF art. 29-A', 'Não Apurado'],
            values=[valor_apuracao_percent, complemento],
            hole=0.3
        ))
        fig_pizza.update_layout(
    title_text='Estimativa Não Considerando INSS Patronal dos Agentes Políticos',
    height=420,  # aumenta a altura do gráfico
)

        texto_pizza = f"Estimativa da Folha: R$ {valor_estimativa_total:,.2f} | Apuração: {valor_apuracao_percent:.2f}%",
        style={"textAlign": "left", "marginTop": "15px"}

        # Subtabela com dados de INSS e apuração por mês
        df_tabelas = df.iloc[195:211].reset_index(drop=True)
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

        # Totais finais (linha 211)
        linha_total = df.iloc[209]
        total_agentes = pd.to_numeric(linha_total[1], errors='coerce')
        total_servidores = pd.to_numeric(linha_total[3], errors='coerce')
        total_estimativa = pd.to_numeric(linha_total[7], errors='coerce')
        total_apuracao = pd.to_numeric(linha_total[10], errors='coerce')

        # Gráfico INSS Patronal
        fig_inss = go.Figure()
        fig_inss.add_trace(go.Bar(
            y=df_dados['Comp'], x=df_dados['Agentes_Politicos'],
            name='Agentes Políticos', marker_color='indianred', orientation='h'
        ))
        fig_inss.add_trace(go.Bar(
            y=df_dados['Comp'], x=df_dados['Servidores'],
            name='Servidores', marker_color='seagreen', orientation='h'
        ))
        fig_inss.update_layout(title='INSS Patronal: Agentes Políticos vs Servidores', barmode='group', height=600)

        texto_inss = f"Total - Agentes Políticos: R$ {total_agentes:,.2f} | Servidores: R$ {total_servidores:,.2f}"

        # Gráfico Estimativa x Apuração
        fig_apuracao = go.Figure()
        fig_apuracao.add_trace(go.Bar(
            y=df_dados['Comp'], x=df_dados['Estimativa_Total'],
            name='Estimativa Total da Folha', marker_color='orange', orientation='h'
        ))
        fig_apuracao.add_trace(go.Bar(
            y=df_dados['Comp'], x=df_dados['Apuracao_29A'],
            name='Apuração CF art. 29-A', marker_color='blue', orientation='h'
        ))
        fig_apuracao.update_layout(title='Estimativa vs Apuração CF art. 29-A', barmode='group', height=600)

        texto_apuracao = f"Total - Estimativa: R$ {total_estimativa:,.2f} | Apuração: R$ {total_apuracao:,.2f}"

        return fig_pizza, texto_pizza, fig_inss, texto_inss, fig_apuracao, texto_apuracao
