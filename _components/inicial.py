from dash import dcc, html
import dash_bootstrap_components as dbc

inicial_layout = html.Div([
    # Botão hambúrguer visível apenas no celular
    html.Button("☰ Menu", id="btn-toggle-menu", className="btn btn-primary d-md-none", style={"margin": "10px"}),

    # Barra lateral fixa no desktop, overlay no mobile
    html.Div([
        dbc.Card([
            html.Img(src="assets/camara_municipal_VCA.jpg"),
            html.Hr(),
            html.Img(src="assets/LOPES CONSULTORIA.png"),
            html.Hr(),
            html.H6("Apuração CF art. 29-A"),
            dcc.Checklist(
                options=[{"label": "Apurações", "value": "Apuracao_CF_art_29_A"}],
                value=["Apuracao_CF_art_29_A"],
                id="apuracao_checklist"
            ),
            html.Hr(),
            html.H6("Selecione um Lote:"),
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
                value="Lote 01 - Efetivos",
                id="main_variable"
            ),
        ], className="fixed-radio-items p-2")
    ], id="side-menu"),

    html.Div(id="dynamic-content-container-right")
])
