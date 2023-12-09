variable "postgresql_server_name" {
  description = "Name of the PostgreSQL server"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "sku_name" {
  description = "SKU name"
  type        = string
  
}

variable "postgres_version" {
  description = "Version of PostgreSQL"
  type        = string
}

variable "database_name" {
  description = "Name of the database"
  type        = string
}

variable "ssl_enforcement_enabled" {
  description = "Enable SSL enforcement"
  type        = bool  
}

variable "service_app_principal_id" {
  description = "The principal ID of the service app"
  type        = string
}

variable "function_app_principal_id" {
  description = "The principal ID of the function app"
  type        = string
}

variable "psql_admin_username" {
  description = "PostgreSQL Admin Username"
  type        = string
}

variable "psql_admin_password" {
  description = "PostgreSQL Admin Password"
  type        = string
}

variable "service_app_outbound_ip_addresses" {
  description = "Outbound IP addresses of the service app"
  type        = list(string)
}