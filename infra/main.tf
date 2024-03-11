provider "azurerm" {
  features {}
}

provider "azuread" {}


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
      version = ">= 3.75" # Specify an appropriate version
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = ">= 2.0"
    }
  }
}

locals {
  resource_prefix = "${var.organization}-${var.project_name}-${var.environment}"
  resource_prefix_no_hyphens = "${replace(local.resource_prefix, "-", "")}"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-rg"
  location = var.location
}

module "service_principal" {
  source            = "./modules/service_principal"
  application_name  = "${local.resource_prefix}-sp"
}

module "function_app" {
  source = "./modules/function_app"
  resource_group_name         = azurerm_resource_group.rg.name
  location                    = var.location
  function_app_name           = "${local.resource_prefix}-func"
  storage_account_name        = "${local.resource_prefix_no_hyphens}funcst"
  log_analytics_workspace_id  = module.log_analytics_workspace.log_analytics_workspace_id
  function_app_plan_tier      = var.function_app_plan_tier
  function_app_plan_size      = var.function_app_plan_size 
  service_app_principal_id    = module.service_app.service_app_principal_id
  azurerm_application_insights_connection_string = module.application_insights.app_insights_connection_string
  environment                 = var.environment
}

module "service_app" {
  source = "./modules/service_app"
  resource_group_name         = azurerm_resource_group.rg.name
  location                    = var.location
  function_app_principal_id   = module.function_app.principal_id
  app_service_name            = "${local.resource_prefix}-svc"
  log_analytics_workspace_id  = module.log_analytics_workspace.log_analytics_workspace_id
  app_service_plan_tier       = var.app_service_plan_tier
  app_service_plan_size       = var.app_service_plan_size 
  azurerm_application_insights_connection_string = module.application_insights.app_insights_connection_string
  environment                 = var.environment
  postgresql_server_url       = module.postgresql.postgresql_server_fqdn
  postgresql_database_name    = module.postgresql.database_name
  postgresql_admin_username   = var.psql_admin_username
  postgresql_admin_password   = var.psql_admin_password
  first_superuser             = var.first_superuser
  first_superuser_auth_id     = var.first_superuser_auth_id
  postgresql_server_name      = module.postgresql.postgresql_server_name
  auth0_domain                = var.auth0_domain
  auth0_client_id             = var.auth0_client_id
  auth0_api_identifier        = var.auth0_api_identifier
  auth0_rule_namespace        = var.auth0_rule_namespace
  service_principal_id        = module.service_principal.application_id
  service_principal_secret    = module.service_principal.service_principal_secret
  tenant_id                   = var.tenant_id
  key_vault_name              = module.key_vault.name
  trello_api_key              = var.trello_api_key
  openai_api_key              = var.openai_api_key
  pinecone_api_key            = var.pinecone_api_key
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
  service_principal_id        = module.service_principal.service_principal_id
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
  service_app_outbound_ip_addresses = module.service_app.outbound_ip_addresses
}

module "static_website" {
  source                  = "./modules/static_website"
  resource_group_name     = azurerm_resource_group.rg.name
  location                = var.location
  static_website_name     = "${local.resource_prefix}-webst"
  domain_name             = var.domain_name
}