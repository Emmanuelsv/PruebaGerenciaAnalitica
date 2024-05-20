from sqlalchemy import create_engine
import pandas as pd

# Configurar la conexión a la base de datos
DATABASE_URI = 'postgresql+psycopg2://gerentecomercial:gerentecomercial@localhost:5432/BaseDatosPruebaTalentoB'
engine = create_engine(DATABASE_URI)

df1 = pd.read_csv('historico_aba_macroactivos.csv')
df2 = pd.read_csv('cat_perfil_riesgo.csv')
df3 = pd.read_csv('catalogo_activos.csv')
df4 = pd.read_csv('catalogo_banca.csv')


df1.to_sql('historico_aba_macroactivos', engine, if_exists='replace', index=False)
df2.to_sql('cat_perfil_riesgo', engine, if_exists='replace', index=False)
df3.to_sql('catalogo_activos', engine, if_exists='replace', index=False)
df4.to_sql('catalogo_banca', engine, if_exists='replace', index=False)
