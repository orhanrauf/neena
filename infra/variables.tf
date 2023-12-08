variable "organization" {
  description = "The organization name"
  type        = string
}

variable "environment" {
  description = "The deployment environment (dev, test, acc, prod)"
  type        = string
}

variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "tenant_id" {
  description = "The Azure Tenant ID"
  type        = string
}

variable "location" {
  description = "The Azure location where resources will be created"
  type        = string
}

variable "app_service_plan_tier" {
  description = "The pricing tier for the app service plan"
  type        = string
}

variable "app_service_plan_size" {
  description = "The instance size for the app service plan"
  type        = string
}

variable "function_app_plan_tier" {
  description = "The pricing tier for the function app plan"
  type        = string
}
variable "function_app_plan_size" {
  description = "The instance size for the function app plan"
  type        = string
}

variable "kv_sku_name" {
  description = "The Name of the SKU used for this Key Vault"
  default     = "standard"
  type        = string 
}

variable "postgresql_version" {
  description = "The version of PostgreSQL to use"
  default     = "11"
  type        = string
}

variable "postgresql_sku_name" {
  description = "The Name of the SKU used for this PostgreSQL server"
  default     = "B_Gen5_1"
  type        = string
}

variable "postgresql_ssl_enforcement_enabled" {
  description = "Enable SSL enforcement"
  default     = true
  type        = bool
  
}

variable "psql_admin_username" {
  description = "PostgreSQL Admin Username"
  type        = string
}

variable "psql_admin_password" {
  description = "PostgreSQL Admin Password"
  type        = string
}

variable "first_superuser" {
  description = "First Superuser"
  type        = string
}

variable "first_superuser_password" {
  description = "First Superuser Password"
  type        = string
}