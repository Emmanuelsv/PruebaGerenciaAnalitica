import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Configurar la conexión a la base de datos
DATABASE_URI = 'postgresql+psycopg2://gerentecomercial:gerentecomercial@localhost:5432/BaseDatosPruebaTalentoB'
engine = create_engine(DATABASE_URI)

conn = psycopg2.connect(
    dbname="BaseDatosPruebaTalentoB",
    user="gerentecomercial",
    password="gerentecomercial",
    host="localhost"
)

cur = conn.cursor()

# Queries
create_temp_table_query = """
CREATE TEMP TABLE historico_aba_macroactivos_temp AS
SELECT 
    ingestion_year::TEXT,
    ingestion_month::TEXT,
    ingestion_day::TEXT,
    id_sistema_cliente::TEXT,
    macroactivo::TEXT,
    cod_activo::TEXT,
    aba::TEXT,
    cod_perfil_riesgo::TEXT,
    cod_banca::TEXT,
    year::TEXT,
    month::TEXT
FROM 
    historico_aba_macroactivos;
"""

# Crear tabla limpia si no existe
create_clean_table_query = """
CREATE TABLE IF NOT EXISTS historico_aba_macroactivos_clean (
    ingestion_year INTEGER,
    ingestion_month INTEGER,
    ingestion_day INTEGER,
    id_sistema_cliente TEXT,
    macroactivo TEXT,
    cod_activo TEXT,
    aba NUMERIC,
    cod_perfil_riesgo TEXT,
    cod_banca TEXT,
    year INTEGER,
    month INTEGER
);
"""

insert_clean_data_query = """
INSERT INTO historico_aba_macroactivos_clean (
    ingestion_year, ingestion_month, ingestion_day, id_sistema_cliente, macroactivo, cod_activo, aba, cod_perfil_riesgo, cod_banca, year, month
)
SELECT 
    CAST(ingestion_year AS INTEGER),
    CAST(ingestion_month AS INTEGER),
    CAST(ingestion_day AS INTEGER),
    id_sistema_cliente,
    macroactivo,
    cod_activo,
    CAST(aba AS NUMERIC),
    cod_perfil_riesgo,
    cod_banca,
    CAST(year AS INTEGER),
    CAST(month AS INTEGER)
FROM 
    historico_aba_macroactivos_temp
WHERE
    ingestion_year ~ '^[0-9]+$' AND
    ingestion_month ~ '^[0-9]+$' AND
    ingestion_day ~ '^[0-9]+$' AND
    year ~ '^[0-9]+$' AND
    month ~ '^[0-9]+$' AND
    cod_banca IS NOT NULL AND
    id_sistema_cliente IS NOT NULL AND
    macroactivo IS NOT NULL AND
    cod_activo IS NOT NULL AND
    ingestion_month BETWEEN '1' AND '12' AND
    ingestion_day BETWEEN '1' AND '31';
"""

eliminar_duplicados_query = """
DELETE FROM historico_aba_macroactivos_clean a
USING (
    SELECT 
        MIN(ctid) as ctid, 
        ingestion_year, ingestion_month, ingestion_day, id_sistema_cliente, macroactivo, cod_activo, aba, cod_perfil_riesgo, cod_banca, year, month
    FROM 
        historico_aba_macroactivos_clean
    GROUP BY 
        ingestion_year, ingestion_month, ingestion_day, id_sistema_cliente, macroactivo, cod_activo, aba, cod_perfil_riesgo, cod_banca, year, month
    HAVING COUNT(*) > 1
) b
WHERE 
    a.ingestion_year = b.ingestion_year AND
    a.ingestion_month = b.ingestion_month AND
    a.ingestion_day = b.ingestion_day AND
    a.id_sistema_cliente = b.id_sistema_cliente AND
    a.macroactivo = b.macroactivo AND
    a.cod_activo = b.cod_activo AND
    a.aba = b.aba AND
    a.cod_perfil_riesgo = b.cod_perfil_riesgo AND
    a.cod_banca = b.cod_banca AND
    a.year = b.year AND
    a.month = b.month AND
    a.ctid <> b.ctid;
"""

indexar_tabla_query = """
CREATE INDEX IF NOT EXISTS idx_year ON historico_aba_macroactivos_clean (year);
CREATE INDEX IF NOT EXISTS idx_macroactivo ON historico_aba_macroactivos_clean (macroactivo);
CREATE INDEX IF NOT EXISTS idx_cod_banca ON historico_aba_macroactivos_clean (cod_banca);
"""

# Ejecutar los queries
cur.execute(create_temp_table_query)
cur.execute(create_clean_table_query)
cur.execute(insert_clean_data_query)
cur.execute(eliminar_duplicados_query)
cur.execute(indexar_tabla_query)

# Confirmar la transacción
conn.commit()

# Cerrar el cursor y la conexión
cur.close()
conn.close()
