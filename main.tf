terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
    }
  }
}

provider "databricks" {
  host     = var.databricks_host
  token    = var.databricks_token
}

resource "databricks_notebook" "api_ingestion" {
  path     = "${var.output_path}/api_ingestion"
  language = "PYTHON"
  content_base64 = base64encode(file("${path.module}/notebooks/api_ingestion.py"))
}

resource "databricks_notebook" "db_ingestion" {
  path     = "${var.output_path}/db_ingestion"
  language = "PYTHON"
  content_base64 = base64encode(file("${path.module}/notebooks/db_ingestion.py"))
}

resource "databricks_secret" "path_table_output" {
  key          = "PATH_TABLE_OUTPUT"
  string_value = var.path_table_output
  scope        = "app-credentials"
}

resource "databricks_secret" "db_url" {
  key          = "DB_URL"
  string_value = var.db_url
  scope        = "app-credentials"
}

resource "databricks_secret" "db_user" {
  key          = "DB_USER"
  string_value = var.db_user
  scope        = "app-credentials"
}

resource "databricks_secret" "db_password" {
  key          = "DB_PASSWORD"
  string_value = var.db_password
  scope        = "app-credentials"
}

resource "databricks_secret" "api_url" {
  key          = "API_URL"
  string_value = var.api_url
  scope        = "app-credentials"
}

resource "databricks_secret" "api_user" {
  key          = "API_USER"
  string_value = var.api_user
  scope        = "app-credentials"
}

resource "databricks_secret" "api_password" {
  key          = "API_PASSWORD"
  string_value = var.api_password
  scope        = "app-credentials"
}