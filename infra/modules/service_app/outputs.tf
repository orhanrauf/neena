output "service_app_id" {
  value = azurerm_app_service.app_service.id
}

output "service_app_principal_id" {
  value = azurerm_app_service.app_service.identity[0].principal_id
}

output "name" {
  value = azurerm_app_service.app_service.name
}