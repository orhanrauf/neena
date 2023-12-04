resource "azurerm_app_service_plan" "funcapp_plan" {
  name                = var.function_app_name
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "FunctionApp"

  sku {
    tier = var.function_app_plan_tier
    size = var.function_app_plan_size
  }
}

resource "azurerm_storage_account" "funcapp_storage" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_function_app" "funcapp" {
  name                      = var.function_app_name
  location                  = var.location
  resource_group_name       = var.resource_group_name
  app_service_plan_id       = azurerm_app_service_plan.funcapp_plan.id
  storage_account_name      = var.storage_account_name
  storage_account_access_key = azurerm_storage_account.funcapp_storage.primary_access_key
  os_type                   = "linux"
  version                   = "~3"

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "func_sami_role" {
  scope                = azurerm_function_app.funcapp.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_function_app.funcapp.identity[0].principal_id
}

resource "azurerm_role_assignment" "funcapp" {
  scope                = azurerm_function_app.funcapp.id
  role_definition_name = "Contributor" # Or a more restrictive role as needed
  principal_id         = var.service_app_principal_id
}

resource "azurerm_role_assignment" "storage_access" {
  scope                = azurerm_storage_account.funcapp_storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_function_app.funcapp.identity.0.principal_id
}

resource "azurerm_monitor_diagnostic_setting" "law" {
  name                       = "${var.function_app_name}-diagnostics"
  target_resource_id         = azurerm_function_app.funcapp.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  enabled_log {
    category = "FunctionAppLogs"
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}



