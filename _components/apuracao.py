from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import flask

def layout_apuracao():
    return dbc.Card([
        dbc.CardHeader("Apuração CF art. 29-A"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Div(id="apuracao-grafico"),
                            html.Div(id="apuracao-totalizador", className="text-end fw-bold mt-2")
                        ]),
                        className="card-grafico"
                    ),
                    width=9,
                    id="apuracao-col-grafico"
                ),
                dbc.Col(
                    html.Div(id="apuracao-cards"),
                    width=3,
                    id="apuracao-col-cards"
                )
            ], className="apuracao-row"),
        ])
    ])

def registrar_callbacks_apuracao(app):
    @app.callback(
        [Output("apuracao-cards", "children"),
         Output("apuracao-grafico", "children"),
         Output("apuracao-totalizador", "children")],
        Input("data-store", "data")
    )
    def atualizar_apuracao(data):
        df = pd.DataFrame(data)

        df_apuracao = df.iloc[211:218].copy()
        df_apuracao.columns = df_apuracao.iloc[0]
        df_apuracao = df_apuracao.iloc[1:].reset_index(drop=True)

        col_lote = df_apuracao.columns[0]

        def formatar_valor(valor):
            try:
                valor_float = float(str(valor).strip())
                return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                return "-"

        resumo_titulos = [
            ("Estimativa TCM-BA Duodécimo 2025", "Estimativa TCM-BA Duodécimo 2025"),
            ("Estimativa Folha para fins CF art. 29-A", "Estimativa Folha total para fins CF art. 29-A"),
            ("Apuração CF art. 29-A", "Apuração CF art. 29-A")
        ]

        linhas_resumo = df[df.apply(
            lambda row: row.astype(str).str.contains(
                "|".join([termo for _, termo in resumo_titulos]),
                case=False
            ).any(), axis=1)].copy()

        resumo_valores = []
        for titulo_card, termo_busca in resumo_titulos:
            linha_match = linhas_resumo[linhas_resumo.apply(
                lambda row: row.astype(str).str.contains(termo_busca, case=False).any(), axis=1)]
            if not linha_match.empty:
                linha = linha_match.iloc[0]
                valor = next((v for v in linha if pd.api.types.is_number(v)), None)
                try:
                    if "apuração" in titulo_card.lower():
                        valor_formatado = f"{float(valor) * 100:.2f}%"
                    else:
                        valor_formatado = formatar_valor(valor)
                except:
                    valor_formatado = "-"
            else:
                valor_formatado = "-"
            resumo_valores.append((titulo_card, valor_formatado))

        cards_resumo = dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H6(titulo, className="card-title text-center"),
                        html.H4(valor, className="card-text text-center")
                    ])
                ], className="card-resumo mb-4"),
                width=12
            )
            for titulo, valor in resumo_valores
        ])

        totais = {
            "Lote": [],
            "Total Somado (R$)": []
        }

        def parse_valor(v):
            try:
                v_str = str(v).replace("R$", "").replace("\xa0", "").strip()
                if "." in v_str and "," in v_str:
                    v_str = v_str.replace(".", "").replace(",", ".")
                elif "," in v_str:
                    v_str = v_str.replace(",", ".")
                return float(v_str)
            except:
                return 0.0

        total_salario = total_outros = 0.0

        for _, linha in df_apuracao.iterrows():
            nome = linha[col_lote]
            base = parse_valor(linha['Salário Base Total (R$)'])
            outros = parse_valor(linha['Outros Vencimentos (R$)'])
            if nome == "Total":
                total_salario = base
                total_outros = outros
                continue
            totais["Lote"].append(nome)
            totais["Total Somado (R$)"].append(base + outros)

        texto = [formatar_valor(v) for v in totais["Total Somado (R$)"]]

        def abreviar_lote(nome):
            mapa = {
                "Lote 01 - Efetivos": "Efetivos",
                "Lote 02 - Ag. Políticos": "Ag. Políticos",
                "Lote 03 - Aposentados e Pensionistas": "Aposentados",
                "Lote 05 - Assessores Parlamentares": "Assessores",
                "Lote 06 - Comissionados": "Comissionados",
                "Lote 11 - Estagiários": "Estagiários"
            }
            return mapa.get(nome, nome)

        nomes_exibidos = [abreviar_lote(lote) for lote in totais["Lote"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=nomes_exibidos,
            y=totais["Total Somado (R$)"],
            orientation='v',
            marker_color='teal',
            text=texto,
            textposition='auto',
            texttemplate='%{text}'
        ))
        fig.update_layout(
            title="Totais de Cada Lote (Salário Base + Outros Vencimentos)",
            xaxis_title="Lote",
            yaxis_title="Valor (R$)",
            barmode='group',
            height=600,
            showlegend=False
        )

        totalizador_texto = html.Div(
            f"Total do Salário Base: {formatar_valor(total_salario)} / Total dos Outros Vencimentos: {formatar_valor(total_outros)}"
        )

        return cards_resumo, dcc.Graph(figure=fig), totalizador_texto
