from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

def layout_estagiarios():
    return dbc.Row([
        *[
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(
                            id=f'fig{i}_estagiarios',
                            className="grafico-estagiario",
                            style={
                                "width": "100%",
                                "maxWidth": "100%",
                                "height": "2000px",
                                "width": "100%"
                            }
                        )
                    ]),
                    className="grafico-estagiario-card"
                ),
                id=f'col{i}_estagiarios', xs=12, md=6
            )
            for i in range(10)
        ]
    ])

def registrar_callbacks_estagiarios(app):
    @app.callback(
        [Output(f'fig{i}_estagiarios', 'figure') for i in range(10)] +
        [Output(f'col{i}_estagiarios', 'style') for i in range(10)],
        Input('data-store', 'data')
    )
    def atualizar_graficos_estagiarios(data):
        df_raw = pd.DataFrame(data)
        registros = []

        janeiro_dados = df_raw.iloc[7]
        periodo = janeiro_dados[1]
        status = "REALIZADO"

        registros.append({
            "Período": periodo,
            "Status": status,
            "Lotes": "Lote 11 - Estagiários",
            "Qtd": janeiro_dados[1],
            "Salário Base Total (R$)": janeiro_dados[2],
            "Outros Vencimentos (R$)": janeiro_dados[3],
            "1/3 de Férias": janeiro_dados[4],
            "Média Valor Férias/H.Extras": janeiro_dados[5],
            "Total de Vencimentos (R$)": janeiro_dados[6],
            "INSS Padronal": janeiro_dados[7],
            "Verbas Indenizatórias": janeiro_dados[8],
            "Licença Prêmio": janeiro_dados[9],
            "Abono Pecuniário + 1/3 do Abono": janeiro_dados[10],
        })

        for i in range(len(df_raw)):
            row = df_raw.iloc[i]
            if isinstance(row[0], str) and "Período:" in row[0] and i != 7:
                periodo = row[1]
                status = str(row[3]).strip().upper() if pd.notna(row[3]) else None
                header_index = None
                for offset in range(1, 6):
                    if i + offset >= len(df_raw):
                        break
                    possible_header = df_raw.iloc[i + offset]
                    if any(isinstance(cell, str) and "Lotes" in str(cell) for cell in possible_header):
                        header_index = i + offset
                        break
                if header_index is None and i + 2 < len(df_raw):
                    possible_header = df_raw.iloc[i + 2]
                    if any(isinstance(cell, str) and "Lotes" in str(cell) for cell in possible_header):
                        header_index = i + 2
                if header_index is None:
                    continue

                j = header_index + 1
                while j < len(df_raw):
                    linha = df_raw.iloc[j]
                    if pd.isna(linha[0]) or "Período:" in str(linha[0]):
                        break
                    registros.append({
                        "Período": periodo,
                        "Status": status,
                        "Lotes": linha[0],
                        "Qtd": linha[1],
                        "Salário Base Total (R$)": linha[2],
                        "Outros Vencimentos (R$)": linha[3],
                        "1/3 de Férias": linha[4],
                        "Média Valor Férias/H.Extras": linha[5],
                        "Total de Vencimentos (R$)": linha[6],
                        "INSS Padronal": linha[7],
                        "Verbas Indenizatórias": linha[8],
                        "Licença Prêmio": linha[9],
                        "Abono Pecuniário + 1/3 do Abono": linha[10],
                    })
                    j += 1

        df = pd.DataFrame(registros)
        df['Lotes'] = df['Lotes'].astype(str).str.strip()
        df = df[df['Lotes'] == 'Lote 11 - Estagiários'].reset_index(drop=True)

        df['Mês'] = df['Período'].str.extract(r'([\wº]+)(?=/2025)')[0].str.strip().str.capitalize()

        meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro', '13º'
        ]
        df = df[df['Mês'].isin(meses)]
        dados_por_mes = df.set_index('Mês').reindex(meses)

        dados_por_mes.at['Janeiro', 'Qtd'] = janeiro_dados[1]
        dados_por_mes.at['Janeiro', 'Salário Base Total (R$)'] = janeiro_dados[2]
        dados_por_mes.at['Janeiro', 'Outros Vencimentos (R$)'] = janeiro_dados[3]
        dados_por_mes.at['Janeiro', '1/3 de Férias'] = janeiro_dados[4]
        dados_por_mes.at['Janeiro', 'Média Valor Férias/H.Extras'] = janeiro_dados[5]
        dados_por_mes.at['Janeiro', 'Total de Vencimentos (R$)'] = janeiro_dados[6]
        dados_por_mes.at['Janeiro', 'INSS Padronal'] = janeiro_dados[7]
        dados_por_mes.at['Janeiro', 'Verbas Indenizatórias'] = janeiro_dados[8]
        dados_por_mes.at['Janeiro', 'Licença Prêmio'] = janeiro_dados[9]
        dados_por_mes.at['Janeiro', 'Abono Pecuniário + 1/3 do Abono'] = janeiro_dados[10]
        dados_por_mes.at['Janeiro', 'Status'] = "REALIZADO"

        opacities = [
            1.0 if str(dados_por_mes.at[m, 'Status']).strip().upper() == 'REALIZADO' else 0.5
            for m in meses
        ]

        def get_col_data(col):
            return [dados_por_mes[col].get(m, 0) for m in meses]

        def fmt(v):
            v = 0 if pd.isna(v) else v
            return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        def make_fig(title, col, color, est_color, is_currency):
            vals = get_col_data(col)
            texts = [fmt(v) if is_currency else str(int(v)) if pd.notna(v) else '0' for v in vals]
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=meses,
                x=vals,
                marker=dict(color=color, opacity=opacities),
                text=texts,
                textposition='auto',
                orientation='h',
                showlegend=False
            ))
            fig.add_trace(go.Bar(x=[None], y=[None], name='Realizado',
                                 marker=dict(color=color, opacity=1.0), showlegend=True))
            fig.add_trace(go.Bar(x=[None], y=[None], name='Estimado',
                                 marker=dict(color=est_color, opacity=0.5), showlegend=True))
            fig.update_layout(
                title=title,
                yaxis_title='Meses',
                xaxis_title='Valor (R$)' if is_currency else 'Quantidade',
                yaxis=dict(autorange='reversed'),
                xaxis=dict(tickvals=[]),
                legend=dict(title='Legenda', orientation='v', x=1.02, y=1)
            )
            return fig

        specs = [
            ('Salário Base Total por Mês',    'Salário Base Total (R$)',    'blue',    'lightblue', True),
            ('Quantidade de Estagiários por Mês','Qtd',                     'orange',  '#FFCC80',    False),
            ('Total de Vencimentos por Mês',  'Total de Vencimentos (R$)',  'green',   'lightgreen', True),
            ('Outros Vencimentos',            'Outros Vencimentos (R$)',    'red',     'lightcoral', True),
            ('Férias/H.Extras',               'Média Valor Férias/H.Extras','purple',  'lavender',   True),
            ('1/3 de Férias',                 '1/3 de Férias',              'cyan',    'lightcyan',  True),
            ('Abono Pecuniário + 1/3 do Abono','Abono Pecuniário + 1/3 do Abono','yellow','lightyellow',True),
            ('Licença Prêmio',                'Licença Prêmio',             'gray',    'lightgray',  True),
            ('INSS',                          'INSS Padronal',              'green',   'lightgreen', True),
            ('Verbas Indenizatórias',         'Verbas Indenizatórias',      'purple',  'lavender',   True),
        ]

        figs = [make_fig(*s) for s in specs]

        styles = []
        for _, col, *_ in specs:
            vals = df[col].fillna(0)
            styles.append({'display': 'none'} if (vals == 0).all() else {})

        print("\n\n📌 DEBUG - DADOS ESTAGIÁRIOS LOTE 11:")
        print(df[['Mês', 'Período', 'Lotes', 'Qtd', 'Salário Base Total (R$)', 'Status']])

        return figs + styles
