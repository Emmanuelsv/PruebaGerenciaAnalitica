-- Crear tabla para cat_perfil_riesgo
CREATE TABLE cat_perfil_riesgo (
    cod_perfil_riesgo VARCHAR PRIMARY KEY,
    perfil_riesgo VARCHAR
);

-- Crear tabla para catalogo_activos
CREATE TABLE catalogo_activos (
    activo VARCHAR,
    cod_activo VARCHAR PRIMARY KEY
);

-- Crear tabla para catalogo_banca
CREATE TABLE catalogo_banca (
    cod_banca VARCHAR PRIMARY KEY,
    banca VARCHAR
);

-- Crear tabla para historico_aba_macroactivos
CREATE TABLE historico_aba_macroactivos (
    ingestion_year INTEGER,
    ingestion_month INTEGER,
    ingestion_day INTEGER,
    id_sistema_cliente VARCHAR,
    macroactivo VARCHAR,
    cod_activo VARCHAR,
    aba NUMERIC,
    cod_perfil_riesgo VARCHAR,
    cod_banca VARCHAR,
    year INTEGER,
    month INTEGER
);
