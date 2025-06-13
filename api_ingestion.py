# Databricks notebook source
# ====================================================================
# 1. IMPORTAÇÕES E CONFIGURAÇÃO
# ====================================================================
import requests
import logging
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType
from pyspark.sql.functions import schema_of_json, lit # Importações sugeridas
from typing import Dict, List, Any, Optional

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicialização da Sessão Spark
spark = SparkSession.builder.appName("API_Extraction_Robust").getOrCreate()

# ====================================================================
# 2. PARÂMETROS E SECRETS
# ====================================================================
config = {
    "base_url": dbutils.secrets.get("adventure-works-secrets", "api-url"),
    "auth": (
        dbutils.secrets.get("adventure-works-secrets", "api-username"),
        dbutils.secrets.get("adventure-works-secrets", "api-password")
    ),
    "limit": 100000,
    "max_offset": 200000,
    "max_retries": 3,
    "max_workers": 8,
    # ALTERADO: Aumentado o timeout para dar mais tempo para a API responder
    "timeout": 45, 
    "endpoints": [
        'SalesOrderDetail',
        'SalesOrderHeader',
        'PurchaseOrderDetail',
        'PurchaseOrderHeader'
    ]
}

# ====================================================================
# 3. FUNÇÕES DE EXTRAÇÃO, INFERÊNCIA E PROCESSAMENTO
# ====================================================================

def fetch_pagina(endpoint: str, offset: int, limit: int) -> Dict[str, Any]:
    """Busca uma única página de dados da API com lógica de retentativas."""
    url = f"{config['base_url']}{endpoint}"
    params = {'offset': offset, 'limit': limit}
    
    for attempt in range(1, config['max_retries'] + 1):
        try:
            response = requests.get(url, params=params, auth=config['auth'], timeout=config['timeout'])
            response.raise_for_status()
            return {"data": response.json(), "success": True}
        except requests.RequestException as e:
            logger.warning(f"[{endpoint}] Erro no offset {offset}: {e}. Tentando novamente...")
            if attempt < config['max_retries']:
                time.sleep(2 ** attempt)
        except json.JSONDecodeError as e:
            logger.error(f"[{endpoint}] Erro de JSON no offset {offset}: {e}")
            return {"data": [], "success": False}
            
    logger.error(f"[{endpoint}] Falha final no offset {offset} após {config['max_retries']} tentativas.")
    return {"data": [], "success": False}

# Expondo os tipos de dados: Função para inferir o schema dinamicamente usando 5 registros
def inferir_schema_da_api(endpoint: str) -> Optional[StructType]:
    """
    Busca uma pequena amostra de dados da API para inferir o schema do DataFrame.
    """
    logger.info(f"[{endpoint}] Tentando inferir schema a partir de uma amostra de 5 registros...")
    try:
        # Pega uma amostra pequena (5 registros) para inferir o schema
        amostra_result = fetch_pagina(endpoint, offset=0, limit=5)
        
        if not amostra_result["success"] or not amostra_result["data"]:
            logger.error(f"[{endpoint}] Não foi possível obter uma amostra para inferir o schema.")
            return None
        
        # Converte a amostra para uma string JSON
        json_amostra_str = json.dumps(amostra_result["data"])
        
        # Usa a função do Spark para extrair o schema do JSON
        df_schema = spark.range(1).select(schema_of_json(lit(json_amostra_str))).first()[0]
        
        logger.info(f"[{endpoint}] Schema inferido com sucesso!")
        return df_schema
        
    except Exception as e:
        logger.exception(f"[{endpoint}] Falha crítica ao inferir o schema: {e}")
        return None

def limpar_e_padronizar_dados(registros: List[Dict]) -> List[Row]:
    """Limpa os dados brutos e os converte para o formato Row."""
    dados_limpos = []
    for record in registros:
        if isinstance(record, dict):
            dados_limpos.append(Row(**record))
    return dados_limpos

def processar_e_salvar_endpoint(endpoint: str) -> bool:
    """Orquestra a extração, limpeza e salvamento de um único endpoint."""
    try:
        logger.info(f"[{endpoint}] Iniciando processamento...")
        start_time = time.time()
        
        # ALTERADO: Passo 1 - Inferir o schema ANTES de buscar todos os dados
        schema_inferido = inferir_schema_da_api(endpoint)
        if schema_inferido is None:
            # Se não conseguir inferir o schema, não adianta continuar
            return False
            
        # Passo 2 - Buscar todos os dados em paralelo
        offsets = list(range(0, config['max_offset'], config['limit']))
        all_data_raw = []
        with ThreadPoolExecutor(max_workers=config['max_workers']) as executor:
            futures = [executor.submit(fetch_pagina, endpoint, offset, config['limit']) for offset in offsets]
            for future in as_completed(futures):
                result = future.result()
                if result.get("success") and result.get("data"):
                    all_data_raw.extend(result["data"])
        
        if not all_data_raw:
            logger.warning(f"[{endpoint}] Nenhum dado foi coletado.")
            return False

        # Passo 3 - Limpar e padronizar
        dados_em_rows = limpar_e_padronizar_dados(all_data_raw)
        
        # ALTERADO: Passo 4 - Criar DataFrame usando o schema pré-definido
        logger.info(f"[{endpoint}] Criando DataFrame com {len(dados_em_rows)} registros e schema explícito...")
        # A mágica acontece aqui: ao fornecer o schema, evitamos o erro de inferência
        df = spark.createDataFrame(dados_em_rows, schema=schema_inferido)
        
        # Passo 5 - Salvar tabela
        table_name = f"ted_dev.dev_diego_brito.raw_API_{endpoint}"
        df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(table_name)

        logger.info(f"[{endpoint}] SUCESSO! Salvos {df.count()} registros.")
        return True

    except Exception as e:
        logger.exception(f"[{endpoint}] FALHA GERAL NO PROCESSAMENTO: {e}")
        return False

# ====================================================================
# 4. EXECUÇÃO PRINCIPAL - Extração de a partir dos endepoisnts da API
# ====================================================================
logger.info("=" * 50)
logger.info("INICIANDO PROCESSO DE EXTRAÇÃO DE APIs")
resultados_finais = {}

for endpoint in config["endpoints"]:
    logger.info("Executando comando 'keep-alive' para manter a sessão Spark ativa...")
    spark.sql("SELECT 1").count()
    success = processar_e_salvar_endpoint(endpoint)
    resultados_finais[endpoint] = success
    logger.info("-" * 50)

logger.info("=" * 50)
logger.info("RESUMO FINAL DA EXTRAÇÃO")
falhas = []
for endpoint, success in resultados_finais.items():
    status = " Sucesso" if success else "Falha"
    logger.info(f"- {endpoint}: {status}")
    if not success:
        falhas.append(endpoint)
