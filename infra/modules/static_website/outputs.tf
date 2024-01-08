output "endpoint" {
  value = azurerm_storage_account.website.primary_web_endpoint
}

output "blob_store_account_name" {
  value = azurerm_storage_account.website.name
}

output "blob_connection_string" {
  value = azurerm_storage_account.website.primary_connection_string
}