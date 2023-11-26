variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The Azure Region in which all resources in this example should be created."
  type        = string
}

variable "function_app_name" {
  description = "The name of the function app"
  type        = string
}

variable "service_app_principal_id" {
  description = "The ID of the service app principal"
  type        = string
  
}

variable "app_service_plan_name" {
  description = "The name of the app service plan"
  type        = string
}

variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
}

variable "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics Workspace"
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