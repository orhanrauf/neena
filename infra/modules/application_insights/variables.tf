variable "name" {
  description = "The name of the Application Insights component."
  type        = string
}

variable "location" {
  description = "The Azure region where the Application Insights will be created."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group in which to create the Application Insights."
  type        = string
}

variable "application_type" {
  description = "Type of application being monitored."
  default     = "web"
  type        = string
}