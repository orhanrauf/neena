output "static_site_default_hostname" {
  value = azurerm_static_site.neena_core_static_app.default_host_name
  description = "The default hostname of the static site."
}

output "static_site_id" {
  value = azurerm_static_site.neena_core_static_app.id
  description = "The ID of the static site."
}

output "static_site_url" {
  value = "https://${azurerm_static_site.neena_core_static_app.default_host_name}"
  description = "The URL of the static site."
}