from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import datetime

def layout_total():
    return dbc.Row([
        *[
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(
                            id=f'fig{i}_total',
                            className="grafico-total",
                            style={
                                "width": "100%",
                                "maxWidth": "100%",
                                "height": "2000px",
                            }
                        )
                    ]),
                    className="grafico-total-card"
                ),
                id=f'col{i}_total', xs=12, md=6
            )
            for i in range(10)
        ]
    ])

def registrar_callbacks_total(app):
    @app.callback(
        [Output(f'fig{i}_total', 'figure') for i in range(10)] +
        [Output(f'col{i}_total', 'style') for i in range(10)],
        Input('data-store', 'data')
    )
    def atualizar_graficos_total(data):
        df = pd.DataFrame(data).iloc[2:].reset_index(drop=True).iloc[:, :11]
        df.columns = [
            'Lotes', 'Qtd', 'Salário Base Total (R$)', 'Outros Vencimentos (R$)',
            '1/3 de Férias', 'Média Valor Férias/H.Extras', 'Total de Vencimentos (R$)',
            'INSS Padronal', 'Verbas Indenizatórias', 'Licença Prêmio',
            'Abono Pecuniário + 1/3 do Abono'
        ]
        df['Lotes'] = df['Lotes'].str.strip()

        current = None
        periods = []
        for _, row in df.iterrows():
            if pd.notna(row['Lotes']) and '2025' in row['Lotes']:
                current = row['Lotes']
            periods.append(current)
        df['Período'] = periods

        df = df[df['Lotes'] == 'Total'].reset_index(drop=True)

        meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro',
            'Dezembro', '13º Mês'
        ]
        month_idx = {m: i+1 for i, m in enumerate(meses[:-1])}

        periodo = df['Período'].iloc[0] if not df.empty else None
        if isinstance(periodo, str) and '/' in periodo:
            mes_str, _ = periodo.split('/')
            mes_atual = month_idx.get(mes_str, datetime.datetime.now().month)
        else:
            mes_atual = datetime.datetime.now().month

        opacities = [
            1.0 if (month_idx.get(m, 0) <= mes_atual and m != '13º Mês') else 0.5
            for m in meses
        ]

        df['Mês'] = df['Período'].str.extract(r'([\wº]+)(?=/2025)')[0].str.strip().str.capitalize()

        def fmt(v):
            v = 0 if pd.isna(v) else v
            return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        def make_fig(title, col, color, est_color, is_currency):
            vals = df[col]
            texts = vals.apply(fmt) if is_currency else vals.fillna(0).astype(int).apply(str)
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
                legend=dict(title='Legenda', orientation='v', x=1.02, y=1),
                margin=dict(r=150)
            )
            return fig

        specs = [
            ('Salário Base Total por Mês',    'Salário Base Total (R$)',   'blue',    'lightblue', True),
            ('Quantidade Total por Mês',       'Qtd',                       'orange',  '#FFCC80',    False),
            ('Total de Vencimentos por Mês',   'Total de Vencimentos (R$)', 'green',   'lightgreen', True),
            ('Outros Vencimentos',             'Outros Vencimentos (R$)',   'red',     'lightcoral', True),
            ('Férias/H.Extras',                'Média Valor Férias/H.Extras','purple',  'lavender',   True),
            ('1/3 de Férias',                  '1/3 de Férias',              'cyan',    'lightcyan',  True),
            ('Abono Pecuniário + 1/3 do Abono','Abono Pecuniário + 1/3 do Abono','yellow','lightyellow',True),
            ('Licença Prêmio',                 'Licença Prêmio',             'gray',    'lightgray',  True),
            ('INSS',                           'INSS Padronal',              'green',   'lightgreen', True),
            ('Verbas Indenizatórias',          'Verbas Indenizatórias',      'purple',  'lavender',   True),
        ]

        figs = [make_fig(*s) for s in specs]
        styles = [
            {'display': 'none'} if (df[col].fillna(0) == 0).all() else {}
            for _, col, *_ in specs
        ]

        return figs + styles
