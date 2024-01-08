output "endpoint" {
  value = azurerm_storage_account.website.primary_web_endpoint
}

output "blob_store_account_name" {
  value = azurerm_storage_account.website.name
}