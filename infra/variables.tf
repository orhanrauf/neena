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