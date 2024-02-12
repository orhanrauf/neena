resource "azurerm_key_vault" "kv" {
  name                        = var.name
  location                    = var.location
  resource_group_name         = var.resource_group_name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  sku_name                    = var.sku_name

  soft_delete_retention_days = var.soft_delete_retention_days
  purge_protection_enabled   = var.purge_protection_enabled

  network_acls {
    default_action             = "Allow" # For now while dynamic whitelisting of GitHub workers is out of scope.
    bypass                     = "AzureServices"
  }
}

resource "azurerm_key_vault_access_policy" "svc_policy" {
  key_vault_id = azurerm_key_vault.kv.id

  tenant_id = var.tenant_id
  object_id = var.service_app_principal_id

  secret_permissions = [
    "Get",
    "Set",
    "List",
    "Delete"
  ]
}

resource "azurerm_key_vault_access_policy" "func_policy" {
  key_vault_id = azurerm_key_vault.kv.id

  tenant_id = var.tenant_id
  object_id = var.function_app_principal_id

  secret_permissions = [
    "Get"
  ]
}

resource "azurerm_key_vault_access_policy" "sp_policy" {
  key_vault_id = azurerm_key_vault.kv.id

  tenant_id = var.tenant_id
  object_id = var.service_principal_id

  secret_permissions = [
    "Get",
    "Set",
    "List",
    "Delete"
  ]
}
