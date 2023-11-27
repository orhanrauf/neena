output "function_app_id" {
  value = azurerm_function_app.funcapp.id
}

output "function_app_principal_id" {
  value = azurerm_function_app.funcapp.identity[0].principal_id
}