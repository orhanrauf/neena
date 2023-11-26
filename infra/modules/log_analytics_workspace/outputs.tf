output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.law.id
}

output "log_analytics_workspace_primary_shared_key" {
  value     = azurerm_log_analytics_workspace.law.primary_shared_key
  sensitive = true
}

output "log_analytics_workspace_secondary_shared_key" {
  value     = azurerm_log_analytics_workspace.law.secondary_shared_key
  sensitive = true
}
