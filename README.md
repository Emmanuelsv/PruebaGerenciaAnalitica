# PruebaGerenciaAnalitica

Este repositorio contiene el código necesarios para analizar el portafolio de clientes utilizando Python y PostgreSQL. 

## Requisitos

1. **PostgreSQL**: Asegúrate de tener PostgreSQL instalado en tu máquina.
2. **Python 3.x**: Asegúrate de tener Python 3.x instalado en tu máquina.
3. **Librerías Python**: Todas las librerías necesarias están listadas en el archivo `requerimientos.txt`.

## Configuración de la Base de Datos

1. **Crear la Base de Datos**:
    ```sql
    CREATE DATABASE BaseDatosPruebaTalentoB;
    ```

2. **Crear el Usuario**:
    ```sql
    CREATE USER gerentecomercial WITH PASSWORD 'gerentecomercial';
    ALTER DATABASE BaseDatosPruebaTalentoB OWNER TO gerentecomercial;
    GRANT ALL PRIVILEGES ON DATABASE BaseDatosPruebaTalentoB TO gerentecomercial;
    ```

3. **Ejecutar el Script SQL**:
    - Abre la herramienta de consultas de PostgreSQL.
    - Ejecuta el archivo `Querie1.sql` que se encuentra en la carpeta `data`.

## Preparación del Entorno de Python

1. **Clonar el Repositorio**:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. **Instalar las Librerías Necesarias**:
    ```bash
    pip install -r requerimientos.txt
    ```

## Ejecución de los Scripts

1. **Migración de Datos**:
    ```bash
    python scripts/Migracion.py
    ```

2. **Ejecución de Queries**:
    ```bash
    python scripts/Queries.py
    ```

3. **Visualización de Datos**:
    ```bash
    python scripts/VisualizacionDatos.py
    ```

## Estructura del Repositorio

- **data**: Contiene los archivos CSV y el script SQL.
  - `cat_perfil_riesgo.csv`: Datos del catálogo de perfil de riesgo.
  - `catalogo_activos.csv`: Datos del catálogo de activos.
  - `catalogo_banca.csv`: Datos del catálogo de banca.
  - `historico_aba_macroactivos.csv`: Datos históricos de ABA y macroactivos.
  - `Querie1.sql`: Script SQL para inicializar la base de datos.

- **scripts**: Contiene los scripts de Python.
  - `Migracion.py`: Script para migrar datos desde archivos CSV a la base de datos.
  - `Queries.py`: Script para ejecutar las consultas SQL y procesar los datos.
  - `VisualizacionDatos.py`: Script para visualizar los datos utilizando Dash.

- **requerimientos.txt**: Archivo de requisitos para instalar las librerías de Python necesarias.

## Notas

- Asegúrate de que el usuario `gerentecomercial` tenga todos los permisos necesarios en PostgreSQL.
- Asegúrate de que los archivos CSV en la carpeta `data` estén correctamente formateados y disponibles antes de ejecutar los scripts de Python.

