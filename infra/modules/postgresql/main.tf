resource "azurerm_postgresql_server" "psql_server" {
  name                = var.postgresql_server_name
  location            = var.location
  resource_group_name = var.resource_group_name

  sku_name = var.sku_name
  version  = var.postgres_version
  ssl_enforcement_enabled = var.ssl_enforcement_enabled
}

resource "azurerm_postgresql_database" "psql_db" {
  name                = var.database_name
  resource_group_name = azurerm_postgresql_server.psql_server.resource_group_name
  server_name         = azurerm_postgresql_server.psql_server.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}

resource "azurerm_role_assignment" "func_db_access" {
  scope                = azurerm_postgresql_server.psql_server.id
  role_definition_name = "Contributor"  # Use appropriate role
  principal_id         = var.function_app_principal_id
}

resource "azurerm_role_assignment" "service_app_db_access" {
  scope                = azurerm_postgresql_server.psql_server.id
  role_definition_name = "Contributor"  # Use appropriate role
  principal_id         = var.service_app_principal_id
}