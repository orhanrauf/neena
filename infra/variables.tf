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

variable "first_superuser_auth_id" {
  description = "The ID of the first superuser authentication"
  type        = string
}

variable "auth0_domain" {
  description = "The domain of the Auth0 service"
  type        = string
}

variable "auth0_api_identifier" {
  description = "The identifier of the Auth0 API"
  type        = string  
}

variable "auth0_client_id" {
  description = "The client ID of the Auth0 service"
  type        = string
}

variable "auth0_rule_namespace" {
  description = "The namespace for Auth0 rules"
  type        = string
}

variable "trello_api_key" {
  description = "The API key for Neena's Trello integration"
  type        = string
}

variable "openai_api_key" {
  description = "The API key for OpenAI"
  type        = string
}

variable "domain_name" {
  description = "The custom domain name"
  type        = string
}