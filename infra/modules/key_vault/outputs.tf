output "key_vault_id" {
  description = "The ID of the Key Vault."
  value       = azurerm_key_vault.kv.id
}

output "key_vault_uri" {
  description = "The URI of the Key Vault."
  value       = azurerm_key_vault.kv.vault_uri
}

output "name" {
  description = "The name of the Key Vault."
  value       = azurerm_key_vault.kv.name
}
