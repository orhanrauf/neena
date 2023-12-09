output "service_app_id" {
  value = azurerm_linux_web_app.app_service.id
}

output "service_app_principal_id" {
  value = azurerm_linux_web_app.app_service.identity[0].principal_id
}

output "name" {
  value = azurerm_linux_web_app.app_service.name
}

output "outbound_ip_addresses" {
  value = azurerm_linux_web_app.app_service.outbound_ip_addresses
}