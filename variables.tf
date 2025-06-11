variable "databricks_host" {
  description = "Databricks workspace url"
  type        = string
}

variable "databricks_token" {
  description = "Databricks access token"
  type        = string
  sensitive   = true
}

variable "output_path" {
  description = "Output path for the notebook in Databricks"
  type        = string
}

variable "api_url" {
  description = "API URL"
  type        = string
}

variable "api_user" {
  description = "API username"
  type        = string
  sensitive   = true
}

variable "api_password" {
  description = "API password"
  type        = string
  sensitive   = true
}

variable "db_url" {
  description = "database URL"
  type        = string
  sensitive   = true
}

variable "db_user" {
  description = "database username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "database password"
  type        = string
  sensitive   = true
}

variable "path_table_output" {
  description = "Output location for delta tables in Databricks"
  type        = string
  sensitive   = true
}