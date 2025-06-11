# 🚀 Adventure Works - Data Extraction Pipeline

## 📋 Sobre o Projeto

Este projeto faz parte da trilha de desafios e checkpoints da Indicium (Lighthouse 2025-3) e tem como objetivo realizar todas as fases de um projeto de dados, sendo subdivida em entregas parciais, chckpoints, o primeiro foi sobre discovery e desenho da arquitetura de dados, a segunda etapa foca na extração e carregamento dos dados da empresa Adventure Works, que se encontram alocados em 2 fontes, uma API e um DW, usando notebooks no ambiente serverless do databricks foram extraidos os dados, como forma de dar escala e replicabilidade foi adicionada a camada de terraform e docker, preparando uma fundação robusta para as futuras fases do projeto.

**Autor:** Diego Santiago Vieira de Brito  
**Programa:** Jornada Técnica – Programa Lighthouse 2025-3  
**Checkpoint:** 2 - Ingestão de Dados

## 🎯 Objetivos

Construir um pipeline de ingestão de dados seguro, performático e escalável, utilizando:
- ✅ **Databricks + Delta Lake** para processamento e armazenamento
- ✅ **Extração de Banco de Dados Relacional** (Adventure Works DW)
- ✅ **Extração de API REST** com paginação, autenticação e controle de erros
- ✅ **Paralelização** para otimização de performance
- ✅ **Segurança** com Databricks Secrets

## 🏗️ Arquitetura

### Stack Tecnológica

| Componente | Tecnologia |
|------------|------------|
| **Ingestão** | Python + PySpark + Databricks |
| **Armazenamento** | Delta Lake |
| **Infraestrutura** | Docker + Terraform |
| **Versionamento** | Git + GitHub |
| **Segurança** | Databricks Secrets |
| **Orquestração** | Databricks Workflows |

### Camadas de Dados

```
Bronze (Raw) → Silver (Cleaned) → Gold (Business)
     ↑
   Este checkpoint
```

## 📁 Estrutura do Projeto

```
aw_extraction_check_point_2/
├── databricks/
│   ├── notebooks/
│   │   ├── dw_ingestion.py      # Extração do Data Warehouse
│   │   └── api_ingestion.py     # Extração da API REST
│   └── workflows/
│       └── extraction_job.json   # Configuração do workflow
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf              # Configuração principal
│   │   ├── variables.tf         # Variáveis
│   │   └── outputs.tf           # Outputs
│   ├── docker/
│   │   ├── Dockerfile           # Imagem para Terraform
│   │   └── docker-compose.yml   # Orquestração local
│   └── scripts/
│       └── deploy.sh            # Script de deployment
├── docs/
│   ├── slides/                  # Apresentações
│   └── architecture/            # Diagramas de arquitetura
├── tests/
│   └── integration/             # Testes de integração
├── .env.example                 # Exemplo de variáveis de ambiente
├── .gitignore
└── README.md

```

## 🔧 Configuração e Instalação

### Pré-requisitos

- Conta Databricks com acesso ao workspace
- Docker e Docker Compose instalados
- Terraform 1.5+
- Credenciais configuradas no Databricks Secrets

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```bash
# Databricks
DATABRICKS_HOST=https://your-workspace.databricks.com
DATABRICKS_TOKEN=your-token

# Database Adventure Works
DB_URL=jdbc:sqlserver://server:port;database=AdventureWorks
DB_USER=username
DB_PASSWORD=password

# API Adventure Works
API_URL=https://api.adventureworks.com/v1/
API_USER=api_username
API_PASSWORD=api_password

# Output Configuration
OUTPUT_PATH=ted_dev.dev_diego_brito
PATH_TABLE_OUTPUT=dbfs:/mnt/delta/
```

### Deploy com Terraform

```bash
# Inicializar e executar deploy
./deploy.sh
```

## 📊 Componentes do Pipeline

### 1. Extração do Data Warehouse (`dw_ingestion.py`)

**Características:**
- Extração paralela de todas as tabelas do banco
- Uso de ThreadPoolExecutor com 15 workers
- Salvamento em formato Delta Lake
- Tratamento de erros por tabela

**Tabelas extraídas:**
- Todas as tabelas do schema que não sejam `dbo`
- Nomenclatura: `raw_db_{schema}_{table}`

### 2. Extração da API (`api_ingestion.py`)

**Características:**
- Implementação robusta com retry logic
- Paginação automática (limit: 100k, max_offset: 200k)
- Paralelização com 8 workers
- Inferência dinâmica de schema
- Timeout configurável (45s)

**Endpoints:**
- `SalesOrderDetail`
- `SalesOrderHeader`
- `PurchaseOrderDetail`
- `PurchaseOrderHeader`

## 🔐 Segurança

### Databricks Secrets

Todos os segredos são gerenciados através do Databricks Secrets no scope `adventure-works-secrets`:

```python
# Exemplo de uso
password = dbutils.secrets.get(scope="adventure-works-secrets", key="sql-password")
```

### Secrets necessários:
- `sql-host`, `sql-port`, `sql-database`, `sql-username`, `sql-password`
- `api-url`, `api-username`, `api-password`

## 🚀 Execução

### Via Databricks Workflows

1. Importe os notebooks para seu workspace Databricks
2. Configure os secrets no Databricks
3. Execute o workflow `aw_extraction_check_point_2`


## 📈 Monitoramento e Performance

### Métricas de Performance

- **DW Extraction**: ~5 minutos para todas as tabelas
- **API Extraction**: ~1 minutos por endpoint
- **Paralelização**: Redução de 70% no tempo total

### Logs

Os notebooks geram logs detalhados incluindo:
- Tempo de execução por tabela/endpoint
- Quantidade de registros processados
- Erros e tentativas de retry

## 🧪 Testes

```bash
# Executar testes de integração
python -m pytest tests/integration/
```

## 📅 Cronograma

- ✅ **Desenvolvimento**: Concluído
- ✅ **Documentação**: 15/06/2025
- 📌 **Apresentação**: 30/06/2025



## 📧 Contato

Diego Santiago Vieira de Brito - diego.brito@indiciunm.tech - [GitHub](https://github.com/DiegoIndicium)

---

**Programa Lighthouse 2025-3** | **Indicium** | **Analytics Engineering**
