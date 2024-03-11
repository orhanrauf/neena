variable "static_website_name" {
  description = "The name of the static website"
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The Azure location where resources will be created"
  type        = string
}

variable "domain_name" {
  description = "The domain name for the static website"
  type        = string
  default     = "example.com"
}

variable "domain_name_without_www" {
  description = "The domain name without the www prefix"
  type        = string
  default     = replace(var.domain_name, "^www\\.", "")
}

