import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
        
# Layout do aplicativo inicial
inicial_layout = dbc.Row([ 
    dbc.Col([ 
        dbc.Card([ 
            html.Img(src="assets/camara_municipal_VCA.jpg"),
            html.Hr(),
            html.Img(src="assets/LOPES CONSULTORIA.png"),
            html.Hr(),
            html.H6("Apuração CF art. 29-A"),
            # Adicionando o Checklist com a opção "Apuração CF art. 29-A"
            dcc.Checklist(
                options=[  # Adiciona a opção "Apuração CF art. 29-A"
                    {"label": "Apurações", "value": "Apuracao_CF_art_29_A"}
                    ],
                value=["Apuracao_CF_art_29_A"],  # Nenhum valor selecionado inicialmente
                id="apuracao_checklist",  # ID para o checklist  
            ),
            html.Hr(),
            html.H6("Selecione um Lote:"),
            # RadioItems que será fixo
            dcc.RadioItems(
                options=[
                    {"label": "Lote 01 - Efetivos", "value": "Lote 01 - Efetivos"},
                    {"label": "Lote 02 - Ag. Políticos", "value": "Lote 02 - Ag. Políticos"},
                    {"label": "Lote 03 - Aposentados e Pensionistas", "value": "Lote 03 - Aposentados e Pensionistas"},
                    {"label": "Lote 05 - Assessores Parlamentares", "value": "Lote 05 - Assessores Parlamentares"},
                    {"label": "Lote 06 - Comissionados", "value": "Lote 06 - Comissionados"},
                    {"label": "Lote 11 - Estagiários", "value": "Lote 11 - Estagiários"},
                    {"label": "Total", "value": "Total"},
                ],
                value="Lote 01 - Efetivos",  # Valor padrão
                id="main_variable",  # ID para a seleção
            ),
        ], className="fixed-radio-items"),
]),

    # Alterei o ID para "dynamic-content-container-right" para evitar duplicação
    dbc.Col([ 
        html.Div(id="dynamic-content-container-right")  # Alterei o ID aqui
    ])
])
