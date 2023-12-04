output "function_app_id" {
  value = azurerm_function_app.funcapp.id
}

output "principal_id" {
  value = azurerm_function_app.funcapp.identity[0].principal_id
}   