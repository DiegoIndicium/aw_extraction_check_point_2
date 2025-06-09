# 🚀 Projeto Adventure Works - Checkpoint 2 (Lighthouse Indicium)

**Autor:** Diego Santiago Vieira de Brito  
**Repositório:** [github.com/DiegoIndicium/aw_extraction_check_point_2](https://github.com/DiegoIndicium/aw_extraction_check_point_2)  
**Trilha:** Jornada Técnica – Programa Lighthouse 2025-3  

---

## 🧭 Visão Geral

Este repositório contém o código desenvolvido para o **Checkpoint 2** da Jornada Técnica do Programa Lighthouse. 
O objetivo é construir um pipeline de ingestão de dados seguro, performático e escalável, utilizando **Databricks + Delta Lake**, extraindo informações de:

- ✅ **Banco de Dados Relacional (DW)**
- ✅ **API REST com paginação, autenticação e controle de erros**

Todos os dados extraídos são carregados diretamente na **camada Bronze (raw)** do Data Lakehouse, sem transformação ou tratamento adicional nesta fase.

---

## 📐 Arquitetura da Solução

A arquitetura adotada para este checkpoint foi otimizada para ingestão inicial de dados, com foco em performance, paralelismo e boas práticas.


> 🔁 A extração da API foi implementada com `ThreadPoolExecutor` para permitir chamadas paralelas por endpoint.

---

## 🧰 Tecnologias Utilizadas

| Finalidade           | Ferramenta                           |
|----------------------|--------------------------------------|
| Ingestão             | Python + PySpark + Databricks        |
| Armazenamento        | Delta Lake                           |
| Infraestrutura (WIP) | Docker + Terraform                   |
| Versionamento        | Git + GitHub                         |
| Segurança            | Databricks Secrets                   |
| Orquestração         | Databricks Workflows                 |



📌 Referência: Checkpoint 1
A arquitetura desenhada no Checkpoint 1 previa a construção de uma base sólida com:

Modelo em camadas

Indicium Mesh no Databricks

Planejamento de migração para DBT nas camadas superiores

Foco em escalabilidade, governança e cultura analítica

Neste checkpoint, concentramos esforços na camada Bronze (raw).

📅 Entregas
✅ Código e notebooks organizados no GitHub

✅ README.md com instruções claras

✅ Slides de apresentação e cronograma

🕒 Entrega final: 15/06/2025

📢 Apresentação agendada: 30/06/2025


