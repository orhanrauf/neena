output "postgresql_server_id" {
  value = azurerm_postgresql_server.psql_server.id
}

output "postgresql_server_name" {
  value = azurerm_postgresql_server.psql_server.name
}
output "database_name" {
  value = azurerm_postgresql_database.psql_db.name
}

output "postgresql_server_fqdn" {
  value = azurerm_postgresql_server.psql_server.fqdn
}