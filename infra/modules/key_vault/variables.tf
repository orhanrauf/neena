variable "name" {
  description = "Specifies the name of the Key Vault."
  type        = string
}

variable "location" {
  description = "Specifies the supported Azure location where the resource exists."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group in which to create the Key Vault."
  type        = string
}

variable "tenant_id" {
  description = "The Azure Tenant ID."
  type        = string
}

variable "soft_delete_retention_days" {
  description = "The number of days that items should be retained for once soft-deleted."
  default     = 90
  type        = number
}

variable "sku_name" {
  description = "The Name of the SKU used for this Key Vault."
  default     = "standard"
  type        = string
}

variable "purge_protection_enabled" {
  description = "Is Purge Protection enabled for this Key Vault?"
  default     = false
  type        = bool
}


variable "function_app_principal_id" {
  description = "The principal ID of the function app."
  type        = string
}

variable "service_app_principal_id" {
  description = "The principal ID of the service app."
  type        = string
}