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
            
            # Adicionando o Checklist com a opção "Apuração CF art. 29-A"
            dcc.Checklist(
                 options=[  # Adiciona a opção "Apuração CF art. 29-A"
                    {"label": "Estimativas e Apurações", "value": "Apuracao_CF_art_29_A"}
                    ],
                value=["Apuracao_CF_art_29_A"],  # Nenhum valor selecionado inicialmente
                id="apuracao_checklist",  # ID para o checklist  
            ),
            html.Hr(),
            # RadioItems que será fixo
            dcc.RadioItems(
                options=[
                    {"label": "Efetivos", "value": "Efetivos"},
                    {"label": "Comissionados", "value": "Comissionados"},
                    {"label": "Agentes Políticos", "value": "Agentes Políticos"},
                    {"label": "Estagiários", "value": "Estagiários"},
                    {"label": "Pensionistas", "value": "Pensionistas"},
                    {"label": "Aposentados", "value": "Aposentados"},
                    {"label": "Total", "value": "Total"},
                ],
                value="Efetivos",  # Valor padrão
                id="main_variable",  # ID para a seleção
            ),
            html.Hr(),
        ], className="fixed-radio-items"),
    ], width=2),

    # Alterei o ID para "dynamic-content-container-right" para evitar duplicação
    dbc.Col([ 
        html.Div(id="dynamic-content-container-right")  # Alterei o ID aqui
    ], width=10)
])
