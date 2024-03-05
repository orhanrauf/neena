# Create an App Service Plan
resource "azurerm_app_service_plan" "app_service_plan" {
  name                = var.app_service_name
  location            = var.location
  resource_group_name = var.resource_group_name

  kind                = "Linux"
  reserved            = true

  sku {
    tier = var.app_service_plan_tier
    size = var.app_service_plan_size
  }
}

resource "azurerm_linux_web_app" "app_service" {
  name                = var.app_service_name
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id = azurerm_app_service_plan.app_service_plan.id


  site_config {
    app_command_line = "./startup.sh"
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    "PROJECT_NAME" = "Neena"
    "DTAP_ENVIRONMENT" = var.environment
    "FIRST_SUPERUSER" = var.first_superuser
    "FIRST_SUPERUSER_AUTH_ID" = var.first_superuser_auth_id
    "POSTGRES_SERVER" = var.postgresql_server_url
    "POSTGRES_DB" = var.postgresql_database_name
    "POSTGRES_USER" = "${var.postgresql_admin_username}@${var.postgresql_server_name}"
    "POSTGRES_PASSWORD" = var.postgresql_admin_password
    "AUTH0_DOMAIN" = var.auth0_domain
    "AUTH0_CLIENT_ID" = var.auth0_client_id
    "AUTH0_API_IDENTIFIER" = var.auth0_api_identifier
    "AUTH0_RULE_NAMESPACE" = var.auth0_rule_namespace
    "AZURE_CLIENT_ID" = var.service_principal_id
    "AZURE_CLIENT_SECRET" = var.service_principal_secret
    "AZURE_TENANT_ID" = var.tenant_id
    "AZURE_KEYVAULT_NAME" = var.key_vault_name
    "LOG_APPINSIGHTS": "true"
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = var.azurerm_application_insights_connection_string
    "TRELLO_API_KEY" = var.trello_api_key
    "OPENAI_API_KEY" = var.openai_api_key
    "PORT" = "8000"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "service_app_sami_role" {
  scope                = azurerm_linux_web_app.app_service.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_linux_web_app.app_service.identity[0].principal_id
}

resource "azurerm_role_assignment" "function_to_app_service" {
  scope                = azurerm_linux_web_app.app_service.id
  role_definition_name = "Contributor" # Or a more restrictive role as needed
  principal_id         = var.function_app_principal_id
}

# Configure App Service diagnostics to send to Log Analytics Workspace
resource "azurerm_monitor_diagnostic_setting" "app_service_diagnostic" {
  name                       = "${var.app_service_name}-diagnostics"
  target_resource_id         = azurerm_linux_web_app.app_service.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  enabled_log {
    category = "AppServiceHTTPLogs"
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
