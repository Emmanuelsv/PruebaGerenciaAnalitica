import pandas as pd
import psycopg2
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

conn = psycopg2.connect(
    dbname="BaseDatosPruebaTalentoB",
    user="gerentecomercial",
    password="gerentecomercial",
    host="localhost",
    port='5432'
)

def execute_query(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=columns)

# Consultas SQL
query_client_portfolio = """
SELECT id_sistema_cliente, macroactivo, cod_activo, SUM(aba) as total_aba
FROM historico_aba_macroactivos_clean
GROUP BY id_sistema_cliente, macroactivo, cod_activo;
"""

query_banking_portfolio = """
SELECT b.banca, h.macroactivo, SUM(h.aba) as total_aba
FROM historico_aba_macroactivos_clean h
LEFT JOIN catalogo_banca b ON CAST(h.cod_banca AS TEXT) = CAST(b.cod_banca AS TEXT)
GROUP BY b.banca, h.macroactivo;
"""

query_risk_profile_portfolio = """
SELECT p.perfil_riesgo, h.macroactivo, SUM(h.aba) as total_aba
FROM historico_aba_macroactivos_clean h
LEFT JOIN cat_perfil_riesgo p ON CAST(h.cod_perfil_riesgo AS TEXT) = CAST(p.cod_perfil_riesgo AS TEXT)
GROUP BY p.perfil_riesgo, h.macroactivo;
"""

query_aba_evolution = """
SELECT ingestion_year, ingestion_month, AVG(aba) as avg_aba
FROM historico_aba_macroactivos_clean
GROUP BY ingestion_year, ingestion_month
ORDER BY ingestion_year, ingestion_month;
"""

df_client_portfolio = execute_query(query_client_portfolio)
df_banking_portfolio = execute_query(query_banking_portfolio)
df_risk_profile_portfolio = execute_query(query_risk_profile_portfolio)
df_aba_evolution = execute_query(query_aba_evolution)

df_aba_evolution['ingestion_month'] = df_aba_evolution['ingestion_month'].astype(int)

df_aba_evolution['date'] = pd.to_datetime(df_aba_evolution['ingestion_year'].astype(str) + '-' + df_aba_evolution['ingestion_month'].astype(str).str.zfill(2) + '-01')

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Análisis de Portafolio de Clientes"),

    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Portafolio por Cliente', value='tab-1'),
        dcc.Tab(label='Portafolio por Banca', value='tab-2'),
        dcc.Tab(label='Portafolio por Perfil de Riesgo', value='tab-3'),
        dcc.Tab(label='Evolución del ABA', value='tab-4'),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Dropdown(
                id='client-dropdown',
                options=[{'label': i, 'value': i} for i in df_client_portfolio['id_sistema_cliente'].unique()],
                value=df_client_portfolio['id_sistema_cliente'].unique()[0]
            ),
            dcc.Graph(id='client-portfolio-graph')
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                id='banking-portfolio-graph',
                figure=px.pie(df_banking_portfolio, names='macroactivo', values='total_aba', title='Portafolio por Banca')
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            dcc.Graph(
                id='risk-profile-portfolio-graph',
                figure=px.pie(df_risk_profile_portfolio, names='macroactivo', values='total_aba', title='Portafolio por Perfil de Riesgo')
            )
        ])
    elif tab == 'tab-4':
        return html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df_aba_evolution['date'].min(),
                end_date=df_aba_evolution['date'].max(),
                display_format='YYYY-MM'
            ),
            dcc.Graph(id='aba-evolution-graph')
        ])

@app.callback(
    Output('client-portfolio-graph', 'figure'),
    Input('client-dropdown', 'value')
)
def update_client_portfolio_graph(selected_client):
    filtered_df = df_client_portfolio[df_client_portfolio['id_sistema_cliente'] == selected_client]
    fig = px.pie(filtered_df, names='macroactivo', values='total_aba', title=f'Portafolio del Cliente {selected_client}')
    return fig

@app.callback(
    Output('aba-evolution-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_aba_evolution_graph(start_date, end_date):
    filtered_df = df_aba_evolution[(df_aba_evolution['date'] >= start_date) & (df_aba_evolution['date'] <= end_date)]
    fig = px.line(filtered_df, x='date', y='avg_aba', title='Evolución del ABA')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

