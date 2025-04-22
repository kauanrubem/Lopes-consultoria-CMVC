import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Layouts e callbacks dos componentes
from _components.inicial import inicial_layout
from _components.efetivos import layout_efetivos, registrar_callbacks_efetivos
from _components.comissionados import layout_comissionados, registrar_callbacks_comissionados
from _components.agentes_politicos import layout_agentes_politicos, registrar_callbacks_agentes
from _components.estagiarios import layout_estagiarios, registrar_callbacks_estagiarios
from _components.pensionistas import layout_pensionistas, registrar_callbacks_pensionistas
from _components.aposentados import layout_aposentados, registrar_callbacks_aposentados
from _components.total import layout_total, registrar_callbacks_total
from _components.apuracao import layout_apuracao, registrar_callbacks_apuracao
from utils import carregar_dados_drive

# Inicialização do Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server
app.config.suppress_callback_exceptions = True

# Layout do aplicativo
app.layout = dbc.Container([
    dcc.Interval(id='interval-update', interval=5 * 1000, n_intervals=0),  # Atualiza a cada 5 segundos
    dcc.Store(id='data-store'),  # Armazena os dados atualizados da planilha

    # Gráfico de apuração fixo
    dbc.Row([
        dbc.Col(html.Div(id='apuracao-container'), xs=12)
    ], style={"margin-left": "240px", "padding-right": "0px"}),

    # Conteúdo dinâmico (layouts por regime)
    dbc.Row([
        dbc.Col(inicial_layout, xs=12, md=3, lg=2),
        dbc.Col(html.Div(id='dynamic-content-container'), xs=12, md=9, lg=10),
    ])
], fluid=True)

# Callback para atualizar o layout de apuração
@app.callback(
    Output('apuracao-container', 'children'),
    [Input('apuracao_checklist', 'value')]
)
def update_apuracao_layout(selected_values):
    if "Apuracao_CF_art_29_A" in selected_values:
        return layout_apuracao()

# Callback para trocar o layout com base na seleção
@app.callback(
    Output('dynamic-content-container', 'children'),
    [Input('main_variable', 'value')]
)
def update_layout(selected_value):
    if selected_value == "Efetivos":
        return layout_efetivos()
    elif selected_value == "Comissionados":
        return layout_comissionados()
    elif selected_value == "Agentes Políticos":
        return layout_agentes_politicos()
    elif selected_value == "Estagiários":
        return layout_estagiarios()
    elif selected_value == "Pensionistas":
        return layout_pensionistas()
    elif selected_value == "Aposentados":
        return layout_aposentados()
    elif selected_value == "Total":
        return layout_total()
    else:
        return html.H3("Selecione uma opção válida.")

# Callback que recarrega os dados da planilha periodicamente
@app.callback(
    Output('data-store', 'data'),
    Input('interval-update', 'n_intervals')
)
def atualizar_dados(_):
    df = carregar_dados_drive()
    return df.to_dict('records')

# Registro de todos os callbacks por regime
registrar_callbacks_efetivos(app)
registrar_callbacks_comissionados(app)
registrar_callbacks_agentes(app)
registrar_callbacks_estagiarios(app)
registrar_callbacks_pensionistas(app)
registrar_callbacks_aposentados(app)
registrar_callbacks_total(app)
registrar_callbacks_apuracao(app)

# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=False, port=8050, host="0.0.0.0")
