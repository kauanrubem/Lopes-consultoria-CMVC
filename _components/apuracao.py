from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

def layout_apuracao():
    return dbc.Card([
        dbc.CardHeader("Apuração CF art. 29-A"),
        dbc.CardBody([
            html.Div(id="apuracao-graficos")
        ])
    ])

def registrar_callbacks_apuracao(app):
    @app.callback(
        Output("apuracao-graficos", "children"),
        Input("data-store", "data")
    )
    def atualizar_graficos_apuracao(data):
        df = pd.DataFrame(data)

        # ----- TABELA DE APURAÇÃO -----
        df_apuracao = df.iloc[211:218].copy()
        df_apuracao.columns = df_apuracao.iloc[0]
        df_apuracao = df_apuracao.iloc[1:].reset_index(drop=True)

        col_lote = df_apuracao.columns[0]
        colunas_valores = df_apuracao.columns[1:11]

        def formatar_valor(valor, nome_coluna):
            try:
                nome_coluna = str(nome_coluna).strip().lower()
                valor_float = float(str(valor).strip())
                if nome_coluna == "qtd":
                    return f"{int(valor_float)}"
                else:
                    return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                return "-"

        cards = []

        for idx, linha in df_apuracao.iterrows():
            nome_lote = linha[col_lote]

            valores = []
            valores_formatados = []
            text_positions = []

            for col in colunas_valores:
                valor = pd.to_numeric(str(linha[col]).strip(), errors='coerce')
                valores.append(valor)
                valores_formatados.append(formatar_valor(valor, col))
                text_positions.append("outside" if str(col).strip().lower() == "qtd" else "auto")

            cor = ['indigo', 'green', 'orange', 'darkred', 'darkblue',
                   'purple', 'teal', 'darkcyan', 'slategray', 'crimson'][idx % 10]

            fig = go.Figure()
            for y, x, text, pos in zip(colunas_valores, valores, valores_formatados, text_positions):
                fig.add_trace(go.Bar(
                    x=[x],
                    y=[y],
                    orientation='h',
                    text=[text],
                    texttemplate='%{text}',
                    textposition=pos,
                    marker_color=cor,
                    showlegend=False
                ))

            fig.update_layout(
                title=nome_lote,
                xaxis_title="Valor",
                yaxis_title="Indicadores",
                margin=dict(l=180, r=20, t=50, b=40),
                height=400,
                showlegend=False
            )

            cards.append(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([dcc.Graph(figure=fig)]),
                        className="mb-4"
                    ),
                    xs=12, md=6
                )
            )

        linhas = []
        for i in range(0, len(cards), 2):
            linhas.append(dbc.Row(cards[i:i+2], className="mb-3"))

        # ----- TABELA RESUMO DA APURAÇÃO -----
        df_resumo = df.iloc[227:234].copy()
        df_resumo.columns = df_resumo.iloc[0]
        df_resumo = df_resumo.iloc[1:].reset_index(drop=True)

        resumo_titulos = [
            "Estimativa TCM-BA Duodécimo 2025",
            "Salário Base Total (R$)",
            "Outros Vencimentos (R$)",
            "Estimativa Folha para fins CF art. 29-A",
            "Apuração CF art. 29-A"
        ]

        resumo_valores = []
        for i, titulo in enumerate(resumo_titulos):
            linha_atual = df_resumo.iloc[i]
            valor = next((v for v in linha_atual if pd.api.types.is_number(v)), None)
            try:
                if "apuração" in titulo.lower():
                    valor_formatado = f"{float(valor) * 100:.2f}%"
                else:
                    valor_formatado = f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                valor_formatado = "-"
            resumo_valores.append((titulo, valor_formatado))

        cards_resumo = [
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H6(titulo, className="card-title text-center"),
                        html.H4(valor, className="card-text text-center")
                    ])
                ], className="mb-4"),
                xs=12, sm=6, md=6, lg=4
            )
            for titulo, valor in resumo_valores
        ]

        linhas.append(dbc.Row(cards_resumo, className="mt-2"))

        return linhas
