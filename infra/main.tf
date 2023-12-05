provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name   = "neena-core-tf-state-rg"
    storage_account_name  = "neenacoretfstatest"
    container_name        = "tfstate"
    key                   = "terraform.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.40" # Specify an appropriate version
    }
  }
}


locals {
  resource_prefix = "${var.organization}-${var.project_name}-${var.environment}"
  resource_prefiex_no_hyphens = "${replace(local.resource_prefix, "-", "")}"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-rg"
  location = var.location
}

module "function_app" {
  source = "./modules/function_app"
  resource_group_name         = azurerm_resource_group.rg.name
  location                    = var.location
  function_app_name           = "${local.resource_prefix}-func"
  storage_account_name        = "${local.resource_prefiex_no_hyphens}funcst"
  app_service_plan_name       = "${local.resource_prefix}-func-asp"
  log_analytics_workspace_id  = module.log_analytics_workspace.log_analytics_workspace_id
  function_app_plan_tier      = var.function_app_plan_tier
  function_app_plan_size      = var.function_app_plan_size 
  service_app_principal_id    = module.service_app.service_app_principal_id
}

module "service_app" {
  source = "./modules/service_app"
  resource_group_name         = azurerm_resource_group.rg.name
  location                    = var.location
  function_app_principal_id   = module.function_app.principal_id
  app_service_name            = "${local.resource_prefix}-svc"
  app_service_plan_name       = "${local.resource_prefix}-svc-asp"
  log_analytics_workspace_id  = module.log_analytics_workspace.log_analytics_workspace_id
  app_service_plan_tier       = var.app_service_plan_tier
  app_service_plan_size       = var.app_service_plan_size 
}

module "log_analytics_workspace" {
  source              = "./modules/log_analytics_workspace"
  name                = "${local.resource_prefix}-log"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  retention_in_days   = 30
}

module "key_vault" {
  source                      = "./modules/key_vault"
  name                        = "${local.resource_prefix}-kv"
  location                    = var.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = var.tenant_id
  sku_name                    = var.kv_sku_name
  function_app_principal_id   = module.function_app.principal_id
  service_app_principal_id    = module.service_app.service_app_principal_id
}

module "application_insights" {
  source              = "./modules/application_insights"
  name                = "${local.resource_prefix}-ai"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
}

module "postgresql" {
  source                  = "./modules/postgresql"
  resource_group_name     = azurerm_resource_group.rg.name
  location                = var.location
  postgresql_server_name  = "${local.resource_prefix}-psql"
  database_name           = "${local.resource_prefix}-db"
  sku_name                = var.postgresql_sku_name
  postgres_version        = var.postgresql_version
  ssl_enforcement_enabled = var.postgresql_ssl_enforcement_enabled
  service_app_principal_id = module.service_app.service_app_principal_id
  function_app_principal_id = module.function_app.principal_id
  psql_admin_username     = var.psql_admin_username
  psql_admin_password     = var.psql_admin_password
}

module "static_website" {
  source                  = "./modules/static_website"
  resource_group_name     = azurerm_resource_group.rg.name
  location                = var.location
  storage_account_name    = "${local.resource_prefiex_no_hyphens}webst"
}
