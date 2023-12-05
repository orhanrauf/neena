# terraform.tfvars for Development Environment

organization              = "neena"
environment               = "prd"
project_name              = "core"
tenant_id                 = "3468fb09-8781-4717-9e95-d5e3f4c8bc44" # Replace with actual Tenant ID
location                  = "West Europe"
app_service_plan_tier     = "Standard"
app_service_plan_size     = "S1"
function_app_plan_tier    = "Standard"
function_app_plan_size    = "S1"
kv_sku_name               = "standard"

backend_resource_group_name = "neena-core-tf-state-rg"
backend_storage_account_name = "neenacoretfstatest"
backend_container_name = "tfstate"
backend_key = "core-prd.terraform.tfstate"