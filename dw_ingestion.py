# Databricks notebook source
# Importando as bibliotecas
import time
from concurrent.futures import ThreadPoolExecutor
#Configurando o acesso ao SQL Warehouse - Usando Databricks Secrests
def get_secret(key):
    return dbutils.secrets.get(scope="adventure-works-secrets", key=key)

path_output = "ted_dev.dev_diego_brito"
jdbcUrl = f"jdbc:sqlserver://{get_secret('sql-host')}:{get_secret('sql-port')};database={get_secret('sql-database')};encrypt=false"
connectionProperties = {
     "user": get_secret("sql-username"),
    "password": get_secret("sql-password"),
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}
# Funções para extração e salvamento dos dados
def get_all_db_tables():
    """Usa o Get para adquirir todas as tables do DW database"""
    query = """SELECT
        TABLE_NAME, 
        TABLE_SCHEMA 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA != 'dbo'"""
    df = spark.read.jdbc(url=jdbcUrl, table=f"({query}) as tables", properties=connectionProperties)
    
    return df
# Funções para extração e salvamento dos dados de uma table específica
def extract_table(schema, table):
    
    try:
        df = spark.read.jdbc(url=jdbcUrl, table=f"{schema}.{table}", properties=connectionProperties)
        return df
    
    except Exception as e:
        print(f"Error ao extrair {schema}.{table}: {e}")
        return None

def save_table(df, schema, table):
    """Salva a table no databricks como delta lake"""
    try:
        df.write.format("delta").mode("overwrite").saveAsTable(f'{path_output}.raw_db_{schema}_{table}')
    except Exception as e:
        print(f"Error to save {schema}.{table}: {e}")
        return None
    
def process_single_table(schema, table):
    """Processa a table paralelamente"""
    try:
        df = extract_table(schema, table)

        if df is None:
            return f"No data for {schema}.{table}"
    
        save_table(df, schema, table)
        return f'Extraction complete for {schema}.{table}'
    
    except Exception as e:
        return f"Error {schema}.{table}: {e}"

def el_tables_db():
    """Função principal para executar todo o pipeline"""
    time_start = time.time()
    tables_df = get_all_db_tables()
    total_tables = tables_df.count()

    print(f'Total tables: {total_tables}')

    with ThreadPoolExecutor(max_workers=15) as executor: 
        futures = [
            executor.submit(process_single_table, row.TABLE_SCHEMA, row.TABLE_NAME)
            for row in tables_df.collect()
        ]
        for future in futures:
            result = future.result()
            print(result)
    
    time_end = time.time()
    print('Migracao completa para delta lake')
    print(f"Total time: {time_end - time_start}")

el_tables_db()
