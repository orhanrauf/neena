output "function_app_default_hostname" {
  value = module.function_app.default_hostname
}

output "function_app_principal_id" {
  value = module.function_app.principal_id
}

output "resource_group_name" {
  value = azurerm_resource_group.example_rg.name
}

output "resource_group_location" {
  value = azurerm_resource_group.example_rg.location
}