from dash import Dash, dcc, html, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from _components.inicial import inicial_layout
from _components.efetivos import layout_efetivos, registrar_callbacks_efetivos
from _components.comissionados import layout_comissionados, registrar_callbacks_comissionados
from _components.agentes_politicos import layout_agentes_politicos, registrar_callbacks_agentes
from _components.estagiarios import layout_estagiarios, registrar_callbacks_estagiarios
from _components.assessores_parlamentares import layout_assessores_parlamentares, registrar_callbacks_assessores_parlamentares
from _components.aposentados import layout_aposentados, registrar_callbacks_aposentados
from _components.total import layout_total, registrar_callbacks_total
from _components.apuracao import layout_apuracao, registrar_callbacks_apuracao
from utils import carregar_dados_drive

# Inicialização do Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
app.title = "Apuração de Dados CMVC"
app._favicon = "assets/favicon.ico"

# Configuração do servidor
server = app.server
app.config.suppress_callback_exceptions = True

# Layout do aplicativo
app.layout = dbc.Container([
    dcc.Interval(id='interval-update', interval=10 * 1000, n_intervals=0),
    dcc.Store(id='data-store'),

    # Layout inicial (barra lateral e botão de menu)
    dbc.Row([
        dbc.Col(inicial_layout)
    ]),

    # Gráfico de apuração fixo
    dbc.Row([
        dbc.Col(html.Div(id='apuracao-container'), xs=12)
    ]),

    # Checklist e gráficos
    dbc.Row([
        dbc.Col(html.Div(id='dynamic-content-container'), xs=12)
    ])
], fluid=True)

# Callback: atualiza layout de apuração
@app.callback(
    Output('apuracao-container', 'children'),
    Input('apuracao_checklist', 'value')
)
def update_apuracao_layout(selected_values):
    if "Apuracao_CF_art_29_A" in selected_values:
        return layout_apuracao()

# Callback: troca layout com base na seleção
@app.callback(
    Output('dynamic-content-container', 'children'),
    Input('main_variable', 'value')
)
def update_layout(selected_value):
    if selected_value is None:
        return html.H3("Selecione uma opção válida.")

    titulo = html.H5(f"Valores do {selected_value} Por Mês", className="my-4 text-center")

    if selected_value == "Lote 01 - Efetivos":
        return html.Div([titulo, layout_efetivos()])
    elif selected_value == "Lote 02 - Ag. Políticos":
        return html.Div([titulo, layout_agentes_politicos()])
    elif selected_value == "Lote 03 - Aposentados e Pensionistas":
        return html.Div([titulo, layout_aposentados()])
    elif selected_value == "Lote 05 - Assessores Parlamentares":
        return html.Div([titulo, layout_assessores_parlamentares()])
    elif selected_value == "Lote 06 - Comissionados":
        return html.Div([titulo, layout_comissionados()])
    elif selected_value == "Lote 11 - Estagiários":
        return html.Div([titulo, layout_estagiarios()])
    elif selected_value == "Total":
        return html.Div([
            html.H4("Valores Totais por mês", className="my-4 text-center"),
            layout_total()
        ])
    else:
        return html.H3("Selecione uma opção válida.")

# Callback: recarrega dados periodicamente
@app.callback(
    Output('data-store', 'data'),
    Input('interval-update', 'n_intervals')
)
def atualizar_dados(_):
    df = carregar_dados_drive()
    return df.to_dict('records')

@app.callback(
    Output("side-menu", "style"),
    Input("btn-toggle-menu", "n_clicks"),
    Input("main_variable", "value"),
    Input("apuracao_checklist", "value"),
    State("side-menu", "style"),
    prevent_initial_call=True
)
def toggle_menu(btn_clicks, main_var, checklist_value, current_style):
    triggered_id = ctx.triggered_id

    if triggered_id == "btn-toggle-menu":
        # Abrir/fechar com o botão
        if not current_style or current_style.get("display") == "none":
            return {"display": "block"}
        else:
            return {"display": "none"}
    else:
        # Fechar ao selecionar algo no menu
        return {"display": "none"}

# Registro de callbacks
registrar_callbacks_efetivos(app)
registrar_callbacks_comissionados(app)
registrar_callbacks_agentes(app)
registrar_callbacks_estagiarios(app)
registrar_callbacks_assessores_parlamentares(app)
registrar_callbacks_aposentados(app)
registrar_callbacks_total(app)
registrar_callbacks_apuracao(app)

# Execução local
if __name__ == "__main__":
    app.run(debug=False, port=8050, host="0.0.0.0")
    