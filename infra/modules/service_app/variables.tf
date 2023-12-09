variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The Azure Region in which all resources in this example should be created."
  type        = string
}

variable "function_app_principal_id" {
  description = "The ID of the service app principal"
  type        = string
  
}

variable "app_service_name" {
  description = "The name of the app service"
  type        = string
}

variable "azurerm_application_insights_instrumentation_key" {
  description = "The instrumentation key for the application insights instance"
  type        = string
  
}

variable "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics Workspace"
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

variable "environment" {
  description = "The environment for the app service"
  type        = string
}

variable "postgresql_server_url" {
  description = "The url of the postgresql server"
  type        = string  
}

variable "postgresql_server_name" {
  description = "The name of the postgresql server"
  type        = string
}

variable "postgresql_database_name" {
  description = "The name of the postgresql database"
  type        = string  
}

variable "postgresql_admin_username" {
  description = "The admin username for the postgresql server"
  type        = string  
}

variable "postgresql_admin_password" {
  description = "The admin password for the postgresql server"
  type        = string  
}

variable "first_superuser" {
  description = "The first superuser."
  type        = string  
}

variable "first_superuser_password" {
  description = "The first superuser password."
  type        = string  
}