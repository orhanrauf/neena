output "function_app_principal_id" {
  value = module.function_app.principal_id
}

output "service_app_principal_id" {
  value = module.service_app.service_app_principal_id
}

output "service_app_name" {
  value = module.service_app.name
}

output "service_app_base_url" {
  value = module.service_app.service_app_base_url
}

output "function_app_name" {
  value = module.function_app.name
}

output "postgresql_server_name" {
  value = module.postgresql.postgresql_server_name
}

output "postgresql_database_name" {
  value = module.postgresql.database_name
}

output "postgresql_server_id" {
  value = module.postgresql.postgresql_server_id
}

output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "postgresql_server_fqdn" {
  value = module.postgresql.postgresql_server_fqdn
}