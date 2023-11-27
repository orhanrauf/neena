variable "name" {
  description = "Specifies the name of the Log Analytics Workspace."
  type        = string
}

variable "location" {
  description = "Specifies the supported Azure location where the resource exists."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group in which to create the Log Analytics Workspace."
  type        = string
}

variable "sku" {
  description = "Specifies the SKU of the Log Analytics Workspace."
  default     = "PerGB2018"
  type        = string
}

variable "retention_in_days" {
  description = "The workspace data retention in days. -1 means Unlimited retention."
  default     = 30
  type        = number
}
