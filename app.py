import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from _components.inicial import inicial_layout  # Importando o layout inicial
from _components.efetivos import efetivos_layout  # Importando o layout de Efetivos
from _components.comissionados import comissionados_layout  # Importando o layout de Comissionados
from _components.agentes_politicos import agentes_politicos_layout  # Importando o layout de Agentes Políticos
from _components.estagiarios import estagiarios_layout  # Importando o layout de Estagiários  
from _components.pensionistas import pensionistas_layout  # Importando o layout de Pensionistas
from _components.aposentados import aposentados_layout  # Importando o layout de Aposentados
from _components.total import total_layout  # Importando o layout de Total
from _components.apuracao import apuracao_layout  # Importando o layout da apuração

# Inicializando o app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

# Configurações
app.config.suppress_callback_exceptions = True

# Layout do aplicativo
app.layout = dbc.Container([

    # Gráfico de apuração - agora acima
    dbc.Row([ 
        dbc.Col(
            html.Div(id='apuracao-container'),
            xs=12, md=12
        ),
    ], style={"margin-left": "240px", "padding-right": "0px"}),

    # Conteúdo dinâmico abaixo
    dbc.Row([ 
        dbc.Col(inicial_layout, xs=12, md=3, lg=2),
        dbc.Col(
            html.Div(id='dynamic-content-container'),
            xs=12, md=9, lg=10,
        ),
    ]),

    # Intervalo para atualizar os gráficos a cada 5 segundos
    dcc.Interval(
        id='interval-update',
        interval=5 * 1000,  # Atualiza a cada 5 segundos (5 * 1000 ms)
        n_intervals=0  # Inicializa com 0 intervalos
    )
], fluid=True)

# Atualizando o gráfico de apuração quando o item do checklist for selecionado
@app.callback(
    Output('apuracao-container', 'children'),  # Atualizando o novo container para apuração
    [Input('apuracao_checklist', 'value'), Input('interval-update', 'n_intervals')]  # O Input do checklist e do Interval
)
def update_apuracao_layout(selected_values, n_intervals):
    if "Apuracao_CF_art_29_A" in selected_values:  # Se "Apuração CF art. 29-A" estiver selecionado
        return apuracao_layout  # Exibe o gráfico de apuração

# Atualiza o layout com base no valor selecionado
@app.callback(
    Output('dynamic-content-container', 'children'),  # Alterei o ID aqui
    [Input('main_variable', 'value'), Input('interval-update', 'n_intervals')]  # O dropdown de mês foi removido
)
def update_layout(selected_value, n_intervals):
    if selected_value == "Efetivos":
        return efetivos_layout  # Retorna o layout de Efetivos
    elif selected_value == "Comissionados":
        return comissionados_layout
    elif selected_value == "Agentes Políticos":
        return agentes_politicos_layout
    elif selected_value == "Estagiários":
        return estagiarios_layout
    elif selected_value == "Pensionistas":
        return pensionistas_layout
    elif selected_value == "Aposentados":
        return aposentados_layout
    elif selected_value == "Total":
        return total_layout
    else:
        return html.H3("Selecione uma opção válida.")

# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=False, port=8050, host="0.0.0.0")  # Para rodar em qualquer IP
